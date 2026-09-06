#!/usr/bin/env python3
"""Session 17 - build catalog entries from the P54 club-roster master (s17_master.tsv).

Promotion rules for this pool (inherited + P54-specific):
  - only rows whose status is "volleyball": member of a volleyball-only club (exactly one
    P641 sport: volleyball/beach volleyball) and no contradicting personal sport statement;
  - display name: English label; if absent, the title of the linked English Wikipedia
    article (flagged NAME_FROM_WIKIPEDIA_TITLE); if neither, skipped (never guessed);
  - age-evidence tiers as IRR-2026-09-07-020 (P854 URL > en-wiki sitelink > named source
    only, flagged); corroborated rows without any evidence -> review queue;
  - cross-sport club artifacts ("umbrella-only", "sport-conflict") stay in the master TSV
    only - they are not volleyball candidates and are NOT queued (would mislabel them);
  - dedupe on Q-ID, normalized name and every handle, as in session 16.

Usage: python3 scripts/session17_build.py [--apply]
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
REFERENCE = os.path.join(ROOT, "data", "catalog-reference.json")
MASTER = os.path.join(RESEARCH, "s17_master.tsv")
AUDIT = os.path.join(RESEARCH, "s17_selected.tsv")

TODAY = date(2026, 9, 7)
s13.TODAY = TODAY
s13.age_on.__defaults__ = (TODAY,)

UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE
PASS_LABEL = "Session 17 P54 club-roster sweep (2026-09-07)."

COLLEGE_RE = re.compile(
    r"aztecs|hoyas|blue hens|mean green|longhorns|titans|wildcats|nittany lions|"
    r"golden bears|blue devils|cardinals|gators|wolverines|rams|red storm|terrapins|"
    r"utes|huskies|gaels|eagles", re.I)

EXTRA_CATEGORY_OCC = {"Q4610556": "Modeling", "Q762121": "Fitness", "Q15982795": "Fitness"}

NOTES_OVERRIDE = {
    "Q16623203": "Wikidata records the occupation as sitting volleyball player (P641 sitting "
                 "volleyball, Q597628) with membership of Lokomotiv Baku; the display name is taken "
                 "from the linked English Wikipedia article title because the item has no English label.",
    "Q458984": "Wikidata occupations recorded: model, actor (film/television) and Playboy Playmate; "
               "roster membership of the San Diego State Aztecs women's volleyball team is recorded "
               "in the same item.",
    "Q56486676": "Wikidata records the occupation politician (US Representative) alongside roster "
                 "membership of the Georgetown Hoyas women's volleyball team.",
}


def load_master():
    rows = []
    with open(MASTER, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("|")
            if len(p) != 14:
                raise SystemExit(f"bad row: {line[:90]}")
            rows.append(p)
    return rows


def main():
    apply_changes = "--apply" in sys.argv
    catalog = json.load(open(CATALOG, encoding="utf-8"))

    have_qids = set()
    for path in (CATALOG, REFERENCE):
        have_qids.update(re.findall(r"Q\d+", open(path, encoding="utf-8").read()))
    existing_names = {s13.norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    rq_names = {s13.norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}
    existing_handles = set()
    for e in catalog["entries"]:
        for a in e.get("socialAccounts", []):
            existing_handles.add(a.get("username", "").lstrip("@").lower())
    for r in catalog.get("reviewQueue", []):
        if r.get("handle"):
            existing_handles.add(r["handle"].lstrip("@").lower())

    rows = load_master()
    by_status = {}
    for r in rows:
        by_status[r[13].split(",")[0]] = by_status.get(r[13].split(",")[0], 0) + 1
    print("master rows by status:", by_status)

    selected, queued, skipped = [], [], []
    next_id = max(int(e["id"].split("-")[-1]) for e in catalog["entries"]) + 1
    seen_names, seen_handles = set(), set()

    for p in rows:
        (qid, name, dob, ig, x, tt, countries, srcs, urls, wiki, teams,
         occs, sports, status) = p
        if not status.startswith("volleyball"):
            continue  # cross-sport / label-less artifacts stay in the master only
        cand = {
            "qid": qid, "name": name, "dob": dob,
            "group": "ncaa" if COLLEGE_RE.search(teams) else "intl",
            "country": "; ".join(c for c in countries.split(";") if c) or "UNKNOWN",
            "teams": [t for t in teams.split(";") if t],
            "handles": {k: v for k, v in (("Instagram", ig), ("X", x), ("TikTok", tt)) if v},
            "dob_sources": [s for s in srcs.split(";") if s],
            "ref_urls": [u for u in urls.split(";") if u],
            "wiki_urls": [w for w in wiki.split(";") if w],
            "imports": [], "occ_keys": {v.split("=")[0] for v in occs.split(";") if v},
        }
        # display name: label, else English-Wikipedia article title (documented, flagged)
        flags = []
        if re.fullmatch(r"Q\d+", cand["name"]):
            wt = cand["wiki_urls"]
            if wt:
                cand["name"] = re.sub(r".*/wiki/", "", wt[0]).replace("_", " ")
                flags.append("NAME_FROM_WIKIPEDIA_TITLE")
            else:
                skipped.append((cand, "no-display-name"))
                continue
        key = s13.norm_name(cand["name"])
        hkeys = {h.lower() for h in cand["handles"].values()}
        if qid in have_qids:
            skipped.append((cand, "duplicate-qid")); continue
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name")); continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand, "duplicate-handle")); continue

        dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            queued.append((cand, "AGE_UNVERIFIED")); continue
        if s13.age_on(dob) < 18:
            queued.append((cand, "AGE_OUT_OF_RANGE_OR_MINOR")); continue
        if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"]):
            queued.append((cand, "AGE_SOURCE_NOT_RECORDED")); continue

        entry = s13.build_entry(next_id, cand, dob)
        cats = entry["categories"]
        if "Q597628" in {v.split("=")[0] for v in sports.split(";") if v}:
            pass  # sitting volleyball already inside the Volleyball group family
        for occ_key, cat in EXTRA_CATEGORY_OCC.items():
            if occ_key in cand["occ_keys"] and cat not in cats:
                cats.append(cat)
        if not cand["ref_urls"] and cand["wiki_urls"]:
            flags.append("AGE_EVIDENCE_WIKIPEDIA_ONLY")
        entry["flags"] = flags
        notes = [PASS_LABEL, entry["notes"]]
        if qid in NOTES_OVERRIDE:
            notes.append(NOTES_OVERRIDE[qid])
        if flags:
            notes.append("Flags: " + ", ".join(flags) + ".")
        entry["notes"] = " ".join(notes)
        entry["largestPublicFollowing"] = None
        selected.append((cand, dob, entry))
        seen_names.add(key); seen_handles |= hkeys; next_id += 1

    # review queue additions (corroborated volleyball rows lacking evidence)
    rq = catalog.get("reviewQueue", [])
    rq_num = max((int(r["id"].split("-")[-1]) for r in rq
                  if isinstance(r, dict) and r.get("id") and re.fullmatch(r"R-\d{4}-\d+", r["id"])),
                 default=0) + 1
    REASON_TEXT = {
        "AGE_UNVERIFIED": "the structured item carries no date of birth.",
        "AGE_OUT_OF_RANGE_OR_MINOR": "the recorded date of birth is outside the adult 18+ scope.",
        "AGE_SOURCE_NOT_RECORDED": "a date of birth is recorded but no reference URL, reference "
                                   "source or English Wikipedia article is attached, so it cannot "
                                   "be traced to a document.",
    }
    for cand, reason in queued:
        handles = {p: h for p, h in cand["handles"].items() if h}
        platform = "Instagram" if "Instagram" in handles else (sorted(handles)[0] if handles else "Instagram")
        handle = handles.get(platform, "")
        rq.append({
            "id": f"R-2026-{rq_num:03d}",
            "displayName": cand["name"],
            "handle": s13.display_handle(platform, handle) if handle else "",
            "platform": platform,
            "profileUrl": s13.profile_url(platform, handle) if handle else "",
            "discoveryCategory": "club-roster volleyball (P54, volleyball-only club)",
            "evidenceFound": {
                "summary": (f"Wikidata item {cand['qid']} records a female member of volleyball-only "
                            f"club(s) {s13.join_sources(cand['teams'][:3])}. Date of birth recorded: "
                            f"{cand['dob'] or 'none'}."),
                "sourceLabel": f"Wikidata {cand['qid']} \u2014 {cand['name']}",
                "sourceUrl": f"https://www.wikidata.org/wiki/{cand['qid']}",
            },
            "missingEvidence": [reason],
            "flags": [reason],
            "lastChecked": TODAY.isoformat(),
            "notes": (f"{PASS_LABEL} Not promoted: {REASON_TEXT[reason]} Candidate Q-ID {cand['qid']}; "
                      f"country recorded in Wikidata: {cand['country']}."),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# {PASS_LABEL} selection audit (generated {TODAY.isoformat()}).\n")
        fh.write("# entryId\tqid\tname\tdob\tage\tcountry\thandles\treferenceUrls\twiki\tteams\tflags\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["name"], dob.isoformat(),
                str(s13.age_on(dob)), cand["country"], handles,
                ";".join(cand["ref_urls"]) or "-", ";".join(cand["wiki_urls"]) or "-",
                ";".join(cand["teams"][:4]) or "-", ",".join(entry["flags"]) or "-",
            ]) + "\n")

    print(f"promoted : {len(selected)}  (ids W-2026-{next_id - len(selected)}..{next_id - 1})")
    for cand, dob, entry in selected:
        print(f"    {entry['id']} {cand['qid']} {cand['name']} age {s13.age_on(dob)} "
              f"[{entry['catalogType'] if 'catalogType' in entry else ''}] flags={entry['flags']}")
    print(f"queued   : {len(queued)} ({[c['qid'] for c, _ in queued]})")
    print(f"skipped  : {len(skipped)} ({[(c['qid'], r) for c, r in skipped]})")

    if not apply_changes:
        print("[dry run] re-run with --apply to write data/catalog.json")
        return 0

    catalog["entries"].extend(e for _, _, e in selected)
    catalog["reviewQueue"] = rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(rq)
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 17 swept the previously invisible P54 club-roster population (female items "
        f"with an Instagram/TikTok handle on a volleyball-team roster but no volleyball "
        f"occupation/sport statement): of 227 candidates, {len(selected)} were verified and "
        f"promoted, {len(queued)} corroborated volleyball rows went to the review queue "
        f"(unreferenced birth dates), 13 volleyball-only-club members lack an English label "
        f"(retained in data/research/s17_master.tsv, never guessed) and the remaining 210 are "
        f"cross-sport or multi-sport-umbrella artifacts kept in the master file only."
    )
    irr = {
        "id": "IRR-2026-09-07-022",
        "detectedAt": TODAY.isoformat(),
        "severity": "info",
        "title": "Session 17 P54 club-roster sweep: umbrella-club contamination quantified and excluded",
        "details": (
            "The session-16 sweeps enumerated female volleyball/beach-volleyball players by their own "
            "occupation/sport statements, so a second population remained invisible: items with an "
            "Instagram or TikTok handle whose only volleyball signal is membership (P54) of a team that "
            "plays volleyball. Querying that graph returned 227 new candidates (none previously cited). "
            "Resolving every team item showed the population is heavily contaminated by multi-sport "
            "umbrellas (university athletics programs, omnisport clubs): only 29 of the 133 distinct "
            "team items are volleyball-only (exactly one P641 sport). 202 candidates were members of "
            "umbrella clubs only ( NCAA university programs, Fenerbahce/Flamengo/USC-style omnisport "
            "clubs, German TSVs) and 8 had contradicting personal sports (e.g. Elena Delle Donne "
            "basketball Q2113902, Neta Rivkin rhythmic gymnastics Q640908, Alicja Slezak handball "
            "Q107332975, Joo Seung-eun cheerleader-for-a-volleyball-team Q129755125) - all retained in "
            "data/research/s17_master.tsv but not catalogued and not queued, because they are not "
            "volleyball candidates. 13 further members of volleyball-only clubs (mostly the Belarusian "
            "Zhemchuzhina Polessia / Pribuzhie / Atlant / Minchanka roster cohort) have no English "
            "label, so no display name can be recorded without guessing - retained in the master for a "
            "future label pass. Q97721439 (Hanna Boubezari) is flagged as an identity conflict: the "
            "item claims both the Algeria women's national volleyball team and an association-football "
            "occupation with a Soccerdonna reference. Two corroborated rows were routed to the review "
            "queue (Q110269996 Alina Ilyuta, Q11500637 Mayumi Saito) - birth dates without references. "
            "Process note: one fetch failed with HTTP 400 because the query URL was hand-retyped "
            "(malformed percent-encoding); URLs are always copied programmatically from the archived "
            ".url files, and the earlier det-template parenthesis bug was caught by a paren-balance "
            "assertion before fetching."
        ),
        "resolution": (
            "3 entries promoted with full cited evidence (Summer Altice W-2026-1186, Whitney Dosty "
            "W-2026-1187 - display name from the linked English Wikipedia article title, flagged - "
            "and Lori Trahan W-2026-1188); 2 review-queue rows; full audit in data/research/"
            "s17_selected.tsv and data/research/s17_master.tsv."
        ),
    }
    catalog.setdefault("irregularities", []).append(irr)
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"applied: {len(catalog['entries'])} entries, {len(rq)} review, "
          f"{len(catalog['irregularities'])} irregularities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
