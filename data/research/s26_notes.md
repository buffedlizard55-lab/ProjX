# Session 26 (2026-09-06)

Wikidata P106 model / fashion-model / volleyball continuation (OFFSET 500–950) with line-by-line verdicts.

## Harvest
- 14 SPARQL queries archived in `data/research/s26_queries.json` and `data/research/urls/s26_*.url`.
- Raw rows `data/research/s26_*.tsv` (`\|`-escaped pipes, `##` row terminators).
- `scripts/session26_parse.py` → `data/research/s26_candidates.json`: 700 rows / 470 unique QIDs / 251 new
  (dupes: qid 211, name 6, handle 2).
- `data/research/s26_verify_buckets.json`: wiki 159 + agency 91 objects (qid/name/dob/ig/tt/refUrl/wiki).

## Verification
- `data/research/verification_s26_log.tsv` — 260 rows `qid|name|dob|verdict|category|evidence|source_url`.
- Verdicts: PROMOTE 153, REVIEW 100, REJECT 6, MINOR_UNDERAGE 1.
- Evidence hosts (PROMOTE): en.wikipedia 112, cs.wikipedia 5, famousbirthdays 4, web.archive.org (V.LEAGUE) 2,
  zh-yue.wikipedia 1, official agency/federation singletons (rising-pro.jp, vivi.tv, karascioconsulenzeartistiche.com,
  rbcasting.com, es.yatecasting.com, aoi-15days.com, thetv.jp, worldathletics.org), press singletons.

## Apply (`scripts/session26_apply.py`)
- Dry-run then live. +144 entries W-2026-1861..2004 (social; 143 IG, 37 TT), +102 queue R-2026-155..256.
- Guards fired: 6 year-only DOB PROMOTEs → REVIEW AGE_PARTIAL; 1 QID already in catalog; 6 batch dupes.
- REJECT log-only: Anielle Franco, Rina Matsuno (d.), Sienna Weir (d.), Abby Choi (d.), Kelsey Turner.
- MINOR: Vittoria Seixas Q122866537 (2008-12-22) queued, never published.
- Flags: AGE_EVIDENCE_WIKIPEDIA_ONLY 111, AGE_EVIDENCE_SECONDARY_SOURCES 11.
- IRR-2026-09-06-028.

## Post-apply fixes
- Removed 104 redundant duplicate Wikipedia source rows (same URL listed as age-evidence and other-trusted).
- Review-queue ID collision (R-2026-154 issued twice) → Session 26 rows renumbered R-2026-155..256; script counter fixed.

## Spot-checks
Park Eun-jin 1999-12-15, Rachael Kramer 1998-03-15 (live), Madison Lilley 1999-04-15, Bryoni Govender 1996-07-17,
Karely Ruiz 2000-10-28, Elena Funari 1995-04-12, Reiyo Matsumoto 2008-02-29, Carman Chan 2000-11-11,
Akiho Matsumoto 1997-06-29, Marie-Ange Brumelot 1993-01-14 — all matched.

## Catalog after this session
**2003** entries, **1811** social, **192** reference, **244** review, **28** IRR. Validator errors=0.
