#!/usr/bin/env python3
"""Session 13 pass 2 — structured-data volleyball discovery, birth-year band 1996-1999.

Pass 1 (scripts/session13_volleyball.py) enumerated three pools built around *Instagram handles*
plus specific league/NCAA filters. Pass 2 closes an honest gap in that sweep: every female
volleyball player whose birth year falls in 1996-1999 and who has **any** public handle
(Instagram P2003, X P2002 or TikTok P7085), regardless of league or country.

Discovery query   : data/research/urls/poolB1.url   -> data/research/s13_poolB1.tsv   (188 unique Q-IDs)
Evidence queries  : data/research/urls/evB1.url, evB2.url -> data/research/s13_evidenceB.tsv
                    S = named source attached to the date-of-birth reference (P248)
                    U = reference URL attached to the date-of-birth statement (P854)
                    W = English Wikipedia article linked to the item
                    "NONE" = a reference exists but carries neither a named source nor a URL
                             -> NOT age evidence (candidate goes to the review queue)

Nothing here is inferred: names, dates, handles, reference URLs, Wikipedia links and country
labels are all transcribed verbatim from the two archived query results. Follower counts are
never invented — every new account keeps FOLLOWER_COUNT_UNKNOWN until publicly observed.

Usage:  python3 scripts/session13_pass2.py            (dry run, writes the audit sheet)
        python3 scripts/session13_pass2.py --apply     (writes data/catalog.json)
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session13_volleyball as s13  # noqa: E402  (reuses the pass-1 entry builders verbatim)

ROOT = s13.ROOT
RESEARCH = os.path.join(ROOT, "data", "research")
CATALOG = s13.CATALOG
POOL = os.path.join(RESEARCH, "s13_poolB1.tsv")
EVIDENCE = os.path.join(RESEARCH, "s13_evidenceB.tsv")
AUDIT = os.path.join(RESEARCH, "s13_pass2_selected.tsv")
TODAY = s13.TODAY
UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE

def load_pool():
    """qid -> candidate; flags Q-IDs whose item carries two different dates of birth."""
    rows, conflicts = [], {}
    with open(POOL, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 7:
                continue
            qid, name, dob, ig, x, tt, country = parts[:7]
            rows.append((qid, name, dob, ig, x, tt, country))
            conflicts.setdefault(qid, []).append(dob)
    dup_dobs = {q: sorted(set(v)) for q, v in conflicts.items() if len(set(v)) > 1}

    cands = {}
    for qid, name, dob, ig, x, tt, country in rows:
        if qid in cands:
            continue
        cands[qid] = {
            "qid": qid,
            "name": name,
            "dob": s13.dash(dob),
            "dob_conflict": dup_dobs.get(qid),
            "group": "intl",
            "country": s13.dash(country) or "UNKNOWN",
            "teams": [],
            "handles": {"Instagram": s13.dash(ig), "X": s13.dash(x), "TikTok": s13.dash(tt)},
            "dob_sources": [],
            "ref_urls": [],
            "wiki_urls": [],
            "imports": [],
        }
    return list(cands.values()), dup_dobs


def load_evidence():
    ev = {}
    with open(EVIDENCE, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            qid, tag, value = parts[0], parts[1], parts[2]
            slot = ev.setdefault(qid, {"S": [], "U": [], "W": [], "NONE": False})
            if tag == "S" and value == "NONE":
                slot["NONE"] = True          # a reference with no named source and no URL
                continue
            if value and value not in slot[tag]:
                slot[tag].append(value)
    return ev


def classify(cand, ev):
    refs = ev.get("U", [])
    cand["ref_urls"] = refs
    cand["wiki_urls"] = ev.get("W", [])
    cand["dob_sources"] = ev.get("S", [])
    if refs and all("bvbinfo.com" in u for u in refs):
        # every age reference points at the Beach Volleyball Database -> beach discipline
        cand["group"] = "beach"
    return cand


def generic_sport_text(entry):
    """Pass 2 does not harvest league/team rosters, so the discipline is stated generically."""
    blob = json.dumps(entry, ensure_ascii=False)
    blob = blob.replace("women's indoor volleyball", "women's volleyball")
    blob = blob.replace("indoor volleyball", "volleyball")
    return json.loads(blob)


def reason_explanation(reason):
    if reason == "AGE_CONFLICTING_VALUES":
        return ("the structured item records two different dates of birth and no source settles which is "
                "correct, so no single value is promoted and nothing is guessed.")
    return s13.reason_explanation(reason)


def main():
    apply_changes = "--apply" in sys.argv
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    existing_names = {s13.norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    existing_handles = set()
    blob_by_entry = {}
    for e in catalog["entries"]:
        blob_by_entry[e["id"]] = json.dumps(e, ensure_ascii=False)
        for a in e.get("socialAccounts", []):
            existing_handles.add(a.get("username", "").lstrip("@").lower())
    existing_qids = set()
    for blob in blob_by_entry.values():
        existing_qids |= set(re.findall(r"Q\d{4,}", blob))
    rq_names = {s13.norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}

    entry_nums = [int(m.group(1)) for e in catalog["entries"]
                  for m in [re.match(r"W-2026-(\d+)$", str(e.get("id", "")))] if m]
    next_id = (max(entry_nums) + 1) if entry_nums else len(catalog["entries"]) + 1
    rq_nums = [int(m.group(1)) for r in catalog.get("reviewQueue", [])
               for m in [re.match(r"R-2026-(\d+)$", str(r.get("id", "")))] if m]
    rq_num = (max(rq_nums) + 1) if rq_nums else len(catalog.get("reviewQueue", [])) + 1

    cands, dup_dobs = load_pool()
    ev_all = load_evidence()
    cands = [classify(c, ev_all.get(c["qid"], {})) for c in cands]

    selected, queued, skipped = [], [], []
    seen_names, seen_handles = set(), set()

    for cand in cands:
        key = s13.norm_name(cand["name"])
        handles = {p: h for p, h in cand["handles"].items() if h}
        hkeys = {h.lstrip("@").lower() for h in handles.values()}

        if cand["qid"] in existing_qids:
            skipped.append((cand, "duplicate-qid"))
            continue
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name"))
            continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand, "duplicate-handle"))
            continue
        if not handles:
            skipped.append((cand, "no-public-handle"))
            continue
        if cand["dob_conflict"]:
            queued.append((cand, "AGE_CONFLICTING_VALUES"))
            continue

        dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            queued.append((cand, "AGE_UNVERIFIED"))
            continue
        if dob < s13.MIN_DOB or s13.age_on(dob) < 18:
            queued.append((cand, "AGE_OUT_OF_RANGE_OR_MINOR"))
            continue
        if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"]):
            queued.append((cand, "AGE_SOURCE_NOT_RECORDED"))
            continue

        entry = s13.build_entry(next_id, cand, dob)
        if cand["group"] != "beach":
            entry = generic_sport_text(entry)
        if not cand["ref_urls"] and not cand["wiki_urls"]:
            entry["flags"] = ["AGE_EVIDENCE_SECONDARY_SOURCES"]
        selected.append((cand, dob, entry))
        seen_names.add(key)
        seen_handles |= hkeys
        next_id += 1

    rq = catalog.get("reviewQueue", [])
    for cand, reason in queued:
        handles = {p: h for p, h in cand["handles"].items() if h}
        platform = "Instagram" if "Instagram" in handles else sorted(handles)[0]
        handle = handles[platform]
        conflict_note = ""
        if reason == "AGE_CONFLICTING_VALUES":
            conflict_note = (f" The item carries two dates of birth ({' and '.join(cand['dob_conflict'])}); "
                             f"neither is promoted until a primary document settles it.")
        rq.append({
            "id": f"R-2026-{rq_num:03d}",
            "displayName": cand["name"],
            "handle": s13.display_handle(platform, handle),
            "platform": platform,
            "profileUrl": s13.profile_url(platform, handle),
            "discoveryCategory": s13.group_label(cand["group"]),
            "evidenceFound": {
                "summary": (
                    f"Wikidata item {cand['qid']} records the athlete as a female volleyball player. "
                    f"Date of birth recorded: {cand['dob'] or 'none'}."
                    + (f" Reference URLs attached to that statement: {'; '.join(cand['ref_urls'][:2])}."
                       if cand["ref_urls"] else "")
                    + (f" English Wikipedia article: {cand['wiki_urls'][0]}." if cand["wiki_urls"] else "")
                    + conflict_note
                ),
                "sourceLabel": f"Wikidata {cand['qid']} \u2014 {cand['name']}",
                "sourceUrl": f"https://www.wikidata.org/wiki/{cand['qid']}",
            },
            "missingEvidence": [reason],
            "flags": [reason],
            "lastChecked": TODAY.isoformat(),
            "notes": (
                f"Session 13 pass 2 (birth-year band 1996-1999, any public handle). Not promoted to a "
                f"verified entry: {reason_explanation(reason)} Recorded here with provenance instead of "
                f"being guessed. Candidate Q-ID {cand['qid']}; country recorded in Wikidata: "
                f"{cand['country']}."
            ),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write("# Session 13 pass 2 selection audit \u2014 every promoted entry with its evidence links "
                 "(generated 2026-09-06).\n")
        fh.write("# entryId\tqid\tgroup\tname\tdob\tage\tcountry\thandles\tdobSources\treferenceUrls\twikipedia\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["group"], cand["name"], dob.isoformat(),
                str(s13.age_on(dob)), cand["country"], handles,
                ";".join(cand["dob_sources"]) or "-",
                ";".join(cand["ref_urls"]) or "-",
                ";".join(cand["wiki_urls"]) or "-",
            ]) + "\n")

    print(f"pool B1 unique candidates : {len(cands)}")
    print(f"conflicting DOB Q-IDs     : {list(dup_dobs)}")
    print(f"promoted to entries       : {len(selected)}")
    with_ref = sum(1 for c, _, _ in selected if c["ref_urls"])
    with_wiki = sum(1 for c, _, _ in selected if c["wiki_urls"])
    flagged = sum(1 for _, _, e in selected if "AGE_EVIDENCE_SECONDARY_SOURCES" in e.get("flags", []))
    print(f"    with external ref URL : {with_ref}")
    print(f"    with Wikipedia article: {with_wiki}")
    print(f"    flagged secondary-only: {flagged}")
    print(f"sent to review queue      : {len(queued)}")
    rc = {}
    for _, reason in queued:
        rc[reason] = rc.get(reason, 0) + 1
    for r, n in sorted(rc.items()):
        print(f"    {r}: {n}")
    print(f"skipped (duplicates etc)  : {len(skipped)}")
    sc = {}
    for _, reason in skipped:
        sc[reason] = sc.get(reason, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    print(f"audit artifact            : {os.path.relpath(AUDIT, ROOT)}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return

    catalog["entries"].extend(entry for _, _, entry in selected)
    catalog["reviewQueue"] = rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(rq)
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 13 pass 2 added {len(selected)} further verified volleyball profiles from the "
        f"birth-year band 1996-1999 across every league and country whose structured item links a public "
        f"Instagram, X or TikTok handle: {with_ref} cite an external reference URL attached to their own "
        f"date-of-birth statement (CEV, FIVB/Volleyball World, the German Bundesliga, Lega Volley "
        f"Femminile, the Slovak, Greek, Turkish, Dutch, Belarusian, Japanese, Peruvian and Brazilian "
        f"federations, olympic.ca, university athletics rosters, women.volleybox.net, bvbinfo.com, "
        f"worldofvolley.com), {with_wiki} also carry an English Wikipedia article, and {flagged} are "
        f"flagged AGE_EVIDENCE_SECONDARY_SOURCES because the birth date is referenced to a named database "
        f"that attaches no URL. {len(queued)} candidates were routed to the review queue instead of being "
        f"promoted (including one whose item records two conflicting dates of birth). Follower counts for "
        f"these new accounts stay {UNKNOWN_COUNT} / {UNKNOWN_RANGE} until publicly observed \u2014 never "
        f"estimated, never summed across platforms."
    )
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, {len(rq)} review-queue items")


if __name__ == "__main__":
    main()
