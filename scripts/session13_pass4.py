#!/usr/bin/env python3
"""Session 13 pass 4 — international birth-year bands, the X/TikTok-only cohort, and a review-queue re-test.

Passes 1-3 enumerated (a) NCAA / US-college volleyball for both disciplines and (b) the Instagram-bearing
international population. Pass 4 closes three remaining structured-data populations and then re-tests the
backlog, so nothing is left to age unexamined:

  pool D  data/research/s13_poolD.tsv  female volleyball/beach-volleyball players (P106), DOB 2000-2002, ANY of
                                       Instagram/X/TikTok, no country or league restriction  (188 rows / 184 Q-IDs)
  pool E  data/research/s13_poolE.tsv  the gap population: sport (P641) = volleyball or beach volleyball but NO
                                       occupation statement, DOB 1998-2005, any handle        (14 rows / 13 Q-IDs)
  pool F  data/research/s13_poolF.tsv  the X-only / TikTok-only cohort: P106 volleyball/beach, DOB 1990-2005,
                                       FILTER NOT EXISTS Instagram                            (69 rows)
  pool G  data/research/s13_poolG.tsv  the 52 reviewQueue items that carry a Q-ID, re-harvested (53 rows)

Evidence (data/research/s13_evidenceD.tsv) was harvested for the union of the new candidates and the backlog
(122 Q-IDs) in one query, so both are judged by the same standard:

  S  named source on the date-of-birth reference ("NONE" = reference carries neither name nor URL -> not evidence)
  U  reference URL on the date-of-birth statement
  W  English Wikipedia article linked to the item
  N  label of a US volleyball team the player is a member of (P54 + P17=Q30) -> college-team documentation only

Promotion rule (docs/verification-protocol.md §92-94): a candidate is promoted when the recorded date of birth is
traceable — a named source (S), a reference URL (U) or a linked English Wikipedia article (W). S-only promotions
carry the flag AGE_EVIDENCE_SECONDARY_SOURCES exactly as the protocol requires. Everything else is queued.

Two pass-4 rules are new and are applied only from harvested values, never from assumption:

1. SPORT_NOT_CORROBORATED — pool E selects on a sport statement alone, and three of its items (Q29017817 Risa
   Watanabe, Q54867512 Nao Kosaka, Q98480727 Hono Tamura) reference their date of birth only to a Japanese
   idol-group agency page (sakurazaka46.com / hinatazaka46.com); Q20895315 Maya Jansen references hers only to a
   college TENNIS roster (collegetennisonline.com). Where every reference URL belongs to a domain that is
   demonstrably not a volleyball source, the sport claim is not corroborated by any volleyball document, so the
   candidate is queued for human review instead of being catalogued as a volleyball athlete.
2. Both disciplines — where the reference URLs include the Beach Volleyball Database (bvbinfo.com) AND at least one
   other source, or where a beach-only record is combined with a US collegiate team, the entry carries BOTH
   "Volleyball" and "Beach Volleyball" (the same correction applied by hand to W-2026-101 in pass 3).

Handles are recorded verbatim. Three X values look like machine identifiers rather than chosen handles; they are
kept exactly as the structured record states them and flagged SUSPECT_HANDLE_SHAPE for review, never "corrected".
Follower counts are never invented: every account stays FOLLOWER_COUNT_UNKNOWN until publicly observed.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
import urllib.parse
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session13_volleyball as s13  # noqa: E402
import session13_pass3 as p3        # noqa: E402  (reuses the pass-3 pool/evidence loaders and classifier)

ROOT = s13.ROOT
RESEARCH = os.path.join(ROOT, "data", "research")
CATALOG = s13.CATALOG
UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE

# Passes 1-3 were harvested and stamped 2026-09-06. Pass 4 ran after that session boundary, so its own records are
# stamped with the date the evidence was actually harvested — 2026-09-07 — rather than inheriting yesterday's date.
# This is not cosmetic: three candidates in this pass have 7 September birthdays, so the recorded age differs by a
# year depending on the stamp (W-2026-704 Jimena Fernández Gayoso, born 2001-09-07, is 25 on 2026-09-07 and would
# have been written as 24). Ages are computed as of the stamp actually recorded on the entry.
TODAY = date(2026, 9, 7)
s13.TODAY = TODAY
s13.age_on.__defaults__ = (TODAY,)


def arg(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


NEW_POOL = os.path.join(RESEARCH, arg("--new", "s13_pass4_new.tsv"))
BACKLOG_POOL = os.path.join(RESEARCH, arg("--backlog", "s13_poolG.tsv"))
EVIDENCE = os.path.join(RESEARCH, arg("--evidence", "s13_evidenceD.tsv"))
AUDIT = os.path.join(RESEARCH, arg("--audit", "s13_pass4_selected.tsv"))
PASS_LABEL = arg("--label", "Session 13 pass 4 (international bands 2000-2002, sport-only gap population, "
                            "X/TikTok-only cohort, review-queue re-test)")

# Domains that are demonstrably NOT volleyball sources (reviewed individually against the harvested reference URL):
#   collegetennisonline.com — US college TENNIS rosters
#   sakurazaka46.com / hinatazaka46.com — Japanese idol-group artist pages
NON_SPORT_HOSTS = {"collegetennisonline.com", "sakurazaka46.com", "hinatazaka46.com"}

# Domains that are legitimate public pages but establish nothing about THIS athlete's identity: a national legal
# gazette publishes name/record-correction notices for anyone, so a date-of-birth reference that points only at one
# does not tie the value to the volleyball player in the item. Reviewed by hand: ilan.gov.tr (Turkish official
# gazette) is the reference on Q61667862 (Ezgi Kara) — a court notice "on the correction of a population record",
# which is also the unresolved FLAG carried by reviewQueue item R-2026-024 from an earlier pass. Such a candidate is
# queued AGE_SOURCE_IDENTITY_UNRESOLVED instead of being promoted on a value that may belong to a namesake.
NON_IDENTITY_HOSTS = {"ilan.gov.tr"}

# Candidates that were PROMOTED by this generator and then withdrawn by a human spot-check of the cited primary
# page. Recorded here so that re-running the script cannot silently undo the finding: they are routed to the review
# queue with the reason that was established by opening the page. Each entry cites the exact page and what it said.
#
# Q64784055 was generated as W-2026-730 ("Yurika Yokoishi", DOB 1991-09-16, X @byurika) on the strength of the
# single reference URL attached to its birth-date statement. Opening that URL on 2026-09-07 showed a Volleyball
# Bundesliga player profile titled "Bamba, Yurika" (Date of birth Sep 16, 1991; Nationality Japan; Libero; VfB
# Suhl LOTTO Thueringen 2022/23-2023/24, SC Potsdam 2024/25, Allianz MTV Stuttgart 2025/26). Birth date and
# nationality match exactly; the family name does not. A matching birth date on a differently-named page is NOT
# proof of identity — the two may well be the same person (a family-name change on marriage is common), but
# nothing held here establishes it, so the record went to reviewQueue R-2026-096 with BOTH names preserved
# (neither discarded, merged nor replaced, and no third form invented) and the entry ID range was renumbered.
MANUAL_WITHDRAWALS = {
    "Q64784055": (
        "NAME_MISMATCH_IN_CITED_SOURCE",
        "spot-check 2026-09-07: the only reference URL attached to the recorded date of birth "
        "(https://www.volleyball-bundesliga.de/popup/teamMember/teamMemberDetails.xhtml?teamMemberId=771899351) "
        "serves a Volleyball Bundesliga player profile titled \"Bamba, Yurika\" — Date of birth Sep 16, 1991, "
        "Nationality Japan, Libero — while the structured record labels the item \"Yurika Yokoishi\". The birth "
        "date and nationality match, the family name does not, and no source held here links the two names to one "
        "person. This candidate was promoted by an earlier run of this script and withdrawn before commit.",
    ),
}

# X (P2002) values whose shape suggests a machine identifier rather than a chosen handle. Recorded verbatim and
# flagged, never rewritten. Each was reviewed by hand against the harvested row.
SUSPECT_HANDLES = {
    "Q97901120": ("X", "PH3H6ggKTnWGLYZ", "15 characters mixing upper/lower case and digits; shape of a "
                                           "machine-generated channel identifier rather than a chosen handle"),
    "Q109596239": ("X", "mnynMmE565SNojT", "15 characters mixing upper/lower case and digits; shape of a "
                                            "machine-generated channel identifier rather than a chosen handle"),
    "Q110272655": ("X", "izi7dsluwmz9len", "15 characters with embedded digits and no separator; shape of a "
                                           "machine-generated identifier rather than a chosen handle"),
}


def reason_explanation(reason):
    if reason == "SPORT_NOT_CORROBORATED":
        return ("every reference URL attached to the recorded date of birth belongs to a domain that is not a "
                "volleyball source, so the sport claim is not corroborated by any volleyball document and the "
                "profile is not catalogued as a volleyball athlete.")
    if reason == "AGE_SOURCE_IDENTITY_UNRESOLVED":
        return ("the only reference attached to the recorded date of birth is a general public notice (a national "
                "legal gazette) that documents a record correction for a name, not this athlete, so the value "
                "cannot be tied to the person in the item and may belong to a namesake.")
    if reason == "NAME_MISMATCH_IN_CITED_SOURCE":
        return ("the primary page cited for the recorded date of birth was opened by hand and it names a different "
                "person from the structured record (birth date and nationality match, the name does not), so the "
                "identity is not established and the record is held for human review rather than published as "
                "verified. Both names are preserved; nothing was merged, discarded or invented.")
    if reason == "AGE_CONFLICTING_VALUES":
        return ("the structured item records two different dates of birth and no source settles which is "
                "correct, so no single value is promoted and nothing is guessed.")
    return s13.reason_explanation(reason)


def load_pool(path):
    p3.POOL = path
    return p3.load_pool()


def sport_corroborated(cand):
    """False only when the item HAS reference URLs and every one of them is a non-volleyball domain."""
    refs = cand["ref_urls"]
    if not refs:
        return True
    return not all(s13.host_of(u) in NON_SPORT_HOSTS for u in refs)


def identity_resolved(cand):
    """False only when the item HAS reference URLs and every one of them is a general public notice that says
    nothing about this athlete's identity (see NON_IDENTITY_HOSTS)."""
    refs = cand["ref_urls"]
    if not refs:
        return True
    return not all(s13.host_of(u) in NON_IDENTITY_HOSTS for u in refs)


