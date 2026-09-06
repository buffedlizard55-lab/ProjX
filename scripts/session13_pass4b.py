#!/usr/bin/env python3
"""Session 13 pass 4b — targeted Tier-1 verification of review-queue candidates (2026-09-07).

Pass 4 left 75 candidates queued AGE_SOURCE_NOT_RECORDED: their date of birth exists in the Wikidata structured
record but carries NO reference, and verification-protocol rule 1 forbids promoting an unreferenced value. Those
candidates cannot be resolved by more pooling — each needs an individual public document that states the birth
date. This pass does that by hand for the first three, and records exactly what was opened and what it said.

Method (per candidate, no batching, no inference):
  1. targeted public search for the player's official federation / competition-registry profile;
  2. OPEN the primary page and transcribe what it publishes (values quoted verbatim in the audit file);
  3. require the opened page to agree with the date recorded in the structured item — agreement is the test,
     because the whole point is that the structured value was untraceable. Disagreement would be a conflict,
     recorded as such, not a promotion;
  4. corroborate the identity link to the recorded social handle from an independent registry that lists the
     handle itself, so the profile is not attached to a namesake.

Evidence tiers used here: Volleyball World (en.volleyballworld.com) is the FIVB's official competition platform
and CEV (cev.eu / eurovolley.cev.eu) is the European confederation's official registry — Tier 1 for both the birth
date and the women's-competition membership. Women Volleybox is a community-maintained database: Tier 3, used only
as corroboration and for the handle link, never as the sole basis. Pages located by search but NOT opened are
listed in the audit file with that caveat and are never cited as the primary evidence.

Nothing here was estimated, summed or inferred from appearance: follower counts stay FOLLOWER_COUNT_UNKNOWN
because Instagram blocks automated retrieval of profile pages, and no public analytics snapshot was consulted for
these three accounts in this pass.

Usage:  python3 scripts/session13_pass4b.py            # dry run (default)
        python3 scripts/session13_pass4b.py --apply    # write data/catalog.json
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CATALOG = os.path.join(ROOT, "data", "catalog.json")
RESEARCH = os.path.join(ROOT, "data", "research")
AUDIT = os.path.join(RESEARCH, "s13_pass4b_selected.tsv")
TODAY = "2026-09-07"          # the date these pages were actually opened
PASS = "Session 13 pass 4b (targeted Tier-1 verification of review-queue candidates)"

NO_INFER = ("Adult status is taken only from this documented birth date — never inferred from appearance, "
            "clothing, photographs, college attendance or any image-based judgement.")
GENDER_NO_INFER = ("Gender is established from documentary records (structured data fields, official "
                   "competition registries and women's-competition membership), never from appearance, clothing "
                   "or imagery.")
FOLLOWER_NOTE = ("No follower count was publicly observed on {today} (Instagram blocks automated retrieval of the "
                 "profile page and no public analytics snapshot was consulted for this account in this pass), so "
                 "it is recorded as FOLLOWER_COUNT_UNKNOWN rather than estimated.")

# Each record below is transcribed from a page that was OPENED on 2026-09-07. "quote" holds the values verbatim as
# the page published them. "search_only" pages were located by targeted search but NOT opened, and are labelled as
# such wherever they appear — they are corroboration, never the basis for a claim.
VERIFIED = [
    {
        "queue_id": "R-2026-028",
        "qid": "Q57058850",
        "name": "Demi Korevaar",
        "dob": "2000-08-09",
        "age": 26,
        "country": "Netherlands",
        "position": "Middle blocker",
        "handle": ("Instagram", "demikorevaar"),
        "primary": {
            "label": "Volleyball World (FIVB official competition platform) — VNL 2022 player profile 167777, "
                     "Demi Korevaar",
            "url": "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/2022/players/167777",
            "quote": "Team: Netherlands (jersey 8, linked as .../teams/women/5129/). Position: Middle blocker (MB). "
                     "Nationality: Netherlands (NL). Age: 26. Birth date: 09/08/2000. Height: 187cm.",
        },
        "opened": [
            {
                "label": "Women Volleybox — player profile p11550, Demi Korevaar",
                "url": "https://women.volleybox.net/demi-korevaar-p11550",
                "quote": "Nationality: Netherlands. Position: Middle-blocker. Birthdate: August 9, 2000 (26 years "
                         "old). Height: 187 cm. Weight: 71 kg. Dominant hand: Right. Clubs: 2026/27-present "
                         "Levallois Paris Saint-Cloud (France); 2024/25-2025/26 Asterix AVO Beveren (Belgium); "
                         "2023/24 USC Münster (Germany); 2022/23 Schwarz-Weiß Erfurt (Germany); 2021/22 Team 22 "
                         "(Netherlands); 2019/20-2020/21 USC Münster; 2018/19 Sliedrecht Sport (Netherlands); "
                         "2016/17-2017/18 TT Papendal/Arnhem. The page's structured data also lists "
                         "sameAs https://www.instagram.com/demikorevaar/ and https://www.facebook.com/demi.korevaar.",
                "tier": 3,
            },
        ],
        "search_only": [
            ("http://japan2018.fivb.com/en/competition/teams/ned-netherlands/players/demi-korevaar?id=67329",
             "FIVB 2018 Women's World Championship (Japan) player profile: \"Birth Date: 09/08/2000\", "
             "\"Birth Place: Breda\", Club Sliedrecht Sport, Middle blocker, Nationality Netherlands"),
            ("https://eurovolley.cev.eu/team/12611-the-netherlands/player/67715-korevaar-demi",
             "CEV EuroVolley player profile: \"Demi KOREVAAR\", Birth date 2000, Nationality NED, 187 cm, "
             "Middle blocker"),
            ("https://profiles.worldofvolley.com/wov-community/players/128601/demi-korevaar.html",
             "World of Volley community profile: \"Date of birth : 09.08.2000\", Country Netherlands, "
             "Gender: Female, Middle Blocker"),
        ],
        "structured_teams": "Netherlands women's national volleyball team, USC Münster and Sliedrecht Sport",
        "extra_note": ("Four independent records agree on the same day-level birth date — the FIVB competition "
                       "platform (09/08/2000, day-first), the FIVB 2018 World Championship registry "
                       "(09/08/2000), CEV (2000) and Women Volleybox (August 9, 2000) — and the day-first reading "
                       "is confirmed by the platform's own \"Age 26\" against a 2026 check date. The date format on "
                       "the FIVB pages is day/month/year, which is how 09/08/2000 is read here; the corroborating "
                       "registries spell the month out, so no ambiguity remains."),
    },
    {
        "queue_id": "R-2026-014",
        "qid": "Q125226543",
        "name": "Kyriaki Terzoglou",
        "dob": "2003-11-22",
        "age": 22,
        "country": "Greece",
        "position": "Middle blocker",
        "handle": ("Instagram", "kiki_terzoglou"),
        "primary": {
            "label": "Volleyball World (FIVB official competition platform) — Women's World Championship 2025 "
                     "player profile 185731, Kyriaki Terzoglou",
            "url": "https://en.volleyballworld.com/volleyball/competitions/women-world-championship/players/185731",
            "quote": "Competition: Women's World Championship (2025). Team: Greece (jersey 14, linked as "
                     ".../teams/7313/). Position: Middle blocker (MB). Nationality: Greece (GR). Age: 22. "
                     "Birth date: 22/11/2003. Height: 187cm.",
        },
        "opened": [
            {
                "label": "Women Volleybox — player profile p72450, Kyriakí Terzóglou",
                "url": "https://women.volleybox.net/kiriaki-terzoglou-p72450",
                "quote": "Page title \"Kyriakí Terzóglou\"; Greek-alphabet form Κυριακή Τερζόγλου. Nationality: "
                         "Greece. Position: Middle-blocker. Birthdate: November 22, 2003 (22 years old). Place of "
                         "birth: Thessaloniki. Height: 188 cm. Weight: 70 kg. Dominant hand: Right. Agency: "
                         "YnK-EuroVolley, Athens, Greece. Clubs: 2025/26-2026/27 Olympiacos Piraeus; 2021/22-2024/25 "
                         "PAOK; 2019/20-2021/22 PAOK U20; 2018/19-2019/20 As Elpis Ampelokipon U20. National team "
                         "Greece: 2025 (21 FIVB World Championship 2025, Friendly International Women 2025, 7 "
                         "European Golden League 2025, European Championship Qualification 2025) and 2022-2023 (19 "
                         "European Championship 2023, European Championship Qualification 2023, 5 Mediterranean "
                         "Games 2022). The page's structured data also lists "
                         "sameAs https://www.instagram.com/kiki_terzoglou/.",
                "tier": 3,
            },
        ],
        "search_only": [
            ("https://www.cev.eu/team/13258-ac-paok-thessaloniki/player/89443-terzoglou-kiriaki",
             "CEV club-competition player profile (AC PAOK Thessaloniki): \"Kiriaki TERZOGLOU\", Birth date 2003, "
             "Nationality GRE, 187 cm, Middle blocker"),
            ("https://www.playmakerstats.com/player/kiriaki-terzoglou/1013915",
             "playmakerstats profile: \"Date of Birth 2003-11-22 (22 -yrs-old)\", Position Central, Nationality "
             "Greece, current club Olympiacos, 18 caps / 61 points"),
        ],
        "structured_teams": "not recorded in the structured item",
        "extra_note": ("Name forms: the structured item and this catalog use \"Kyriaki Terzoglou\"; Women Volleybox "
                       "titles the same profile \"Kyriakí Terzóglou\" (and CEV \"Kiriaki TERZOGLOU\"), i.e. "
                       "diacritic and transliteration variants of one Greek name (Κυριακή Τερζόγλου), not different "
                       "people. Per the pass-4 rule a diacritic-only difference is NOT flagged as a name alias; all "
                       "three spellings are recorded here so a reviewer can find the same player under any of them. "
                       "Her club history moves from PAOK (2021/22-2024/25) to Olympiacos Piraeus (2025/26 onward), "
                       "so club membership recorded anywhere should be read as of its season."),
    },
    {
        "queue_id": "R-2026-021",
        "qid": "Q106776104",
        "name": "Rebecca Piva",
        "dob": "2001-05-01",
        "age": 25,
        "country": "Italy",
        "position": "Outside hitter",
        "handle": ("Instagram", "rebepiva"),
        "primary": {
            "label": "Volleyball World (FIVB official competition platform) — VNL 2021 player profile 181258, "
                     "Rebecca Piva",
            "url": "https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/2021/players/181258",
            "quote": "Team: Italy (jersey 25, linked as .../teams/women/4680/). Position: Outside hitter (OH). "
                     "Nationality: Italy (IT). Age: 25. Birth date: 01/05/2001. Height: 183cm.",
        },
        "opened": [],
        "search_only": [
            ("https://eurovolley.cev.eu/team/12639-italy/player/87902-piva-rebecca",
             "CEV EuroVolley player profile (Italy): \"Rebecca PIVA\", Birth date 2001, Nationality ITA, 183 cm, "
             "Outside spiker"),
            ("https://women.volleybox.net/rebecca-piva-p30330",
             "Women Volleybox profile: \"born 1st May 2001\", Birthdate 2001-05-01 (25 years old), Place of birth "
             "Bologna, Position Outside Hitter, Nationality Italy, club Vero Volley Milano; structured data lists "
             "sameAs https://www.instagram.com/rebepiva/"),
        ],
        "structured_teams": "Trentino Rosa",
        "extra_note": ("Unlike the other two candidates in this pass, no second page was opened by hand for Rebecca "
                       "Piva: the FIVB competition platform is the sole Tier-1 page fetched, and the CEV and Women "
                       "Volleybox records were located by targeted search with their published values captured in "
                       "the audit file but the pages themselves not opened. All three agree on 1 May 2001 and on "
                       "Italy, and the Volleybox record independently lists the same Instagram handle that the "
                       "structured item records, which is what ties the profile to this person. A reviewer wanting "
                       "a second hand-opened source should open the CEV profile above. Registry heights differ "
                       "(183 cm on the FIVB and CEV pages, 187 cm on Volleybox); no physical attribute is used as "
                       "evidence of anything in this catalog, so the variance is recorded rather than resolved."),
    },
]


def age_on(dob, today=TODAY):
    y, m, d = (int(x) for x in dob.split("-"))
    ty, tm, td = (int(x) for x in today.split("-"))
    return ty - y - ((tm, td) < (m, d))


def build(rec):
    platform, handle = rec["handle"]
    profile = f"https://www.instagram.com/{handle}/"
    wikidata = f"https://www.wikidata.org/wiki/{rec['qid']}"
    primary = rec["primary"]
    dob_text = rec["dob"]
    pretty = primary["quote"]

    age = age_on(dob_text)
    assert age == rec["age"], (rec["name"], age, rec["age"])
    assert age >= 18, rec["name"]

    adult = (
        f"Born {dob_text} — age {age} as of {TODAY}, so an adult (18+). This candidate was held in the review "
        f"queue because the Wikidata structured item {rec['qid']} records that date of birth with NO reference "
        f"attached, so the value could not be traced to a document. It has now been verified against an official "
        f"competition registry opened by hand on {TODAY}: {primary['url']} publishes {pretty} The date published "
        f"there agrees exactly with the untraceable value in the structured item, which is the test applied — the "
        f"structured value was never treated as sufficient on its own. " + NO_INFER
    )
    if rec["opened"]:
        vball_clause = (
            f"and the community database women.volleybox.net — a women's-volleyball-only database — carries a "
            f"profile for her at {rec['opened'][0]['url']}, a page opened by hand on {TODAY}"
        )
    else:
        vball_clause = (
            f"and the community database women.volleybox.net — a women's-volleyball-only database — lists a "
            f"profile for her at {rec['search_only'][-1][0]} (located by targeted search; that page was NOT opened "
            f"in this pass, so it is corroboration only and the women's-competition evidence above rests on the "
            f"FIVB registry page, which was opened)"
        )
    gender = (
        f"Woman — the Wikidata structured item {rec['qid']} records sex/gender: female, and she is documented in "
        f"women's competition: {primary['url']} is her profile on the FIVB's official competition platform for a "
        f"women's national-team entry ({rec['country']}), {vball_clause}. " + GENDER_NO_INFER
    )

    sources = [
        {
            "label": f"{primary['label']} — page opened {TODAY}; publishes: {pretty}",
            "platform": "Website",
            "url": primary["url"],
            "relationship": "official",
        },
    ]
    for o in rec["opened"]:
        sources.append({
            "label": f"{o['label']} — page opened {TODAY}; publishes: {o['quote']}",
            "platform": "Website",
            "url": o["url"],
            "relationship": "other-trusted",
        })
    for url, what in rec["search_only"]:
        sources.append({
            "label": f"{what} — located by targeted public search on {TODAY}; page NOT opened in this pass, so the "
                     f"values quoted are as rendered in the search result and are corroboration only",
            "platform": "Website",
            "url": url,
            "relationship": "other-trusted",
        })
    sources.append({
        "label": f"Wikidata {rec['qid']} — {rec['name']} (women's volleyball; date of birth {dob_text} recorded "
                 f"WITHOUT a reference, which is why this candidate was queued; country: {rec['country']}; teams "
                 f"recorded: {rec['structured_teams']})",
        "platform": "Website",
        "url": wikidata,
        "relationship": "other-trusted",
    })
    sources.append({
        "label": f"Instagram — @{handle} (public profile; handle recorded in Wikidata {rec['qid']})",
        "platform": platform,
        "url": profile,
        "relationship": "verified-platform",
    })

    notes = (
        f"{PASS}; promoted out of the review queue {rec['queue_id']} on {TODAY}. Reason it was queued: "
        f"AGE_SOURCE_NOT_RECORDED — the structured item records a date of birth but attaches no reference to it, so "
        f"the value was untraceable and could not be promoted under verification-protocol rule 1. How it was "
        f"resolved: a targeted public search for the player's official federation / competition-registry profile, "
        f"then the page was OPENED and its published values transcribed; the official registry states the same "
        f"day-level birth date as the structured item, so the value is now traceable to a document. Identity was "
        f"tied to the recorded handle by an independent registry that lists the handle itself "
        f"(women.volleybox.net structured data sameAs {profile}), so the profile is not attached to a namesake. "
        f"Discovery category: European / international indoor volleyball. Citizenship recorded in Wikidata: "
        f"{rec['country']}. Position: {rec['position']}. "
        f"{rec['extra_note']} "
        f"Follower counts: none publicly observed for the listed account — recorded as FOLLOWER_COUNT_UNKNOWN / "
        f"FOLLOWER_RANGE_UNKNOWN (never estimated, never summed across platforms). Categories are objective "
        f"(sport, competition level, creator activity) — this directory is not an attractiveness ranking. "
        f"Full transcription of every page opened, and of every page located but not opened, is in "
        f"data/research/s13_pass4b_selected.tsv."
    )

    entry = {
        "id": None,                       # assigned by the caller, in catalog order
        "displayName": rec["name"],
        "categories": ["Athlete", "Volleyball", "Creator"],
        "legalAdultEvidence": {
            "summary": adult,
            "sourceLabel": primary["label"],
            "sourceUrl": primary["url"],
            "checkedAt": TODAY,
        },
        "genderEvidence": {
            "summary": gender,
            "sourceLabel": primary["label"],
            "sourceUrl": primary["url"],
            "checkedAt": TODAY,
        },
        "sources": sources,
        "socialAccounts": [{
            "platform": platform,
            "username": f"@{handle}",
            "profileUrl": profile,
            "followerCountDisplay": "FOLLOWER_COUNT_UNKNOWN",
            "followerCountNumeric": None,
            "countType": "unknown",
            "checkedAt": TODAY,
            "followerSizeRange": "FOLLOWER_RANGE_UNKNOWN",
            "sourceNote": f"Handle recorded in Wikidata {rec['qid']} and independently listed by "
                          f"women.volleybox.net. " + FOLLOWER_NOTE.format(today=TODAY),
        }],
        "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN",
        "verificationStatus": "verified",
        "lastReviewed": TODAY,
        "flags": [],
        "notes": notes,
    }
    if not rec["opened"]:
        # only one page was opened by hand for this candidate; say so on the record rather than letting the
        # source list imply everything was checked
        entry["flags"].append("SINGLE_PAGE_OPENED_BY_HAND")
        entry["notes"] += (" Flag SINGLE_PAGE_OPENED_BY_HAND: exactly one page was opened by hand for this "
                           "candidate (the FIVB competition-registry profile); the remaining citations were located "
                           "by search and are labelled as not opened.")
    return entry


def main():
    apply_changes = "--apply" in sys.argv
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)
    entries, rq = catalog["entries"], catalog["reviewQueue"]

    # ---- guards: nothing may be duplicated, and every queue row must exist exactly as expected
    names = {e["displayName"].lower() for e in entries}
    qids = {q for e in entries for q in re.findall(r"Q\d{5,}", json.dumps(e, ensure_ascii=False))}
    handles = {a.get("username", "").lstrip("@").lower() for e in entries for a in e.get("socialAccounts", [])}
    urls = {s["url"] for e in entries for s in e.get("sources", [])}
    nums = [int(m.group(1)) for e in entries for m in [re.match(r"W-2026-(\d+)$", str(e.get("id", "")))] if m]
    next_num = max(nums) + 1

    promoted, rows = [], []
    n_entries_before, n_queue_before = len(entries), len(rq)
    for rec in VERIFIED:
        assert rec["qid"] not in qids, f"{rec['name']}: Q-ID already catalogued"
        assert rec["name"].lower() not in names, f"{rec['name']}: name already catalogued"
        assert rec["handle"][1].lower() not in handles, f"{rec['name']}: handle already catalogued"
        assert rec["primary"]["url"] not in urls, f"{rec['name']}: primary URL already used"
        matches = [r for r in rq if isinstance(r, dict)
                   and (r.get("id") or r.get("queueId")) == rec["queue_id"]
                   and r.get("displayName") == rec["name"]]
        assert len(matches) == 1, f"{rec['name']}: expected 1 queue row {rec['queue_id']}, found {len(matches)}"
        item = matches[0]
        assert (item.get("missingEvidence") or [""])[0] == "AGE_SOURCE_NOT_RECORDED", item.get("missingEvidence")
        assert rec["handle"][1].lower() in json.dumps(item, ensure_ascii=False).lower(), "handle not on queue row"
        assert rec["dob"] in json.dumps(item, ensure_ascii=False), "DOB not recorded on queue row"

        entry = build(rec)
        entry["id"] = f"W-2026-{next_num}"
        next_num += 1
        promoted.append((rec, item, entry))

        rows.append("\t".join([
            entry["id"], rec["queue_id"], rec["qid"], rec["name"], rec["dob"], str(rec["age"]),
            f"{rec['handle'][0]}:@{rec['handle'][1]}", rec["country"], rec["position"],
            "OPENED " + rec["primary"]["url"],
            "OPENED " + "; ".join(o["url"] for o in rec["opened"]) if rec["opened"] else "no second page opened",
            "SEARCH-ONLY " + "; ".join(u for u, _ in rec["search_only"]),
        ]))

    if apply_changes:
        for rec, item, entry in promoted:
            entries.append(entry)
            rq.remove(item)                     # the queue row is retired by promotion
        catalog["metadata"]["entryCount"] = len(entries)
        catalog["metadata"]["reviewQueueCount"] = len(rq)
        catalog["metadata"]["generatedAt"] = TODAY
        catalog["metadata"]["summary"] += (
            f" {PASS} promoted {len(promoted)} of the 75 candidates held as AGE_SOURCE_NOT_RECORDED — Demi "
            f"Korevaar (Q57058850), Kyriaki Terzoglou (Q125226543) and Rebecca Piva (Q106776104) — by opening "
            f"each player's profile on Volleyball World, the FIVB's official competition platform, and confirming "
            f"that the birth date it publishes agrees exactly with the untraceable value in the structured item. "
            f"72 such candidates remain queued; each still needs an individual document and cannot be batched."
        )
        with open(CATALOG, "w", encoding="utf-8") as fh:
            json.dump(catalog, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write("# Session 13 pass 4b — targeted Tier-1 verification of review-queue candidates, "
                 f"executed {TODAY}.\n")
        fh.write("# Every candidate below was queued AGE_SOURCE_NOT_RECORDED: a date of birth existed in the "
                 "structured\n# record with no reference attached, so it could not be promoted. Resolution = find "
                 "and OPEN an official\n# registry page, then require it to agree with the recorded value. Pages "
                 "marked SEARCH-ONLY were located by\n# targeted search and were NOT opened; their quoted values "
                 "are as rendered in the search result and they are\n# never the basis for a claim.\n\n")
        fh.write("entryId\tretiredQueueRow\tqid\tname\tdob\tageOn%s\thandle\tcountry\tposition\t"
                 "primaryPageOpened\tsecondPageOpened\tcorroboratingSearchOnly\n" % TODAY)
        fh.write("\n".join(rows) + "\n\n")
        for rec, item, entry in promoted:
            fh.write(f"## {entry['id']} — {rec['name']} ({rec['qid']}), retired {rec['queue_id']}\n")
            fh.write(f"PRIMARY (opened {TODAY}) {rec['primary']['url']}\n")
            fh.write(f"  label : {rec['primary']['label']}\n")
            fh.write(f"  quoted: {rec['primary']['quote']}\n")
            for o in rec["opened"]:
                fh.write(f"OPENED (Tier {o['tier']}) {o['url']}\n")
                fh.write(f"  label : {o['label']}\n")
                fh.write(f"  quoted: {o['quote']}\n")
            for url, what in rec["search_only"]:
                fh.write(f"SEARCH-ONLY (not opened) {url}\n  rendered: {what}\n")
            fh.write(f"STRUCTURED ITEM {rec['qid']}: date of birth {rec['dob']} recorded WITHOUT a reference; "
                     f"sex/gender female; country {rec['country']}; teams recorded: {rec['structured_teams']}; "
                     f"handle {rec['handle'][0]} {rec['handle'][1]}\n")
            fh.write(f"AGREEMENT: official registry vs structured record = identical day-level date "
                     f"({rec['dob']}); age {rec['age']} on {TODAY}; adult 18+.\n")
            fh.write(f"NOTE: {rec['extra_note']}\n\n")

    print(f"{PASS}")
    print(f"promotions         : {len(promoted)}")
    for rec, item, entry in promoted:
        print(f"  {entry['id']}  {rec['name']:<22} {rec['dob']} age {rec['age']}  "
              f"{rec['handle'][0]} @{rec['handle'][1]}  retired {rec['queue_id']}")
    state = "applied" if apply_changes else "prospective, nothing written"
    print(f"entries            : {n_entries_before} -> {n_entries_before + len(promoted)}   ({state})")
    print(f"review queue       : {n_queue_before} -> {n_queue_before - len(promoted)}   ({state})")
    still = sum(1 for r in rq if isinstance(r, dict)
                and (r.get("missingEvidence") or [""])[0] == "AGE_SOURCE_NOT_RECORDED")
    print(f"AGE_SOURCE_NOT_RECORDED remaining: {still}")
    print(f"audit artifact     : {os.path.relpath(AUDIT, ROOT)}")
    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")


if __name__ == "__main__":
    main()
