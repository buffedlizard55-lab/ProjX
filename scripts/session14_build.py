#!/usr/bin/env python3
"""Session 14 — continuation of the structured-data women's volleyball discovery (and the
fitness / swimwear / bikini-fashion / modeling categories).

Reuses the Session 13 builder (scripts/session13_volleyball.py) exactly: every row is promoted
only when the recorded date of birth is traceable to a document (a reference URL on the
Wikidata statement), each entry carries its own cited age & gender evidence, a dedupe check on
name *and* every handle, and FOLLOWER_COUNT_UNKNOWN / FOLLOWER_RANGE_UNKNOWN instead of a guess.

Input research file (pipe-delimited):

  qid|name|dob|country|group|ig|x|tt|refUrl|teams;teams;...

where group is one of {ncaa, beach, intl} and refUrl is the primary reference URL recorded
against the date-of-birth statement (so adult status is traceable to a document).

Usage: python3 scripts/session14_build.py [--pool PATH] [--label TEXT] [--apply]

Without --apply the script only prints the plan and writes the audit TSV.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session13_volleyball as s13  # noqa: E402

ROOT = s13.ROOT
RESEARCH = os.path.join(ROOT, "data", "research")
CATALOG = s13.CATALOG

TODAY = date(2026, 9, 7)
s13.TODAY = TODAY
s13.age_on.__defaults__ = (TODAY,)

UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE


def arg(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


POOL = os.path.join(RESEARCH, arg("--pool", "s14_pool.tsv"))
AUDIT = os.path.join(RESEARCH, arg("--audit", "s14_selected.tsv"))
PASS_LABEL = arg("--label", "Session 14 structured-data volleyball & creator expansion (2026-09-07)")


def dash(value):
    value = (value or "").strip()
    return "" if value in ("", "-", "UNKNOWN") else value


def load_candidates(path):
    cands = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 9:
                continue
            qid, name, dob, country, group, ig, x, tt, refurl = parts[:9]
            teams = [t for t in parts[9:11] if t.strip()] if len(parts) > 9 else []
            handles = {}
            if dash(ig):
                handles["Instagram"] = dash(ig)
            if dash(x):
                handles["X"] = dash(x)
            if dash(tt):
                handles["TikTok"] = dash(tt)
            cands.append({
                "qid": qid, "name": name, "dob": dash(dob), "group": group,
                "country": dash(country) or "UNKNOWN", "teams": teams,
                "handles": handles, "dob_sources": [],
                "ref_urls": [dash(refurl)] if dash(refurl) else [],
                "wiki_urls": [], "imports": [],
            })
    return cands


def group_label(group):
    return {"ncaa": "NCAA / US college volleyball",
            "beach": "international beach volleyball",
            "intl": "European / international indoor volleyball"}.get(group, group)


def reason_explanation(reason):
    return {
        "AGE_UNVERIFIED": "the structured item carries no date of birth, so adult status cannot be "
                          "documented (and is never inferred from college attendance or appearance).",
        "AGE_SOURCE_NOT_RECORDED": "a date of birth is present but no reference source is attached to it, "
                                   "so the value cannot be traced to a document.",
        "AGE_OUT_OF_RANGE_OR_MINOR": "the recorded date of birth places the candidate outside the adult "
                                     "18+ scope as of 2026-09-07.",
        "SPORT_NOT_CORROBORATED": "every reference URL attached to the recorded date of birth belongs "
                                  "to a domain that is not a volleyball source, so the sport claim is not "
                                  "corroborated by any volleyball document and the profile is not catalogued "
                                  "as a volleyball athlete.",
    }[reason]


def main():
    apply_changes = "--apply" in sys.argv
    if not os.path.exists(POOL):
        print(f"missing pool file: {POOL}")
        return 1

    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    existing_names = {s13.norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    existing_handles = set()
    for e in catalog["entries"]:
        for a in e.get("socialAccounts", []):
            existing_handles.add(a.get("username", "").lstrip("@").lower())
    rq_names = {s13.norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}
    for r in catalog.get("reviewQueue", []):
        h = r.get("handle") or ""
        if h:
            existing_handles.add(h.lstrip("@").lower())

    cands = load_candidates(POOL)
    selected, queued, skipped = [], [], []
    next_id = (max(int(e["id"].split("-")[-1]) for e in catalog["entries"]) + 1)
    seen_names, seen_handles = set(), set()

    for cand in cands:
        key = s13.norm_name(cand["name"])
        handles = {p: h for p, h in cand["handles"].items() if h}
        hkeys = {h.lower() for h in handles.values()}

        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name"))
            continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand, "duplicate-handle"))
            continue
        if not handles:
            skipped.append((cand, "no-public-handle"))
            continue
        # A Wikidata label that is just the Q-ID means no English name is recorded; don't guess one.
        if re.fullmatch(r"Q\d+", cand["name"]):
            skipped.append((cand, "no-display-name"))
            continue

        dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            queued.append((cand, "AGE_UNVERIFIED"))
            continue
        if dob < s13.MIN_DOB or s13.age_on(dob) < 18:
            queued.append((cand, "AGE_OUT_OF_RANGE_OR_MINOR"))
            continue
        if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"] or cand["imports"]):
            queued.append((cand, "AGE_SOURCE_NOT_RECORDED"))
            continue

        entry = s13.build_entry(next_id, cand, dob)
        if not cand["ref_urls"] and not cand["wiki_urls"]:
            entry["flags"] = ["AGE_EVIDENCE_SECONDARY_SOURCES"]
        entry["notes"] = PASS_LABEL + " " + entry["notes"]
        selected.append((cand, dob, entry))
        seen_names.add(key)
        seen_handles |= hkeys
        next_id += 1

    # ---------------- review queue additions
    rq = catalog.get("reviewQueue", [])
    rq_num = max((int(r["id"].split("-")[-1]) for r in rq
                  if isinstance(r, dict) and r.get("id") and re.fullmatch(r"R-\d{4}-\d+", r["id"])),
                 default=0) + 1
    for cand, reason in queued:
        handles = {p: h for p, h in cand["handles"].items() if h}
        platform = "Instagram" if "Instagram" in handles else sorted(handles)[0] if handles else "Instagram"
        handle = handles.get(platform, "")
        rq.append({
            "id": f"R-2026-{rq_num:03d}",
            "displayName": cand["name"],
            "handle": s13.display_handle(platform, handle) if handle else "",
            "platform": platform,
            "profileUrl": s13.profile_url(platform, handle) if handle else "",
            "discoveryCategory": group_label(cand["group"]),
            "evidenceFound": {
                "summary": (f"Wikidata item {cand['qid']} records the athlete as a female "
                            f"{'beach volleyball' if cand['group'] == 'beach' else 'volleyball'} player"
                            + (f" with teams {s13.join_sources(cand['teams'][:3])}" if cand["teams"] else "")
                            + f". Date of birth recorded: {cand['dob'] or 'none'}."),
                "sourceLabel": f"Wikidata {cand['qid']} \u2014 {cand['name']}",
                "sourceUrl": f"https://www.wikidata.org/wiki/{cand['qid']}",
            },
            "missingEvidence": [reason],
            "flags": [reason],
            "lastChecked": TODAY.isoformat(),
            "notes": (f"{PASS_LABEL}. Not promoted to a verified entry: {reason_explanation(reason)} "
                      f"Candidate Q-ID {cand['qid']}; country recorded in Wikidata: {cand['country']}."),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    # ---------------- audit artifact
    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# {PASS_LABEL} \u2014 selection audit (generated {TODAY.isoformat()}).\n")
        fh.write("# entryId\tqid\tgroup\tname\tdob\tage\tcountry\thandles\treferenceUrls\tteams\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["group"], cand["name"], dob.isoformat(),
                str(s13.age_on(dob)), cand["country"], handles,
                ";".join(cand["ref_urls"]) or "-",
                ";".join(cand["teams"][:4]) or "-",
            ]) + "\n")

    # ---------------- report
    print(f"candidates loaded      : {len(cands)}")
    print(f"promoted to entries    : {len(selected)}")
    by_group = {}
    for cand, _, _ in selected:
        by_group[cand["group"]] = by_group.get(cand["group"], 0) + 1
    for g in ("ncaa", "beach", "intl"):
        if by_group.get(g):
            print(f"    {g:<6}: {by_group.get(g, 0)}")
    print(f"sent to review queue   : {len(queued)}")
    rc = {}
    for _, reason in queued:
        rc[reason] = rc.get(reason, 0) + 1
    for r, n in sorted(rc.items()):
        print(f"    {r}: {n}")
    print(f"skipped                : {len(skipped)}")
    sc = {}
    for _, reason in skipped:
        sc[reason] = sc.get(reason, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    print(f"entry range            : W-2026-{next_id - len(selected)} .. W-2026-{next_id - 1}")
    print(f"audit artifact         : {os.path.relpath(AUDIT, ROOT)}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return 0

    catalog["entries"].extend(entry for _, _, entry in selected)
    catalog["reviewQueue"] = rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(rq)
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 14 added {len(selected)} verified profiles from structured-data discovery and "
        f"public-web creator research ({by_group.get('ncaa', 0)} NCAA/US college, "
        f"{by_group.get('beach', 0)} beach, {by_group.get('intl', 0)} international indoor). "
        f"{len(queued)} further candidates were routed to the review queue rather than promoted. "
        f"Follower counts that could not be publicly observed are recorded as {UNKNOWN_COUNT} with "
        f"range {UNKNOWN_RANGE} \u2014 never estimated and never summed across platforms."
    )
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, {len(rq)} review-queue items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
