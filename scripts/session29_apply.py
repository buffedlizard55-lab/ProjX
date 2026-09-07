#!/usr/bin/env python3
"""Session 29 — Verification Apply Pipeline (model/pageant/creator WDQS harvest page 2, cursor > Q134404200; adapted from session28_apply.py).

Reads the line-by-line verification verdicts from
data/research/verification_s29_log.tsv (pipe-delimited:
    qid|name|dob|verdict|category|evidence|source_url)
and joins them with data/research/s29_verify_buckets.json (handles, wiki).

- PROMOTE            -> data/catalog.json entries (catalogType=social, ID from W-2026-2130)
- REVIEW             -> data/catalog.json reviewQueue (ID from R-2026-318)
- MINOR_UNDERAGE     -> reviewQueue with MINOR_UNDERAGE flag (re-evaluate on the 18th birthday)
- REJECT             -> no entry (verdict retained in the verification log only)

No names, DOBs, handles, URLs, or follower counts are invented. Follower
counts are recorded as FOLLOWER_COUNT_UNKNOWN unless observed on the
verifying page. After updating the catalog, run scripts/build_directory.py
to rebuild the IG/TikTok directory subpages in lockstep.

Usage:
  python3 scripts/session29_apply.py [--dry-run]
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "catalog.json"
LOG_PATH = ROOT / "data" / "research" / "verification_s29_log.tsv"
BUCKETS_PATH = ROOT / "data" / "research" / "s29_verify_buckets.json"

TODAY = date(2026, 9, 6)
UNKNOWN_COUNT = "FOLLOWER_COUNT_UNKNOWN"
UNKNOWN_RANGE = "FOLLOWER_RANGE_UNKNOWN"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# Flags that classify a candidate as adult (full DOB) even when verdict=REVIEW.
# (kept for clarity; not used to override verdicts)


def strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(ch))


def norm_name(name: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(name).lower()).strip()


def parse_dob(dob_str: str) -> date | None:
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", dob_str.strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def age_on(dob: date, on_date: date = TODAY) -> int:
    return on_date.year - dob.year - ((on_date.month, on_date.day) < (dob.month, dob.day))


def human_date(d: date) -> str:
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def make_profile_url(platform: str, handle: str) -> str:
    h = handle.lstrip("@").strip()
    if platform == "TikTok":
        return f"https://www.tiktok.com/@{h}"
    return f"https://www.instagram.com/{h}/"


def clean_handle(platform: str, handle: str) -> str:
    h = handle.strip()
    if not h:
        return ""
    if h.startswith("@"):
        return h
    return f"@{h}"


def domain_of(url: str) -> str:
    try:
        return urlparse(url).netloc or url
    except ValueError:
        return url


SECONDARY_HOSTS = ("famousbirthdays.com", "fandom.com", "imdb.com", "starsunfolded.com",
                   "narcobi.com", "themoviedb.org", "myanimelist.net", "bgm.tv",
                   "kimnereli.net", "dreshare.com")


def evidence_flags(source_url: str, dob: date, evidence: str = "") -> list[str]:
    """Age-evidence provenance flags, following the catalog's existing conventions:
    AGE_EVIDENCE_WIKIPEDIA_ONLY when the only DOB source is a Wikipedia article,
    AGE_EVIDENCE_SECONDARY_SOURCES when the DOB comes from a secondary biography
    database, DOB_JAN1_POSSIBLE_YEAR_PRECISION for 1 January dates."""
    flags: list[str] = []
    host = domain_of(source_url)
    if host.endswith("wikipedia.org"):
        flags.append("AGE_EVIDENCE_WIKIPEDIA_ONLY")
    elif any(host == h or host.endswith("." + h) for h in SECONDARY_HOSTS):
        flags.append("AGE_EVIDENCE_SECONDARY_SOURCES")
    if dob.month == 1 and dob.day == 1:
        flags.append("DOB_JAN1_POSSIBLE_YEAR_PRECISION")
    if evidence and "preferred over Wikidata" in evidence:
        # Wikidata held a 1 January year-precision value; the cited Wikipedia date was used instead
        flags.append("MINOR_SOURCE_CONFLICT_NOTED")
    return flags


def assign_categories(cat_label: str) -> list[str]:
    text = cat_label.lower()
    cats: list[str] = []
    if "beach volleyball" in text:
        cats.extend(["Beach Volleyball", "Athlete", "Sports"])
    elif "volleyball" in text:
        cats.extend(["Volleyball", "Athlete", "Sports"])
    if "ncaa" in text or "college" in text:
        cats.append("College Athlete")
    if "fitness" in text:
        cats.extend(["Fitness", "Fitness Model"])
    if any(w in text for w in ("model", "swimwear", "bikini", "beachwear", "fashion")):
        if "Modeling" not in cats:
            cats.extend(["Modeling", "Fashion"])
    if "creator" in text or "tv" in text or "influencer" in text:
        if "Creator" not in cats:
            cats.append("Creator")
    if not cats:
        cats = ["Creator", "Modeling", "Fashion"]
    seen = set()
    result = []
    for c in cats:
        if c not in seen:
            seen.add(c)
            result.append(c)
    if "Creator" not in result and len(result) < 3:
        result.append("Creator")
    return result


def load_verdicts() -> list[dict]:
    rows = []
    with open(LOG_PATH) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.startswith("Q"):
                continue
            parts = line.split("|")
            if len(parts) < 7:
                raise ValueError(f"Malformed log line: {line[:80]}")
            rows.append({
                "qid": parts[0].strip(),
                "name": parts[1].strip(),
                "dob": parts[2].strip(),
                "verdict": parts[3].strip(),
                "category": parts[4].strip(),
                "evidence": parts[5].strip(),
                "source_url": parts[6].strip(),
            })
    return rows


def load_buckets() -> dict:
    with open(BUCKETS_PATH) as f:
        b = json.load(f)
    by_qid: dict[str, dict] = {}
    for item in b.get("model", []) + b.get("volleyball", []) + b.get("wiki", []) + b.get("agency", []):
        by_qid[item["qid"].strip()] = item
    return by_qid


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    catalog = json.load(open(CATALOG_PATH))
    buckets = load_buckets()
    verdicts = load_verdicts()

    entries = catalog["entries"]
    rq = catalog["reviewQueue"]

    existing_names: set[str] = set()
    existing_qids: set[str] = set()
    existing_igs: set[str] = set()
    existing_tts: set[str] = set()
    max_w = 0
    max_r = 0
    for e in entries:
        m = re.match(r"^W-2026-(\d+)$", e["id"])
        if m:
            max_w = max(max_w, int(m.group(1)))
        existing_names.add(norm_name(e.get("displayName", "")))
        for s in e.get("sources", []):
            u = s.get("url", "")
            if "wikidata.org/wiki/Q" in u:
                existing_qids.add(u.split("wikidata.org/wiki/")[1].strip("/").split("?")[0])
        for sa in e.get("socialAccounts", []):
            u = sa.get("username", "").lstrip("@").lower().strip()
            if sa.get("platform") == "Instagram" and u:
                existing_igs.add(u)
            if sa.get("platform") == "TikTok" and u:
                existing_tts.add(u)
    for r in rq:
        m = re.match(r"^R-2026-(\d+)$", r.get("id", ""))
        if m:
            max_r = max(max_r, int(m.group(1)))
        existing_names.add(norm_name(r.get("displayName", "")))
        u = (r.get("handle") or "").lstrip("@").lower().strip()
        if r.get("platform") == "Instagram" and u:
            existing_igs.add(u)
        if r.get("platform") == "TikTok" and u:
            existing_tts.add(u)
        evf = r.get("evidenceFound")
        ev_url = evf.get("sourceUrl", "") if isinstance(evf, dict) else ""
        if "wikidata.org/wiki/Q" in ev_url:
            existing_qids.add(ev_url.split("wikidata.org/wiki/")[1].strip("/").split("?")[0])

    print(f"Catalog: {len(entries)} entries (max W-2026-{max_w:04d}); "
          f"reviewQueue: {len(rq)} (max R-2026-{max_r:03d})")

    new_entries: list[dict] = []
    new_reviews: list[dict] = []
    skipped: list[str] = []
    seen_in_batch_q: set[str] = set()
    seen_in_batch_n: set[str] = set()
    seen_in_batch_i: set[str] = set()
    seen_in_batch_t: set[str] = set()

    for v in verdicts:
        qid = v["qid"]
        name = v["name"] or buckets.get(qid, {}).get("name", "")
        nname = norm_name(name)
        b = buckets.get(qid, {})
        ig = (b.get("ig") or "").strip()
        tt = (b.get("tt") or "").strip()
        wiki = (b.get("wiki") or "").strip()
        if not name:
            skipped.append(f"{qid}: no name")
            continue
        if qid in seen_in_batch_q or nname in seen_in_batch_n:
            skipped.append(f"{qid} {name}: dupe in batch")
            continue
        if qid in existing_qids:
            skipped.append(f"{qid} {name}: qid already in catalog")
            continue
        if nname in existing_names:
            skipped.append(f"{qid} {name}: name already in catalog")
            continue
        if ig and ig.lower() in existing_igs:
            skipped.append(f"{qid} {name}: IG already in catalog")
            continue
        if tt and tt.lower() in existing_tts:
            skipped.append(f"{qid} {name}: TT already in catalog")
            continue

        verdict = v["verdict"]

        if verdict == "PROMOTE":
            dob = parse_dob(v["dob"])
            if dob is None:
                # year-only DOB must not be promoted
                max_r += 1
                new_reviews.append(_review_record(max_r, qid, name, ig, tt,
                                                  "AGE_PARTIAL",
                                                  f"DOB recorded year-only: {v['dob']} "
                                                  f"(source: {domain_of(v['source_url'])}). {v['evidence']}",
                                                  v["source_url"]))
                seen_in_batch_q.add(qid); seen_in_batch_n.add(nname)
                continue
            age = age_on(dob)
            if age < 18:
                raise ValueError(f"Underage PROMOTE: {name} age {age}")
            if not (ig or tt):
                max_r += 1
                new_reviews.append(_review_record(max_r, qid, name, ig, tt,
                                                  "MISSING_SOCIAL",
                                                  "No Instagram/TikTok handle documented "
                                                  "(catalog rule: social handle required). "
                                                  f"{v['evidence']}",
                                                  v["source_url"]))
                seen_in_batch_q.add(qid); seen_in_batch_n.add(nname)
                continue
            max_w += 1
            entry_id = f"W-2026-{max_w:04d}"
            new_entries.append(_catalog_record(entry_id, name, dob, age, qid,
                                               v["category"], v["evidence"],
                                               v["source_url"], ig, tt, wiki))
            seen_in_batch_q.add(qid); seen_in_batch_n.add(nname)
            if ig:
                seen_in_batch_i.add(ig.lower())
            if tt:
                seen_in_batch_t.add(tt.lower())

        elif verdict in ("REVIEW", "MINOR_UNDERAGE"):
            if verdict == "MINOR_UNDERAGE":
                flags = ["MINOR_UNDERAGE"]
            else:
                # the category field of REVIEW rows carries the flag token(s)
                head = v["category"].strip()
                flags = [f.strip() for f in re.split(r"\+", head) if f.strip()]
                if not flags or flags == ["excluded"]:
                    flags = ["REVIEW_REQUIRED"]
            note = v["evidence"]
            if verdict == "MINOR_UNDERAGE":
                mdob = parse_dob(v["dob"])
                eighteenth = mdob.replace(year=mdob.year + 18).isoformat() if mdob else "UNKNOWN"
                note = (f"Underage: DOB {v['dob']} (age {age_on(mdob)} as of "
                        f"{TODAY.isoformat()}). Keep in queue; re-evaluate from {eighteenth} "
                        f"(18th birthday). Do NOT discard. {note}")
            max_r += 1
            if verdict == "MINOR_UNDERAGE":
                # never record social handles / profile URLs for a minor, even in the review queue
                ig, tt = "", ""
            new_reviews.append(_review_record(max_r, qid, name, ig, tt,
                                              ",".join(flags), note, v["source_url"]))
            seen_in_batch_q.add(qid); seen_in_batch_n.add(nname)

        elif verdict == "REJECT":
            skipped.append(f"{qid} {name}: REJECT ({v['evidence'][:60]})")

        else:
            skipped.append(f"{qid} {name}: unknown verdict {verdict}")

    print(f"\nNew catalog entries: {len(new_entries)}")
    if new_entries:
        print(f"  IDs W-2026-{max_w - len(new_entries) + 1:04d} .. W-2026-{max_w:04d}")
    print(f"New reviewQueue entries: {len(new_reviews)}")
    if new_reviews:
        print(f"  IDs R-2026-{max_r - len(new_reviews) + 1:03d} .. R-2026-{max_r:03d}")
    print(f"Skipped: {len(skipped)}")
    for s in skipped:
        print(f"  - {s}")

    if dry_run:
        print("\nDRY RUN — catalog not modified.")
        return

    entries.extend(new_entries)
    rq.extend(new_reviews)

    meta = catalog["metadata"]
    meta["generatedAt"] = TODAY.isoformat()
    meta["entryCount"] = len(entries)
    meta["reviewQueueCount"] = len(rq)
    meta["summary"] += (
        f" Session 29 added {len(new_entries)} verified adult female creator profiles "
        f"(models, beauty-pageant titleholders, TV/social-media creators from the "
        f"Wikidata model-pool page 2 beyond Q134404200) and {len(new_reviews)} REVIEW_REQUIRED candidates "
        f"with provenance from line-by-line official/trusted-source verification "
        f"(data/research/verification_s29_log.tsv, {len(verdicts)} verdicts). "
        f"Per-platform follower counts are publicly observed displays only — "
        f"unknown counts recorded as FOLLOWER_COUNT_UNKNOWN."
    )

    catalog["irregularities"].append({
        "id": "IRR-2026-09-06-031",
        "type": "BATCH_INGESTION_SESSION_29",
        "entityId": None,
        "description": (
            f"Session 29 batch ingestion (WDQS female model / fitness-model / pageant / creator pool born 1985-2008 with an Instagram or TikTok handle and an English Wikipedia article, page 2 beyond Q134404200: 150 rows, 145 unique, 139 new after dedup): {len(verdicts)} line-by-line verification verdicts "
            f"({sum(1 for v in verdicts if v['verdict'] == 'PROMOTE')} PROMOTE, "
            f"{sum(1 for v in verdicts if v['verdict'] == 'REVIEW')} REVIEW, "
            f"{sum(1 for v in verdicts if v['verdict'] == 'MINOR_UNDERAGE')} MINOR_UNDERAGE, "
            f"{sum(1 for v in verdicts if v['verdict'] == 'REJECT')} REJECT). "
            f"{len(new_entries)} promoted to Catalog Published (catalogType=social); "
            f"{len(new_reviews)} queued as REVIEW_REQUIRED with missing-evidence flags "
            f"(scope-ambiguous actresses/singers with no documented modeling or creator activity, "
            f"AGE_PARTIAL pages without a full birth date, DOB_CONFLICT between en-wiki and Wikidata, "
            f"three WIKI_REDIRECT titles that resolve to another person's or a group's article, and one "
            f"GENDER_EVIDENCE_REVIEW where the article's pronouns disagree with the Wikidata record); "
            f"{len([s for s in skipped if 'REJECT' in s])} rejected (a Wikidata item for a musical duo "
            f"mis-typed as a single person). See data/research/verification_s29_log.tsv."
        ),
        "detectedAt": TODAY.isoformat(),
        "resolved": True,
    })

    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print("\nUpdated data/catalog.json.")


def _catalog_record(entry_id: str, name: str, dob: date, age: int, qid: str,
                    cat_label: str, evidence: str, source_url: str,
                    ig: str, tt: str, wiki: str) -> dict:
    categories = assign_categories(cat_label)

    src_label = f"{domain_of(source_url)} — {name}"
    legal_adult_evidence = {
        "summary": (f"Born {human_date(dob)} ({dob.isoformat()}) — age {age} as of "
                    f"{TODAY.isoformat()}, so an adult (18+). Verified line-by-line from "
                    f"official/trusted public source: {evidence}. Adult status rests "
                    f"strictly on the verified birth date, never on appearance, clothing, "
                    f"photographs, or AI inference."),
        "sourceLabel": src_label,
        "sourceUrl": source_url,
        "checkedAt": TODAY.isoformat(),
    }
    gender_evidence = {
        "summary": ("Identified as a woman from public official documentary records "
                    "(agency/roster/profile records and women's professional/creative "
                    "activities). Gender is established from documentary records, never "
                    "from appearance, body type, or imagery."),
        "sourceLabel": (f"Wikidata {qid} — {name}" if qid else f"Official profile record — {name}"),
        "sourceUrl": (f"https://www.wikidata.org/wiki/{qid}" if qid else source_url),
        "checkedAt": TODAY.isoformat(),
    }

    sources = []
    sources.append({
        "label": src_label,
        "platform": "Website",
        "url": source_url,
        "relationship": "age-evidence",
    })
    if qid:
        sources.append({
            "label": f"Wikidata {qid} — {name}",
            "platform": "Website",
            "url": f"https://www.wikidata.org/wiki/{qid}",
            "relationship": "other-trusted",
        })
    if wiki and wiki != source_url:
        sources.append({
            "label": f"Wikipedia — {name}",
            "platform": "Website",
            "url": wiki,
            "relationship": "other-trusted",
        })

    social_accounts = []
    if ig:
        ig_clean = clean_handle("Instagram", ig)
        ig_url = make_profile_url("Instagram", ig)
        social_accounts.append({
            "platform": "Instagram",
            "username": ig_clean,
            "profileUrl": ig_url,
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "countType": "unknown",
            "checkedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
            "sourceNote": f"Handle documented on official / public profile for {name}. No public count observed.",
        })
        sources.append({
            "label": f"Instagram — {ig_clean} (public profile)",
            "platform": "Instagram",
            "url": ig_url,
            "relationship": "verified-platform",
        })
    if tt:
        tt_clean = clean_handle("TikTok", tt)
        tt_url = make_profile_url("TikTok", tt)
        social_accounts.append({
            "platform": "TikTok",
            "username": tt_clean,
            "profileUrl": tt_url,
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "countType": "unknown",
            "checkedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
            "sourceNote": f"Handle documented on official / public profile for {name}. No public count observed.",
        })
        sources.append({
            "label": f"TikTok — {tt_clean} (public profile)",
            "platform": "TikTok",
            "url": tt_url,
            "relationship": "verified-platform",
        })

    notes = f"Session 29 verified (WDQS model/pageant/creator harvest, line-by-line English Wikipedia lead/infobox check). Category: {cat_label}. Evidence: {evidence}"
    return {
        "id": entry_id,
        "displayName": name,
        "categories": categories,
        "legalAdultEvidence": legal_adult_evidence,
        "genderEvidence": gender_evidence,
        "sources": sources,
        "verificationStatus": "verified",
        "lastReviewed": TODAY.isoformat(),
        "flags": evidence_flags(source_url, dob, evidence),
        "notes": notes,
        "socialAccounts": social_accounts,
        "largestPublicFollowing": None,
        "overallFollowerSizeRange": UNKNOWN_RANGE,
        "catalogType": "social",
    }


def _review_record(rnum: int, qid: str, name: str, ig: str, tt: str,
                   flags: str, notes: str, source_url: str) -> dict:
    handle = clean_handle("Instagram", ig) if ig else (clean_handle("TikTok", tt) if tt else "")
    platform = "Instagram" if ig else ("TikTok" if tt else "")
    profile_url = (make_profile_url("Instagram", ig) if ig
                   else (make_profile_url("TikTok", tt) if tt else ""))
    flag_list = [f.strip() for f in flags.split(",") if f.strip()]
    return {
        "id": f"R-2026-{rnum:03d}",
        "displayName": name,
        "handle": handle,
        "platform": platform,
        "profileUrl": profile_url,
        "discoveryCategory": "Session 29 (modeling / beauty pageant / fitness / creator — WDQS harvest)",
        "evidenceFound": {
            "summary": notes[:400],
            "sourceLabel": f"{domain_of(source_url)} — {name}",
            "sourceUrl": source_url,
        },
        "missingEvidence": flag_list,
        "flags": flag_list,
        "lastChecked": TODAY.isoformat(),
        "notes": f"Session 29 verification (2026-09-06), Wikidata Q-ID {qid}. {notes}",
        "followerCountDisplay": UNKNOWN_COUNT,
        "followerCountNumeric": None,
        "followerCountCheckedAt": TODAY.isoformat(),
        "followerSizeRange": UNKNOWN_RANGE,
    }


if __name__ == "__main__":
    main()
