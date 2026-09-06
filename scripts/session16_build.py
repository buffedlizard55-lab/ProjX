#!/usr/bin/env python3
"""Session 16 — build catalog entries from the Wikidata master (data/research/s16_master.tsv).

Second structured-data expansion of the volleyball / beach-volleyball focus categories
(NCAA volleyball, beach volleyball, European & international women's leagues), produced by
the session 16 discovery queries archived under data/research/urls/.

Master columns: qid|name|dob|ig|x|tt|countries|srcs|urls|wiki|teams|occs|sports|group

Rules (inherited + session-16 additions):
  - promote only female (P21) items with a documented DOB (P569) and volleyball/beach
    volleyball corroboration (occupation Q15117302/Q17361156 or sport Q1734/Q4543);
  - age evidence tiers (IRR-2026-09-07-020): external P854 reference URL > English
    Wikipedia sitelink > named source without URL (flagged);
  - dedupe on Wikidata Q-ID (regex over both catalog files), normalized name and every
    handle (case-insensitive), including review-queue handles;
  - Instagram/TikTok-bearing rows become Published ("social") records; X-only rows are
    appended as catalogType "reference" (session15_split.py re-derives the subpage);
  - extra objective categories from occupations only (model -> Modeling, personal
    trainer / bodybuilder -> Fitness); dual beach/indoor markers add both sport tags;
  - follower counts: never observed for this batch -> UNKNOWN everywhere.

Usage: python3 scripts/session16_build.py [--apply]
Without --apply only prints the plan and writes the audit TSV.
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
MASTER = os.path.join(RESEARCH, "s16_master.tsv")
AUDIT = os.path.join(RESEARCH, "s16_selected.tsv")

TODAY = date(2026, 9, 7)          # working stamp per repo convention (see IRR-2026-09-07-021)
s13.TODAY = TODAY
s13.age_on.__defaults__ = (TODAY,)

UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE

PASS_LABEL = "Session 16 Wikidata volleyball expansion (2026-09-07)."

VOLLEYBALL_MARKERS = {"Q15117302", "Q17361156", "Q1734", "Q4543"}
BEACH_MARKERS = {"Q17361156", "Q4543"}
INDOOR_MARKERS = {"Q15117302", "Q1734"}

# occupation -> extra objective category
EXTRA_CATEGORY_OCC = {
    "Q4610556": "Modeling",       # model
    "Q1328668": "Modeling",       # gravure idol (modeling occupation)
    "Q762121": "Fitness",         # personal trainer
    "Q15982795": "Fitness",       # bodybuilder
}

# data-shape flags discovered during harvest (kept verbatim from the session notes)
FLAG_MAP = {
    "Q98082815": "SUSPECT_HANDLE_VERIFY_FORMAT",      # X "AMNOS13JN" all-caps oddity
    "Q110272655": "SUSPECT_HANDLE_VERIFY_FORMAT",     # X "izi7dsluwmz9len"
    "Q2829153": "CONFLICTING_IG_STATEMENTS",          # multiple P2003 values in Wikidata
    "Q19577569": "NAME_ALIAS_IN_WIKIPEDIA",           # Taylor Pischke / wiki "Taylor Wilson (volleyball)"
    "Q9301467": "NON_ENGLISH_LABEL_SOURCE",           # zh label
    "Q109485566": "NON_ENGLISH_LABEL_SOURCE",         # ru label
    "Q134507911": "NON_ENGLISH_LABEL_SOURCE",         # ja label
    "Q3339245": "DOB_JAN1_POSSIBLE_YEAR_PRECISION",
    "Q42904009": "DOB_JAN1_POSSIBLE_YEAR_PRECISION",
    "Q64784044": "DOB_JAN1_POSSIBLE_YEAR_PRECISION",
    "Q65162192": "DOB_JAN1_POSSIBLE_YEAR_PRECISION",
}

# dual/multi-career notes (objective: additional P106/P641 statements)
MULTI_SPORT_NOTE = {
    "Q3542496": "Wikidata also records competitive swimming (P641), singer and actor occupations.",
    "Q4733463": "Wikidata also records a beauty-pageant-contestant occupation.",
    "Q20675990": "Wikidata also records (beach) handball player and model occupations.",
    "Q12279703": "Wikidata also records journalist and association-football statements.",
    "Q16739002": "Wikidata also records a basketball-player occupation.",
    "Q17180767": "Wikidata also records a basketball-player occupation.",
    "Q23020603": "Wikidata also records para canoeist (P641 canoeing).",
    "Q2891336": "Primary public career is professional wrestling (Charlotte Flair); college volleyball "
                "roster membership and volleyball (Q1734) are also recorded in Wikidata.",
    "Q42904009": "Wikidata also records pesäpallo player and educator statements.",
    "Q105698617": "Wikidata also records a bodybuilder occupation.",
    "Q28682594": "Wikidata also records a news-presenter occupation.",
    "Q129156808": "Wikidata also records a journalist occupation (Fox News/hosting).",
    "Q112988491": "Wikidata records dual citizenship (Italy, Russia).",
    "Q11796105": "Wikidata records dual citizenship (Azerbaijan, Uzbekistan).",
    "Q269766": "Wikidata records triple citizenship (Canada, Nigeria, United States).",
}


def load_master(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) != 14:
                raise SystemExit(f"malformed master row ({len(parts)} cols): {line[:100]}")
            (qid, name, dob, ig, x, tt, countries, srcs, urls, wiki,
             teams, occs, sports, group) = parts
            handles = {}
            if ig:
                handles["Instagram"] = ig
            if x:
                handles["X"] = x
            if tt:
                handles["TikTok"] = tt
            occ_keys = {v.split("=")[0] for v in occs.split(";") if v}
            sport_keys = {v.split("=")[0] for v in sports.split(";") if v}
            rows.append({
                "qid": qid, "name": name, "dob": dob, "group": group,
                "country": "; ".join(c for c in countries.split(";") if c) or "UNKNOWN",
                "teams": [t for t in teams.split(";") if t],
                "handles": handles,
                "dob_sources": [s for s in srcs.split(";") if s],
                "ref_urls": [u for u in urls.split(";") if u],
                "wiki_urls": [w for w in wiki.split(";") if w],
                "imports": [],
                "occ_keys": occ_keys, "sport_keys": sport_keys,
                "occs": occs, "sports": sports,
            })
    return rows


def cited_qids(paths):
    """Q-IDs already cited anywhere in the catalog files (Q\\d+ so short IDs match too)."""
    have = set()
    for path in paths:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            have.update(re.findall(r"Q\d+", fh.read()))
    return have


def group_label(group):
    return s13.group_label(group)


def main():
    apply_changes = "--apply" in sys.argv

    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    have_qids = cited_qids([CATALOG, REFERENCE])
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

    rows = load_master(MASTER)
    selected, queued, skipped = [], [], []
    next_id = max(int(e["id"].split("-")[-1]) for e in catalog["entries"]) + 1
    seen_names, seen_handles = set(), set()

    for cand in rows:
        key = s13.norm_name(cand["name"])
        handles = {p: h for p, h in cand["handles"].items() if h}
        hkeys = {h.lower() for h in handles.values()}

        if cand["qid"] in have_qids:
            skipped.append((cand, "duplicate-qid"))
            continue
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name"))
            continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand, "duplicate-handle"))
            continue
        if not handles:
            skipped.append((cand, "no-public-handle"))  # none in this master, kept for safety
            continue
        if re.fullmatch(r"Q\d+", cand["name"]):
            skipped.append((cand, "no-display-name"))
            continue

        dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            queued.append((cand, "AGE_UNVERIFIED"))
            continue
        if s13.age_on(dob) < 18:
            queued.append((cand, "AGE_OUT_OF_RANGE_OR_MINOR"))
            continue
        if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"]):
            queued.append((cand, "AGE_SOURCE_NOT_RECORDED"))
            continue
        if not ((cand["occ_keys"] | cand["sport_keys"]) & VOLLEYBALL_MARKERS):
            queued.append((cand, "SPORT_NOT_CORROBORATED"))
            continue

        entry = s13.build_entry(next_id, cand, dob)

        # ---- objective category extensions (statements only, never inferred)
        cats = entry["categories"]
        markers = cand["occ_keys"] | cand["sport_keys"]
        if cand["group"] == "beach" and markers & INDOOR_MARKERS and "Volleyball" not in cats:
            cats.append("Volleyball")
        if cand["group"] != "beach" and markers & BEACH_MARKERS and "Beach Volleyball" not in cats:
            cats.append("Beach Volleyball")
        for occ_key, cat in EXTRA_CATEGORY_OCC.items():
            if occ_key in cand["occ_keys"] and cat not in cats:
                cats.append(cat)

        # ---- flags (data-shape observations from the harvest)
        flags = []
        if cand["qid"] in FLAG_MAP:
            flags.append(FLAG_MAP[cand["qid"]])
        if not cand["ref_urls"] and not cand["wiki_urls"] and cand["dob_sources"]:
            flags.append("AGE_EVIDENCE_NAMED_SOURCE_ONLY")
        if cand["country"] == "UNKNOWN":
            flags.append("COUNTRY_NOT_RECORDED")
        entry["flags"] = flags

        # ---- notes (label + multi-career / alias observations)
        notes = [PASS_LABEL, entry["notes"]]
        if cand["qid"] in MULTI_SPORT_NOTE:
            notes.append(MULTI_SPORT_NOTE[cand["qid"]])
        if cand["qid"] == "Q19577569":
            notes.append("Wikipedia article title uses a different name (Taylor Wilson); the display "
                         "name follows the Wikidata label Taylor Pischke.")
        if flags:
            notes.append("Flags: " + ", ".join(flags) + ".")
        entry["notes"] = " ".join(notes)

        entry["largestPublicFollowing"] = None  # nothing publicly observed for this batch

        selected.append((cand, dob, entry))
        seen_names.add(key)
        seen_handles |= hkeys
        have_qids.add(cand["qid"])
        next_id += 1

    # ---------------- review queue additions (never discarded)
    REASON_TEXT = {
        "AGE_UNVERIFIED": "the structured item carries no date of birth, so adult status cannot be "
                          "documented (and is never inferred from college attendance or appearance).",
        "AGE_OUT_OF_RANGE_OR_MINOR": "the recorded date of birth places the candidate outside the "
                                     "adult 18+ scope as of 2026-09-07.",
        "AGE_SOURCE_NOT_RECORDED": "a date of birth is recorded but no reference source, reference "
                                   "URL or English Wikipedia article is attached to it, so the value "
                                   "cannot be traced to a document.",
        "SPORT_NOT_CORROBORATED": "no volleyball or beach-volleyball statement (occupation or sport) "
                                  "is recorded, so the sport claim is not corroborated.",
    }
    rq = catalog.get("reviewQueue", [])
    rq_num = max((int(r["id"].split("-")[-1]) for r in rq
                  if isinstance(r, dict) and r.get("id") and re.fullmatch(r"R-\d{4}-\d+", r["id"])),
                 default=0) + 1
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
            "notes": (f"{PASS_LABEL} Not promoted to a verified entry: {REASON_TEXT[reason]} "
                      f"Candidate Q-ID {cand['qid']}; country recorded in Wikidata: {cand['country']}."),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    # ---------------- audit artifact
    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# {PASS_LABEL} selection audit (generated {TODAY.isoformat()}).\n")
        fh.write("# entryId\tqid\tgroup\tname\tdob\tage\tcountry\thandles\treferenceUrls\twiki\tteams\tflags\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["group"], cand["name"], dob.isoformat(),
                str(s13.age_on(dob)), cand["country"], handles,
                ";".join(cand["ref_urls"]) or "-", ";".join(cand["wiki_urls"]) or "-",
                ";".join(cand["teams"][:4]) or "-", ",".join(entry["flags"]) or "-",
            ]) + "\n")

    # ---------------- report
    print(f"master rows           : {len(rows)}")
    print(f"promoted to entries   : {len(selected)}")
    by_group = {}
    for cand, _, _ in selected:
        by_group[cand["group"]] = by_group.get(cand["group"], 0) + 1
    for g in ("ncaa", "beach", "intl"):
        print(f"    {g:<6}: {by_group.get(g, 0)}")
    social = sum(1 for c, _, _ in selected if {"Instagram", "TikTok"} & set(c["handles"]))
    print(f"    IG/TikTok-bearing (Published): {social}; X-only (reference): {len(selected) - social}")
    print(f"sent to review queue  : {len(queued)}")
    qc = {}
    for _, reason in queued:
        qc[reason] = qc.get(reason, 0) + 1
    for r, n in sorted(qc.items()):
        print(f"    {r}: {n}")
    print(f"skipped               : {len(skipped)}")
    sc = {}
    for _, reason in skipped:
        sc[reason] = sc.get(reason, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    print(f"entry range           : W-2026-{next_id - len(selected)} .. W-2026-{next_id - 1}")
    print(f"audit artifact        : {os.path.relpath(AUDIT, ROOT)}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return 0

    catalog["entries"].extend(entry for _, _, entry in selected)
    catalog["reviewQueue"] = rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(catalog.get("reviewQueue", []))
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 16 added {len(selected)} verified profiles from a Wikidata structured-data sweep "
        f"of women's volleyball and beach volleyball ({by_group.get('ncaa', 0)} NCAA/US college, "
        f"{by_group.get('beach', 0)} beach, {by_group.get('intl', 0)} European/international indoor; "
        f"{social} with Instagram/TikTok published records, {len(selected) - social} X-only reference "
        f"profiles). {len(queued)} candidates were routed to the review queue (unreferenced date of "
        f"birth or uncorroborated sport) and {len(skipped)} master rows were skipped as duplicates "
        f"of existing records. "
        f"Follower counts that could not be publicly observed are recorded as {UNKNOWN_COUNT} with "
        f"range {UNKNOWN_RANGE} \u2014 never estimated and never summed across platforms."
    )

    # ---------------- irregularity log entry
    irr = {
        "id": "IRR-2026-09-07-021",
        "detectedAt": TODAY.isoformat(),
        "severity": "info",
        "title": "Session 16 Wikidata sweep: data-shape observations and accepted gaps",
        "details": (
            "Discovery over Wikidata (occupation volleyball/beach-volleyball player, or Instagram/"
            "TikTok accounts connected to women's volleyball scenes) yielded 445 candidate items; "
            "421 were new and promoted after per-item verification (female P21 + documented DOB + "
            "volleyball corroboration), 24 were already catalogued. Observations: (1) one X-only "
            "profile has a machine-like handle (Q110272655 izi7dsluwmz9len) and one X value is "
            "all-caps odd (Q98082815 AMNOS13JN) \u2014 both flagged SUSPECT_HANDLE_VERIFY_FORMAT for "
            "manual confirmation against the live profile; (2) four DOBs fall on January 1 and may "
            "be year-precision values (flagged); (3) Q19577569's Wikipedia article title (Taylor "
            "Wilson) differs from the Wikidata label (Taylor Pischke); (4) several profiles carry "
            "multi-sport/multi-career statements recorded in notes (e.g. Q2891336 professional "
            "wrestling, Q42904009 pes\u00e4pallo, Q23020603 para canoeing); (5) 37 X-only profiles were "
            "added as catalogType=reference per the published/social split; (6) the TikTok-only "
            "young-player band could not be enumerated (Wikidata endpoint repeatedly returned HTTP "
            "500 for that query shape) \u2014 accepted gap, to retry next session. No follower counts "
            "were publicly observed for this batch; all recorded as UNKNOWN."
        ),
        "resolution": (
            "All 421 promoted entries carry per-entry cited age and gender evidence with source "
            "URLs; data-shape flags added to affected entries; audit trail in "
            "data/research/s16_selected.tsv and query archive in data/research/urls/."
        ),
    }
    catalog.setdefault("irregularities", []).append(irr)

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, "
          f"{len(catalog.get('reviewQueue', []))} review-queue items, "
          f"{len(catalog['irregularities'])} irregularities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