def non_sport_refs(cand):
    return [u for u in cand["ref_urls"]
            if s13.host_of(u) in NON_SPORT_HOSTS or s13.host_of(u) in NON_IDENTITY_HOSTS]


def both_disciplines(cand):
    refs = cand["ref_urls"]
    beach = [u for u in refs if "bvbinfo.com" in u]
    if beach and len(beach) != len(refs):
        return True, beach
    if cand["group"] == "beach" and cand["college_teams"]:
        return True, beach
    return False, beach


def wiki_title(url):
    tail = url.rstrip("/").split("/wiki/")[-1]
    return urllib.parse.unquote(tail).replace("_", " ")


def flatten(s):
    """Diacritic-insensitive comparison key, so 'Riho Ōtake' and the article title 'Riho Otake' are recognised as
    the same name and only a genuine alias (e.g. Mabel Olemar / Katherinne Olemar) is flagged."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("\u0130", "i").replace("\u0131", "i").replace("\u00f8", "o").replace("\u00d8", "O")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def apply_pass4_rules(cand, entry):
    """Categories, flags and notes that pass 4 adds on top of the shared pass-1 entry builder."""
    mixed, beach_refs = both_disciplines(cand)
    if mixed:
        cats = entry["categories"]
        if "Volleyball" not in cats:
            cats.insert(1, "Volleyball")
        if "Beach Volleyball" not in cats:
            cats.insert(cats.index("Volleyball") + 1, "Beach Volleyball")
        entry["notes"] += (
            " Both disciplines are evidenced: the Beach Volleyball Database (bvbinfo.com) is cited by the "
            f"date-of-birth reference ({'; '.join(beach_refs)}) alongside at least one non-beach source, so the "
            "entry carries both \"Volleyball\" and \"Beach Volleyball\" rather than assuming one discipline."
        )
    suspect = SUSPECT_HANDLES.get(cand["qid"])
    if suspect:
        platform, value, why = suspect
        if cand["handles"].get(platform) == value:
            entry["flags"].append("SUSPECT_HANDLE_SHAPE")
            entry["notes"] += (
                f" Handle caution: the {platform} value recorded in Wikidata {cand['qid']} is \"{value}\" "
                f"({why}). It is reproduced verbatim as the structured record states it and was not rewritten or "
                "guessed; a reviewer should confirm the profile before the link is treated as live."
            )
    if cand["wiki_urls"]:
        title = wiki_title(cand["wiki_urls"][0])
        if flatten(title) != flatten(cand["name"]):
            entry["flags"].append("NAME_ALIAS_IN_WIKIPEDIA")
            entry["notes"] += (
                f" Name alias: the linked English Wikipedia article is titled \"{title}\" while the structured "
                f"record labels the item \"{cand['name']}\". Both forms are recorded; neither was discarded and no "
                "third form was invented."
            )
    return entry


def queue_row(cand, reason, rq_num, extra_note=""):
    handles = {p: h for p, h in cand["handles"].items() if h}
    platform = "Instagram" if "Instagram" in handles else sorted(handles)[0]
    handle = handles[platform]
    conflict_note = ""
    if reason == "AGE_CONFLICTING_VALUES":
        conflict_note = (f" The item carries two dates of birth ({' and '.join(cand['dob_conflict'])}); "
                         f"neither is promoted until a primary document settles it.")
    if reason == "SPORT_NOT_CORROBORATED":
        conflict_note = (" The only reference URLs attached to the date of birth are "
                         f"{'; '.join(non_sport_refs(cand))}, which are not volleyball sources.")
    if reason == "AGE_SOURCE_IDENTITY_UNRESOLVED":
        conflict_note = (" The only reference URL attached to the date of birth is "
                         f"{'; '.join(non_sport_refs(cand))}, a general public notice that documents a record "
                         "correction for a name rather than for this athlete, so the value may belong to a "
                         "namesake and is not promoted.")
    if reason == "NAME_MISMATCH_IN_CITED_SOURCE":
        conflict_note = (" " + MANUAL_WITHDRAWALS[cand["qid"]][1])
    return {
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
                + (f" Named source(s) on that statement: {'; '.join(cand['dob_sources'][:3])}."
                   if cand["dob_sources"] else "")
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
            f"Candidate Q-ID {cand['qid']}.{extra_note}"
        ),
        "followerCountDisplay": UNKNOWN_COUNT,
        "followerCountNumeric": None,
        "followerCountCheckedAt": TODAY.isoformat(),
        "followerSizeRange": UNKNOWN_RANGE,
    }


def evaluate(cand, existing, seen):
    """Return (decision, reason) where decision is 'promote', 'queue' or 'skip'."""
    key = s13.norm_name(cand["name"])
    handles = {p: h for p, h in cand["handles"].items() if h}
    hkeys = {h.lstrip("@").lower() for h in handles.values()}
    if cand["qid"] in existing["qids"] or cand["qid"] in seen["qids"]:
        return "skip", "duplicate-qid"
    if key in existing["names"] or key in seen["names"]:
        return "skip", "duplicate-name"
    kt = set(re.sub(r"[^a-z ]", "", cand["name"].lower()).split())
    if kt and any(kt and (kt <= et or et <= kt) for et in existing["tokens"] if et):
        return "skip", "duplicate-name-alias"
    cand_urls = {s13.profile_url(pl, h) for pl, h in handles.items()}
    if cand_urls & existing["urls"]:
        return "skip", "duplicate-source-url"
    if hkeys & (existing["handles"] | seen["handles"]):
        return "skip", "duplicate-handle"
    if not handles:
        return "skip", "no-public-handle"
    if cand["qid"] in MANUAL_WITHDRAWALS:
        # A human spot-check already opened this candidate's cited primary page and found it does not support the
        # identity. Queued, never promoted — see the MANUAL_WITHDRAWALS comment for the page and what it said.
        return "queue", MANUAL_WITHDRAWALS[cand["qid"]][0]
    if cand["dob_conflict"]:
        return "queue", "AGE_CONFLICTING_VALUES"
    dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
    if dob is None:
        return "queue", "AGE_UNVERIFIED"
    if dob < s13.MIN_DOB or s13.age_on(dob) < 18:
        return "queue", "AGE_OUT_OF_RANGE_OR_MINOR"
    if not sport_corroborated(cand):
        return "queue", "SPORT_NOT_CORROBORATED"
    if not identity_resolved(cand):
        return "queue", "AGE_SOURCE_IDENTITY_UNRESOLVED"
    if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"]):
        return "queue", "AGE_SOURCE_NOT_RECORDED"
    return "promote", dob


def main():
    apply_changes = "--apply" in sys.argv
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    existing = {
        "names": {s13.norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")},
        "tokens": [],
        "urls": {s["url"] for e in catalog["entries"] for s in e["sources"]},
        "handles": set(),
        "qids": set(),
    }
    existing["tokens"] = [set(re.sub(r"[^a-z ]", "", n.lower()).split()) for n in existing["names"]]
    for e in catalog["entries"]:
        existing["qids"] |= set(re.findall(r"Q\d{4,}", json.dumps(e, ensure_ascii=False)))
        for a in e.get("socialAccounts", []):
            existing["handles"].add(a.get("username", "").lstrip("@").lower())

    rq = catalog.get("reviewQueue", [])
    rq_by_qid, rq_by_name = {}, {}
    for item in rq:
        rid = item.get("id") or item.get("queueId")
        for q in re.findall(r"Q\d{4,}", json.dumps(item, ensure_ascii=False)):
            rq_by_qid.setdefault(q, (rid, item))
        if item.get("displayName"):
            rq_by_name.setdefault(s13.norm_name(item["displayName"]), (rid, item))

    entry_nums = [int(m.group(1)) for e in catalog["entries"]
                  for m in [re.match(r"W-2026-(\d+)$", str(e.get("id", "")))] if m]
    next_id = (max(entry_nums) + 1) if entry_nums else len(catalog["entries"]) + 1
    rq_nums = [int(m.group(1)) for r in rq for m in [re.match(r"R-2026-(\d+)$", str(r.get("id", "")))] if m]
    rq_num = (max(rq_nums) + 1) if rq_nums else len(rq) + 1

    p3.EVIDENCE = EVIDENCE
    ev_all = p3.load_evidence()

    new_cands, new_conflicts = load_pool(NEW_POOL)
    backlog_cands, backlog_conflicts = load_pool(BACKLOG_POOL)
    for c in new_cands + backlog_cands:
        p3.classify(c, ev_all.get(c["qid"], {}))

    selected, queued, skipped, requeued = [], [], [], []
    promoted_from_queue = []          # (queueId, candidate, entry)
    seen = {"qids": set(), "names": set(), "handles": set()}

    # ---------------------------------------------------- new candidates (pools D/E/F)
    for cand in new_cands:
        decision, payload = evaluate(cand, existing, seen)
        if decision == "skip":
            skipped.append((cand, payload))
            continue
        if decision == "queue":
            queued.append((cand, payload))
            continue
        dob = payload
        entry = s13.build_entry(next_id, cand, dob)
        if cand["group"] != "beach":
            entry = p3.generic_sport_text(entry)
        if cand["college_teams"] and "College Athlete" not in entry["categories"]:
            entry["categories"].append("College Athlete")
        entry = apply_pass4_rules(cand, entry)
        if not cand["ref_urls"] and not cand["wiki_urls"]:
            entry["flags"].append("AGE_EVIDENCE_SECONDARY_SOURCES")
        entry["flags"] = sorted(set(entry["flags"]))
        selected.append((cand, dob, entry))
        seen["qids"].add(cand["qid"])
        seen["names"].add(s13.norm_name(cand["name"]))
        seen["handles"] |= {h.lstrip("@").lower() for h in cand["handles"].values() if h}
        next_id += 1

    # ---------------------------------------------------- backlog re-test (pool G)
    # A backlog candidate is only ever matched to its own queue item (by Q-ID first, then by exact name); it is
    # promoted out of the queue only on the same evidence standard as a new candidate.
    for cand in backlog_cands:
        match = rq_by_qid.get(cand["qid"]) or rq_by_name.get(s13.norm_name(cand["name"]))
        if not match:
            skipped.append((cand, "no-matching-queue-item"))
            continue
        rid, item = match
        # judge against the catalog as it will be after this pass (new promotions included)
        live_existing = {
            "names": existing["names"] | seen["names"],
            "tokens": existing["tokens"] + [set(re.sub(r"[^a-z ]", "", n.lower()).split()) for n in seen["names"]],
            "urls": existing["urls"] | {s["url"] for _, _, e in selected for s in e["sources"]},
            "handles": existing["handles"] | seen["handles"],
            "qids": existing["qids"] | seen["qids"],
        }
        decision, payload = evaluate(cand, live_existing, {"qids": set(), "names": set(), "handles": set()})
        if decision != "promote":
            requeued.append((cand, rid, decision, payload))
            # keep the surviving queue item honest about the re-test: it was looked at again on this date and the
            # outcome is recorded, so a reviewer never has to guess whether the backlog was re-examined.
            item["lastChecked"] = TODAY.isoformat()
            retest = (
                f" {PASS_LABEL} re-test {TODAY.isoformat()}: the structured record was re-harvested "
                f"(pool G, evidence s13_evidenceD.tsv) and the candidate is still not promotable — "
                f"{reason_explanation(payload) if decision == 'queue' else 'skipped as ' + str(payload)} "
                f"No value was changed and nothing was guessed; the item stays in the queue."
            )
            if retest not in item.get("notes", ""):
                item["notes"] = (item.get("notes", "") + retest).strip()
            continue
        dob = payload
        entry = s13.build_entry(next_id, cand, dob)
        if cand["group"] != "beach":
            entry = p3.generic_sport_text(entry)
        if cand["college_teams"] and "College Athlete" not in entry["categories"]:
            entry["categories"].append("College Athlete")
        entry = apply_pass4_rules(cand, entry)
        if not cand["ref_urls"] and not cand["wiki_urls"]:
            entry["flags"].append("AGE_EVIDENCE_SECONDARY_SOURCES")
        entry["flags"] = sorted(set(entry["flags"]))
        entry["notes"] += (
            f" Backlog re-test: this candidate was held in the review queue as {rid} "
            f"({'/'.join(item.get('missingEvidence') or item.get('flags') or ['unknown reason'])}); "
            f"{PASS_LABEL} re-harvested the structured record and the date of birth is now traceable, so the item "
            "is promoted and the queue entry retired. No value was changed to achieve this."
        )
        selected.append((cand, dob, entry))
        promoted_from_queue.append((rid, cand, entry))
        seen["qids"].add(cand["qid"])
        seen["names"].add(s13.norm_name(cand["name"]))
        seen["handles"] |= {h.lstrip("@").lower() for h in cand["handles"].values() if h}
        next_id += 1

    # ---------------------------------------------------- write queue additions
    retired = {rid for rid, _, _ in promoted_from_queue}
    new_rq = [r for r in rq if (r.get("id") or r.get("queueId")) not in retired]
    for cand, reason in queued:
        new_rq.append(queue_row(cand, reason, rq_num))
        rq_num += 1

    # ---------------------------------------------------- audit artifact
    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# {PASS_LABEL} selection audit \u2014 every decision with its evidence links "
                 f"(generated {TODAY.isoformat()}).\n")
        fh.write("# new pools: s13_pass4_new.tsv (pools D/E/F deduped) | backlog pool: s13_poolG.tsv | "
                 "evidence: s13_evidenceD.tsv\n")
        fh.write("\n## PROMOTED (new candidates)\n")
        fh.write("# entryId\tqid\tgroup\tname\tdob\tage\thandles\tdobSources\treferenceUrls\twikipedia\tusTeams\n")
        for cand, dob, entry in selected:
            if any(cand["qid"] == c2["qid"] for _, c2, _ in promoted_from_queue):
                continue
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["group"], cand["name"], dob.isoformat(), str(s13.age_on(dob)),
                handles, ";".join(cand["dob_sources"]) or "-", ";".join(cand["ref_urls"]) or "-",
                ";".join(cand["wiki_urls"]) or "-", ";".join(cand["teams"]) or "-",
            ]) + "\n")
        fh.write("\n## PROMOTED OUT OF THE REVIEW QUEUE (backlog re-test)\n")
        fh.write("# retiredQueueId\tentryId\tqid\tname\tdob\tage\tdobSources\treferenceUrls\twikipedia\n")
        for rid, cand, entry in promoted_from_queue:
            fh.write("\t".join([
                rid, entry["id"], cand["qid"], cand["name"],
                s13.parse_dob(cand["dob"]).isoformat(), str(s13.age_on(s13.parse_dob(cand["dob"]))),
                ";".join(cand["dob_sources"]) or "-", ";".join(cand["ref_urls"]) or "-",
                ";".join(cand["wiki_urls"]) or "-",
            ]) + "\n")
        fh.write("\n## QUEUED (new candidates not promoted)\n# qid\tname\treason\tdob\tevidence\n")
        for cand, reason in queued:
            fh.write("\t".join([cand["qid"], cand["name"], reason, cand["dob"] or "-",
                                ";".join(cand["ref_urls"] + cand["wiki_urls"] + cand["dob_sources"]) or "-"]) + "\n")
        fh.write("\n## BACKLOG RE-TESTED AND LEFT IN THE QUEUE\n# queueId\tqid\tname\tdecision\treason\n")
        for cand, rid, decision, payload in requeued:
            fh.write("\t".join([rid, cand["qid"], cand["name"], decision, str(payload)]) + "\n")
        fh.write("\n## SKIPPED (already catalogued / already queued elsewhere)\n# qid\tname\treason\n")
        for cand, reason in skipped:
            fh.write("\t".join([cand["qid"], cand["name"], reason]) + "\n")

    by_group = {}
    for cand, _, _ in selected:
        by_group[cand["group"]] = by_group.get(cand["group"], 0) + 1
    with_ref = sum(1 for c, _, _ in selected if c["ref_urls"])
    with_wiki = sum(1 for c, _, _ in selected if c["wiki_urls"])
    with_college = sum(1 for c, _, _ in selected if c["college_teams"])
    flagged_secondary = sum(1 for _, _, e in selected if "AGE_EVIDENCE_SECONDARY_SOURCES" in e.get("flags", []))
    flagged_suspect = sum(1 for _, _, e in selected if "SUSPECT_HANDLE_SHAPE" in e.get("flags", []))
    flagged_alias = sum(1 for _, _, e in selected if "NAME_ALIAS_IN_WIKIPEDIA" in e.get("flags", []))
    mixed = sum(1 for _, _, e in selected
                if "Beach Volleyball" in e["categories"] and "Volleyball" in e["categories"])

    print(f"new pool file        : {os.path.relpath(NEW_POOL, ROOT)}  ({len(new_cands)} unique candidates)")
    print(f"backlog pool file    : {os.path.relpath(BACKLOG_POOL, ROOT)}  ({len(backlog_cands)} unique candidates)")
    print(f"evidence file        : {os.path.relpath(EVIDENCE, ROOT)}  ({len(ev_all)} Q-IDs with evidence rows)")
    print(f"conflicting DOB QIDs : new={list(new_conflicts)} backlog={list(backlog_conflicts)}")
    print(f"promoted in total    : {len(selected)}  (new {len(selected) - len(promoted_from_queue)}, "
          f"out of the review queue {len(promoted_from_queue)})")
    for g in ("ncaa", "beach", "intl"):
        if by_group.get(g):
            print(f"    {g:<6}: {by_group[g]}")
    print(f"    with external ref URL : {with_ref}")
    print(f"    with Wikipedia article: {with_wiki}")
    print(f"    college-team member   : {with_college}")
    print(f"    both disciplines      : {mixed}")
    print(f"    flagged secondary-only: {flagged_secondary}")
    print(f"    flagged suspect handle: {flagged_suspect}")
    print(f"    flagged name alias    : {flagged_alias}")
    print(f"queued (new)           : {len(queued)}")
    rc = {}
    for _, reason in queued:
        rc[reason] = rc.get(reason, 0) + 1
    for r, n in sorted(rc.items()):
        print(f"    {r}: {n}")
    print(f"backlog left queued    : {len(requeued)}")
    rc2 = {}
    for _, _, _, payload in requeued:
        rc2[str(payload)] = rc2.get(str(payload), 0) + 1
    for r, n in sorted(rc2.items()):
        print(f"    {r}: {n}")
    print(f"skipped                : {len(skipped)}")
    sc = {}
    for _, reason in skipped:
        sc[reason] = sc.get(reason, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    print(f"review queue           : {len(rq)} -> {len(new_rq)}")
    print(f"audit artifact         : {os.path.relpath(AUDIT, ROOT)}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return

    catalog["entries"].extend(entry for _, _, entry in selected)
    catalog["reviewQueue"] = new_rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(new_rq)
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" {PASS_LABEL} added {len(selected)} further verified volleyball profiles "
        f"({by_group.get('ncaa', 0)} US-college-team-linked, {by_group.get('beach', 0)} beach volleyball, "
        f"{by_group.get('intl', 0)} other): {with_ref} cite an external reference URL attached to their own "
        f"date-of-birth statement (worldofvolley.com, Volleyball World, Volleybox, bvbinfo.com, CEV, the German "
        f"Bundesliga, the Spanish RFEVB, jornaldovolei.com.br, volleyball.ca, olympedia.org, ladies-in-black.de, "
        f"Dresdner SC, wkusports.com), {with_wiki} also carry an English Wikipedia article, {with_college} record "
        f"membership of a US collegiate volleyball team, {mixed} are evidenced in BOTH disciplines, "
        f"{flagged_secondary} are flagged AGE_EVIDENCE_SECONDARY_SOURCES because the birth date is referenced only "
        f"to a named database that attaches no URL, {flagged_suspect} carry SUSPECT_HANDLE_SHAPE and "
        f"{flagged_alias} carry NAME_ALIAS_IN_WIKIPEDIA. {len(promoted_from_queue)} of them were promoted out of "
        f"the existing review queue by re-testing it against the same standard, and {len(queued)} new candidates "
        f"were routed to the review queue instead of being promoted ({rc.get('SPORT_NOT_CORROBORATED', 0)} of them "
        f"SPORT_NOT_CORROBORATED, where the only date-of-birth reference is a tennis roster or an idol-group "
        f"agency page). Follower counts for these accounts stay {UNKNOWN_COUNT} / {UNKNOWN_RANGE} until publicly "
        f"observed \u2014 never estimated, never summed across platforms."
    )
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, {len(new_rq)} review-queue items")


if __name__ == "__main__":
    main()
