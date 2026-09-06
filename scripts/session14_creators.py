#!/usr/bin/env python3
"""Session 14 — creator batch generator (fitness / fitness-model / swimwear / bikini-fashion /
beachwear / modeling / college-athlete categories) from verified public sources.

Reads data/research/s14_creators.json — a list of creator dicts, each with fields assembled
line-by-line from public sources OPENED during research:

  {
    "name": str,
    "dob": "YYYY-MM-DD",                    # documented date of birth
    "dobYearOnly": bool,                    # True when only the birth YEAR is documented
    "categories": [str, ...],               # objective categories
    "ig", "igFollowers", "x", "xFollowers", "tt", "ttFollowers", "yt", "ytFollowers",
    "website": str,
    "dobSourceLabel", "dobSourceUrl",       # source that documents the birth date
    "genderSourceLabel", "genderSourceUrl", # source that documents she is a woman
    "identitySourceLabel", "identitySourceUrl",  # source that documents real person / ownership
    "notes": str,
  }

Follower counts are recorded ONLY from a publicly observed display/snapshot (with countType and
checkedAt); otherwise FOLLOWER_COUNT_UNKNOWN / FOLLOWER_RANGE_UNKNOWN (never estimated, never
summed). Duplicates are detected on normalized name and on every handle.

Usage:
  python3 scripts/session14_creators.py [--apply] [--pool PATH] [--audit PATH]
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session13_volleyball as s13  # noqa: E402

ROOT = s13.ROOT
RESEARCH = os.path.join(ROOT, "data", "research")
CATALOG = s13.CATALOG
TODAY = date(2026, 9, 7)
UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE

# Verification-blocking flags: any pool entry carrying one of these is routed to the
# REVIEW_REQUIRED queue instead of being promoted, because the conflicting/missing
# evidence must be reconciled before the record can be considered verified.
BLOCKING_FLAGS = {
    "DOB_YEAR_CONFLICT",      # two independent sources disagree on the birth year
    "AGE_CONFLICTING_VALUES",  # two different date-of-birth values recorded
    "AGE_SOURCE_IDENTITY_UNRESOLVED",
    "NAME_MISMATCH_IN_CITED_SOURCE",
    "IDENTITY_UNCERTAIN",
    "PROFILE_UNVERIFIED",
}

POOL = os.path.join(RESEARCH, sys.argv[sys.argv.index("--pool") + 1]) if "--pool" in sys.argv \
    else os.path.join(RESEARCH, "s14_creators.json")
AUDIT = os.path.join(RESEARCH, sys.argv[sys.argv.index("--audit") + 1]) if "--audit" in sys.argv \
    else os.path.join(RESEARCH, "s14_creators_selected.tsv")


def strip_accents(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))


def norm_name(name):
    return re.sub(r"\s+", " ", strip_accents(name).lower()).strip()


def prop(d, key):
    v = d.get(key)
    return (v or "").strip()


def domain_label(url):
    if not url:
        return ""
    host = re.sub(r"^https?://", "", url).split("/")[0]
    return host.replace("www.", "")


def size_range(numeric):
    if numeric is None:
        return UNKNOWN_RANGE
    buckets = [(1000, "Under 1K"), (5000, "1K\u20134.9K"), (10000, "5K\u20139.9K"),
               (25000, "10K\u201324.9K"), (50000, "25K\u201349.9K"),
               (100000, "50K\u201399.9K"), (250000, "100K\u2013249.9K"),
               (500000, "250K\u2013499.9K"), (1000000, "500K\u2013999.9K"),
               (5000000, "1M\u20134.9M")]
    for limit, label in buckets:
        if numeric < limit:
            return label
    return "5M+"


SOCIAL_META = {
    "Instagram": ("https://www.instagram.com/{}/", "@{}"),
    "X": ("https://x.com/{}", "@{}"),
    "TikTok": ("https://www.tiktok.com/@{}", "@{}"),
    "YouTube": ("https://www.youtube.com/channel/{}", "{}"),
}


def social_url(platform, handle):
    return SOCIAL_META[platform][0].format(handle)


def social_display(platform, handle):
    return SOCIAL_META[platform][1].format(handle)


def make_account(platform, handle, display, followers, count_type, source_note):
    numeric = None
    fsize = UNKNOWN_RANGE
    if display != UNKNOWN_COUNT and followers is not None:
        numeric = followers
        fsize = size_range(followers)
    return {
        "platform": platform,
        "username": social_display(platform, handle),
        "profileUrl": social_url(platform, handle),
        "followerCountDisplay": display,
        "followerCountNumeric": numeric,
        "countType": count_type,
        "checkedAt": TODAY.isoformat(),
        "followerSizeRange": fsize,
        "sourceNote": source_note,
    }


def build_entry(idx, c):
    name = c["name"]
    dob = c["dob"]
    year_only = c.get("dobYearOnly", False)
    age_label = (f"Born in {dob[:4]}" if year_only else f"Born {dob}")
    age_summary = (
        f"{age_label} \u2014 an adult (18+) as of {TODAY.isoformat()} (documented birth "
        f"{'year' if year_only else 'date'} from an established public biographical source; "
        f"not inferred from appearance, clothing, photographs or any image-based judgement). "
        f"Source: {c['dobSourceLabel']} ({c['dobSourceUrl']})."
    )
    adult = {
        "summary": age_summary,
        "sourceLabel": c.get("dobSourceLabel", domain_label(c["dobSourceUrl"])),
        "sourceUrl": c["dobSourceUrl"],
        "checkedAt": TODAY.isoformat(),
    }
    gender = {
        "summary": (f"Woman \u2014 documented by {c.get('genderSourceLabel')} "
                    f"({c.get('genderSourceUrl')}); she operates a public "
                    f"{', '.join(c['categories'])} profile. Gender is established from "
                    f"documentary public evidence, never from appearance or imagery."),
        "sourceLabel": c.get("genderSourceLabel", domain_label(c["genderSourceUrl"])),
        "sourceUrl": c["genderSourceUrl"],
        "checkedAt": TODAY.isoformat(),
    }

    sources = []
    for label, url in ((c.get("dobSourceLabel"), c.get("dobSourceUrl")),
                       (c.get("genderSourceLabel"), c.get("genderSourceUrl")),
                       (c.get("identitySourceLabel"), c.get("identitySourceUrl"))):
        if not url:
            continue
        host = domain_label(url)
        if host in ("instagram.com", "x.com", "tiktok.com", "youtube.com", "facebook.com"):
            rel = "verified-platform"
        elif host in ("fitveganchef.com", "generationiron.com", "greatestphysiques.com",
                      "fitnessvolt.com", "hoodmwr.com", "hubpages.com", "ranker.com",
                      "famousbirthdays.com", "biographyhost.com", "aminoshots.com",
                      "richathletes.com", "prweb.com", "healthtasy.com"):
            rel = "press" if host not in ("fitveganchef.com",) else "official"
        else:
            rel = "other-trusted"
        sources.append({"label": label or domain_label(url), "platform": "Website",
                        "url": url, "relationship": rel})

    accounts = []
    handles = {}
    # platform -> (handle key in pool, follower display key, follower numeric key)
    PLAT_KEYS = {"Instagram": ("ig", "igFollowers", "igFollowersNumeric"),
                 "X": ("x", "xFollowers", "xFollowersNumeric"),
                 "TikTok": ("tt", "ttFollowers", "ttFollowersNumeric"),
                 "YouTube": ("yt", "ytFollowers", "ytFollowersNumeric")}
    for platform in ("Instagram", "X", "TikTok", "YouTube"):
        hkey, dkey, nkey = PLAT_KEYS[platform]
        handle = prop(c, hkey)
        if not handle:
            continue
        handles[platform] = handle
        display = c.get(dkey, UNKNOWN_COUNT)
        numeric = c.get(nkey) if display != UNKNOWN_COUNT else None
        count_type = "rounded" if display != UNKNOWN_COUNT else "unknown"
        source_note = (f"Publicly observed {platform} figure for @{handle} (published snapshot) on "
                       f"{TODAY.isoformat()}." if display != UNKNOWN_COUNT else
                       f"Handle recorded from {domain_label(c.get('identitySourceUrl') or c.get('dobSourceUrl'))}. "
                       f"No follower count was publicly observed on {TODAY.isoformat()} "
                       f"(the platform blocks automated retrieval), so it is recorded as "
                       f"{UNKNOWN_COUNT} rather than estimated.")
        accounts.append(make_account(platform, handle, display, numeric, count_type, source_note))

    # largest public following -> max single platform
    known = [a for a in accounts if a.get("followerCountNumeric") is not None]
    largest = None
    if known:
        best = max(known, key=lambda a: a["followerCountNumeric"])
        largest = {"platform": best["platform"], "username": best["username"],
                   "display": best["followerCountDisplay"],
                   "numeric": best["followerCountNumeric"],
                   "sizeRange": best["followerSizeRange"], "checkedAt": TODAY.isoformat()}
    overall = largest["sizeRange"] if largest else UNKNOWN_RANGE

    if c.get("website"):
        sources.append({"label": f"{name} \u2014 official website",
                        "platform": "Website", "url": c["website"], "relationship": "official"})

    entry = {
        "id": f"W-2026-{idx}",
        "displayName": name,
        "categories": list(dict.fromkeys(c["categories"])),
        "legalAdultEvidence": adult,
        "genderEvidence": gender,
        "sources": sources,
        "socialAccounts": accounts,
        "overallFollowerSizeRange": overall,
        "verificationStatus": "verified",
        "lastReviewed": TODAY.isoformat(),
        "flags": list(dict.fromkeys(
            list(c.get("flags", [])) + (["BIRTH_YEAR_ONLY"] if year_only else []))),
        "notes": c.get("notes", ""),
    }
    if largest:
        entry["largestPublicFollowing"] = largest

    return entry


def build_review_item(next_r, c):
    """Build a REVIEW_REQUIRED queue item for an entry whose evidence is incomplete/conflicting."""
    # prefer the most-evidenced public handle for the queue's single handle/platform record
    platform = None
    for p, hk, dk, nk in (("Instagram", "ig", "igFollowers", "igFollowersNumeric"),
                          ("X", "x", "xFollowers", "xFollowersNumeric"),
                          ("TikTok", "tt", "ttFollowers", "ttFollowersNumeric"),
                          ("YouTube", "yt", "ytFollowers", "ytFollowersNumeric")):
        handle = prop(c, hk)
        if handle:
            platform, handle_used, count_display, count_numeric = p, handle, \
                c.get(dk, UNKNOWN_COUNT), (c.get(nk) if c.get(dk, UNKNOWN_COUNT) != UNKNOWN_COUNT else None)
            profile = social_url(p, handle)
            break
    flags = list(dict.fromkeys(c.get("flags", []) + (["BIRTH_YEAR_ONLY"] if c.get("dobYearOnly") else [])))
    blocking = [f for f in flags if f in BLOCKING_FLAGS]
    # a blocking flag is the reason routing happened (or AGE_EVIDENCE_INSUFFICIENT)
    reason_flags = blocking if blocking else ["AGE_EVIDENCE_INSUFFICIENT"]
    evidence_summary = (
        f"Discovered in the fitness / bikini-fashion creator pool; candidate was NOT promoted to "
        f"the verified catalog. Known evidence: documented birth "
        f"{c.get('dob', 'NOT RECORDED')} from {c.get('dobSourceLabel', 'no source')} "
        f"({c.get('dobSourceUrl', 'no URL')}); gender source {c.get('genderSourceLabel', 'no source')} "
        f"({c.get('genderSourceUrl', 'no URL')}). A review-required flag applies: "
        f"{', '.join(reason_flags)}. Per the no-hallucination rule this candidate is routed to "
        f"REVIEW_REQUIRED rather than guessed; reconcile the conflicting/missing evidence before promotion."
    )
    return {
        "id": f"R-2026-{next_r}",
        "displayName": c["name"],
        "handle": social_display(platform, handle_used) if platform else (prop(c, "ig") or ""),
        "platform": platform or "Instagram",
        "profileUrl": profile if platform else "",
        "discoveryCategory": c.get("discoveryCategory", "; ".join(c.get("categories", []))),
        "evidenceFound": {
            "summary": evidence_summary,
            "sourceLabel": c.get("dobSourceLabel", ""),
            "sourceUrl": c.get("dobSourceUrl", ""),
        },
        "missingEvidence": reason_flags,
        "flags": reason_flags,
        "lastChecked": TODAY.isoformat(),
        "notes": c.get("notes", ""),
        "followerCountDisplay": count_display if platform else UNKNOWN_COUNT,
        "followerCountNumeric": count_numeric if platform else None,
        "followerCountCheckedAt": TODAY.isoformat() if platform else None,
        "followerSizeRange": size_range(count_numeric) if (platform and count_numeric is not None) else UNKNOWN_RANGE,
    }


def main():
    apply_changes = "--apply" in sys.argv
    if not os.path.exists(POOL):
        print(f"missing pool file: {POOL}")
        return 1
    with open(POOL, encoding="utf-8") as fh:
        pool = json.load(fh)
    if not isinstance(pool, list):
        print("pool must be a list")
        return 1

    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    existing_names = {norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    existing_handles = set()
    for e in catalog["entries"]:
        for a in e.get("socialAccounts", []):
            existing_handles.add(a.get("username", "").lstrip("@").lower())
    rq_names = {norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}
    for r in catalog.get("reviewQueue", []):
        h = r.get("handle") or ""
        if h:
            existing_handles.add(h.lstrip("@").lower())

    next_id = max(int(e["id"].split("-")[-1]) for e in catalog["entries"]) + 1
    # review-queue rows may carry the id under either 'id' or 'queueId'
    rq_ids = [int((r.get("id") or r.get("queueId") or "").split("-")[-1])
              for r in catalog.get("reviewQueue", []) if (r.get("id") or r.get("queueId") or "").startswith("R-2026-")]
    next_r = (max(rq_ids) + 1) if rq_ids else 1
    selected, skipped, queued = [], [], []
    seen_names, seen_handles = set(), set()
    new_queue_rows = []

    for c in pool:
        name = c["name"]
        key = norm_name(name)
        hkeys = {prop(c, p.lower()).lower() for p in ("Instagram", "X", "TikTok", "YouTube")}
        hkeys.discard("")
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((c, "duplicate-name"))
            continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((c, "duplicate-handle"))
            continue
        if not c.get("dobSourceUrl") or not c.get("dob"):
            queued.append((c, "AGE_EVIDENCE_INSUFFICIENT"))
            continue
        if not c.get("genderSourceUrl"):
            queued.append((c, "GENDER_EVIDENCE_INSUFFICIENT"))
            continue
        if BLOCKING_FLAGS & set(c.get("flags", [])):
            flag = next((f for f in c["flags"] if f in BLOCKING_FLAGS))
            queued.append((c, flag))
            qitem = build_review_item(next_r, c)
            new_queue_rows.append(qitem)
            next_r += 1
            continue
        entry = build_entry(next_id, c)
        if not entry["socialAccounts"]:
            skipped.append((c, "no-public-handle"))
            continue
        selected.append((c, entry))
        seen_names.add(key)
        seen_handles |= hkeys
        next_id += 1

    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# Session 14 creator audit (generated {TODAY.isoformat()}).\n")
        fh.write("# entryId\tname\tdob\tcategories\thandles\tdobSource\n")
        for c, e in selected:
            h = ";".join(f"{p}:{a['username']}" for p, a in
                         [(x["platform"], x) for x in e["socialAccounts"]])
            fh.write("\t".join([e["id"], c["name"], c["dob"], ";".join(c["categories"]),
                                h, c.get("dobSourceUrl", "")]) + "\n")

    print(f"pool size       : {len(pool)}")
    print(f"promoted        : {len(selected)}")
    print(f"skipped         : {len(skipped)}")
    sc = {}
    for _, r in skipped:
        sc[r] = sc.get(r, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    print(f"queued          : {len(queued)}")
    qc = {}
    for _, r in queued:
        qc[r] = qc.get(r, 0) + 1
    for r, n in sorted(qc.items()):
        print(f"    {r}: {n}")
    print(f"entry range     : W-2026-{next_id - len(selected)} .. W-2026-{next_id - 1}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return 0

    catalog["entries"].extend(e for _, e in selected)
    if new_queue_rows:
        catalog.setdefault("reviewQueue", [])
        catalog["reviewQueue"].extend(new_queue_rows)
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 14 added {len(selected)} verified creator profiles from public-web activity-first "
        f"research across fitness, fitness-model, swimwear, bikini-fashion, beachwear, modeling and "
        f"college-athlete categories. Follower counts were captured only where publicly observed; "
        f"otherwise {UNKNOWN_COUNT} / {UNKNOWN_RANGE} (never estimated, never summed)."
    )
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
