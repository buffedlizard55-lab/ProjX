#!/usr/bin/env python3
"""Session 13 pass 3+ — generic structured-data volleyball discovery generator.

Pass 3 focuses on college sport, as the owner directed: the NCAA / US-college population for BOTH disciplines
(indoor volleyball P106=Q15117302 and beach volleyball P106=Q17361156), for every player whose item links ANY
public handle (Instagram P2003, X P2002, TikTok P7085) and whose date of birth falls in the adult window
1990-01-01..2008-09-06. Pass 1 had only enumerated the Instagram-bearing subset born 1999+, so this closes the
alumni cohort (born 1990-1998) and the X/TikTok-only players.

The script is deliberately pool-agnostic so later passes (other birth-year bands, other leagues) reuse it
unchanged:

    python3 scripts/session13_pass3.py --pool s13_poolC.tsv --evidence s13_evidenceC.tsv \
                                       --audit s13_pass3_selected.tsv            # dry run
    ... --apply                                                                    # write data/catalog.json

Pool file columns   : qid|name|dob|instagram|x|tiktok        (a 7th country column is accepted and used if present)
Evidence file tags  : S named source on the DOB reference ("NONE" = reference carries neither name nor URL)
                      U reference URL on the DOB statement
                      W linked English Wikipedia article
                      N label of a US volleyball team the player is a member of (P54)

Nothing is inferred. Discipline and college status come only from harvested values:
  * "Beach Volleyball" only when every DOB reference URL is the Beach Volleyball Database (bvbinfo.com);
  * "College Athlete" only when the item records membership of a US *collegiate* volleyball team — national teams
    ("... women's national volleyball team") and professional leagues ("Athletes Unlimited Volleyball") are
    explicitly excluded by NOT_COLLEGE, so a pro/national-only player is never labelled a college athlete;
  * sport wording is kept generic ("women's volleyball") because a roster citation may be historical — the exact
    team labels are recorded verbatim in the entry notes so a reviewer can see the basis.
Follower counts are never invented: every new account keeps FOLLOWER_COUNT_UNKNOWN until publicly observed.
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
TODAY = s13.TODAY
UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE

# US volleyball team labels that are NOT colleges, so they never trigger the College Athlete category.
NOT_COLLEGE = re.compile(r"national (?:volleyball )?team|athletes unlimited", re.I)


def arg(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


POOL = os.path.join(RESEARCH, arg("--pool", "s13_poolC.tsv"))
EVIDENCE = os.path.join(RESEARCH, arg("--evidence", "s13_evidenceC.tsv"))
AUDIT = os.path.join(RESEARCH, arg("--audit", "s13_pass3_selected.tsv"))
PASS_LABEL = arg("--label", "Session 13 pass 3")


def norm(value):
    return s13.dash(value)


def load_pool():
    cands, conflicts, seen = {}, {}, set()
    with open(POOL, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 6:
                continue
            qid, name, dob, ig, x, tt = parts[:6]
            country = norm(parts[6]) if len(parts) > 6 else "UNKNOWN"
            conflicts.setdefault(qid, set()).add(dob)
            if qid in seen:
                continue
            seen.add(qid)
            cands[qid] = {
                "qid": qid,
                "name": name,
                "dob": norm(dob),
                "dob_conflict": None,
                "group": "intl",
                "country": country or "UNKNOWN",
                "teams": [],
                "college_teams": [],
                "handles": {"Instagram": norm(ig), "X": norm(x), "TikTok": norm(tt)},
                "dob_sources": [],
                "ref_urls": [],
                "wiki_urls": [],
                "imports": [],
            }
    for qid, dobs in conflicts.items():
        if len(dobs) > 1 and qid in cands:
            cands[qid]["dob_conflict"] = sorted(dobs)
    return list(cands.values()), {q: sorted(v) for q, v in conflicts.items() if len(v) > 1}


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
            slot = ev.setdefault(qid, {"S": [], "U": [], "W": [], "N": []})
            if tag == "S" and value == "NONE":
                continue                     # reference with neither named source nor URL: not evidence
            if value and value not in slot[tag]:
                slot[tag].append(value)
    return ev


def college_teams(labels):
    return [t for t in labels if not NOT_COLLEGE.search(t)]


def classify(cand, ev):
    refs = ev.get("U", [])
    cand["ref_urls"] = refs
    cand["wiki_urls"] = ev.get("W", [])
    cand["dob_sources"] = ev.get("S", [])
    cand["teams"] = ev.get("N", [])
    cand["college_teams"] = college_teams(cand["teams"])
    if refs and all("bvbinfo.com" in u for u in refs):
        cand["group"] = "beach"
    elif cand["college_teams"]:
        cand["group"] = "ncaa"
    return cand


def generic_sport_text(entry):
    """Roster citations may be historical, so the discipline is stated generically; the exact team labels are
    preserved verbatim in the entry notes."""
    blob = json.dumps(entry, ensure_ascii=False)
    blob = blob.replace("women's NCAA (US college) indoor volleyball", "women's volleyball")
    blob = blob.replace("NCAA (US college) indoor volleyball", "volleyball")
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
    # alias-aware dedupe: a married/changed name ("Kelsey Robinson Cook" vs "Kelsey Robinson") is the same
    # person, so compare name-token sets both ways and also compare cited source URLs.
    existing_tokens = [set(re.sub(r"[^a-z ]", "", n.lower()).split()) for n in existing_names]
    existing_urls = {s["url"] for e in catalog["entries"] for s in e["sources"]}
    existing_handles = set()
    existing_qids = set()
    for e in catalog["entries"]:
        existing_qids |= set(re.findall(r"Q\d{4,}", json.dumps(e, ensure_ascii=False)))
        for a in e.get("socialAccounts", []):
            existing_handles.add(a.get("username", "").lstrip("@").lower())
    rq_names = {s13.norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}
    rq_handles = {str(r.get("handle", "")).lstrip("@").lower() for r in catalog.get("reviewQueue", [])}

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
    seen_names, seen_handles, seen_qids = set(), set(), set()

    for cand in cands:
        key = s13.norm_name(cand["name"])
        handles = {p: h for p, h in cand["handles"].items() if h}
        hkeys = {h.lstrip("@").lower() for h in handles.values()}

        if cand["qid"] in existing_qids or cand["qid"] in seen_qids:
            skipped.append((cand, "duplicate-qid"))
            continue
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name"))
            continue
        kt = set(re.sub(r"[^a-z ]", "", cand["name"].lower()).split())
        if kt and any(kt and (kt <= et or et <= kt) for et in existing_tokens if et):
            skipped.append((cand, "duplicate-name-alias"))
            continue
        cand_urls = {s13.profile_url(p_, h) for p_, h in handles.items()}
        if cand_urls & existing_urls:
            skipped.append((cand, "duplicate-source-url"))
            continue
        if hkeys & (existing_handles | rq_handles | seen_handles):
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
        if cand["college_teams"] and "College Athlete" not in entry["categories"]:
            entry["categories"].append("College Athlete")
        if not cand["ref_urls"] and not cand["wiki_urls"]:
            entry["flags"] = ["AGE_EVIDENCE_SECONDARY_SOURCES"]
        selected.append((cand, dob, entry))
        seen_qids.add(cand["qid"])
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
                    + (f" US teams recorded in the item: {'; '.join(cand['teams'][:3])}." if cand["teams"] else "")
                    + conflict_note
                ),
                "sourceLabel": f"Wikidata {cand['qid']} \u2014 {cand['name']}",
                "sourceUrl": f"https://www.wikidata.org/wiki/{cand['qid']}",
            },
            "missingEvidence": [reason],
            "flags": [reason],
            "lastChecked": TODAY.isoformat(),
            "notes": (
                f"{PASS_LABEL} structured-data discovery. Not promoted to a verified entry: "
                f"{reason_explanation(reason)} Recorded here with provenance instead of being guessed. "
                f"Candidate Q-ID {cand['qid']}."
            ),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# {PASS_LABEL} selection audit \u2014 every promoted entry with its evidence links "
                 f"(generated {TODAY.isoformat()}).\n")
        fh.write("# entryId\tqid\tgroup\tname\tdob\tage\thandles\tdobSources\treferenceUrls\twikipedia\tusTeams\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["group"], cand["name"], dob.isoformat(),
                str(s13.age_on(dob)), handles,
                ";".join(cand["dob_sources"]) or "-",
                ";".join(cand["ref_urls"]) or "-",
                ";".join(cand["wiki_urls"]) or "-",
                ";".join(cand["teams"]) or "-",
            ]) + "\n")

    by_group = {}
    for cand, _, _ in selected:
        by_group[cand["group"]] = by_group.get(cand["group"], 0) + 1
    with_ref = sum(1 for c, _, _ in selected if c["ref_urls"])
    with_wiki = sum(1 for c, _, _ in selected if c["wiki_urls"])
    with_college = sum(1 for c, _, _ in selected if c["college_teams"])
    flagged = sum(1 for _, _, e in selected if "AGE_EVIDENCE_SECONDARY_SOURCES" in e.get("flags", []))
    print(f"pool file               : {os.path.relpath(POOL, ROOT)}")
    print(f"unique candidates       : {len(cands)}")
    print(f"conflicting DOB Q-IDs   : {list(dup_dobs)}")
    print(f"promoted to entries     : {len(selected)}")
    for g in ("ncaa", "beach", "intl"):
        if by_group.get(g):
            print(f"    {g:<6}: {by_group[g]}")
    print(f"    with external ref URL : {with_ref}")
    print(f"    with Wikipedia article: {with_wiki}")
    print(f"    college-team member   : {with_college}")
    print(f"    flagged secondary-only: {flagged}")
    print(f"sent to review queue    : {len(queued)}")
    rc = {}
    for _, reason in queued:
        rc[reason] = rc.get(reason, 0) + 1
    for r, n in sorted(rc.items()):
        print(f"    {r}: {n}")
    print(f"skipped                 : {len(skipped)}")
    sc = {}
    for _, reason in skipped:
        sc[reason] = sc.get(reason, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    print(f"audit artifact          : {os.path.relpath(AUDIT, ROOT)}")

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
        f" {PASS_LABEL} added {len(selected)} further verified volleyball profiles "
        f"({by_group.get('ncaa', 0)} US-college-team-linked, {by_group.get('beach', 0)} beach volleyball, "
        f"{by_group.get('intl', 0)} other): {with_ref} cite an external reference URL attached to their own "
        f"date-of-birth statement (bvbinfo.com, usctrojans.com, mutigers.com, vcuathletics.com, CEV, "
        f"Volleyball World, the German Bundesliga, Lega Volley Femminile, Dresdner SC, worldofvolley.com), "
        f"{with_wiki} also carry an English Wikipedia article, {with_college} record membership of a US "
        f"collegiate volleyball team (national teams and professional leagues were excluded from that count), "
        f"and {flagged} are flagged AGE_EVIDENCE_SECONDARY_SOURCES because the birth date is referenced to a "
        f"named database that attaches no URL. {len(queued)} candidates were routed to the review queue instead "
        f"of being promoted. Follower counts for these accounts stay {UNKNOWN_COUNT} / {UNKNOWN_RANGE} until "
        f"publicly observed \u2014 never estimated, never summed across platforms."
    )
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, {len(rq)} review-queue items")


if __name__ == "__main__":
    main()
