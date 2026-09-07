# Session 27 (2026-09-06)

Wikidata women's volleyball / beach-volleyball harvest (all leagues, born 1985–2008) with line-by-line verdicts.

## Harvest
- 5 SPARQL pages archived in `data/research/urls/s27_vb_wiki_off{0,150,300,450,600}.url`
  (plain-column `SELECT ?p ?name ?dob ?ig ?tt … ORDER BY ?p LIMIT 150 OFFSET n`, csv/tsv, 2–3 fetch chunks each).
- Raw rows `data/research/s27_raw/vb_wiki_off*_chunk0.txt` (fetch_page strips delimiters → glued rows; `\|` / `\_` escapes).
- `scripts/session27_parse.py --out data/research/s27_candidates.json` → 743 rows / 45 new after Q-ID + name + handle dedup.
- Follow-up scoping: 1970–84 band (`s27b_vb1970_84_off0.url`) = 56 rows, 49 known, 7 non-volleyball → `data/research/s27b_candidates.json` (not added).
- Handles for the 44 verified candidates: `data/research/s27_raw/wd_handles_44.txt`.

## Verification
- `data/research/verification_s27_log.tsv` — 44 rows `qid|name|dob|verdict|category|evidence|source_url`.
- Verdicts: PROMOTE 41, REVIEW 3. Anielle Franco Q105939031 excluded up front (Session 26 REJECT, politician).
- Evidence: Wikipedia lead sentences via the MediaWiki extracts API (ja 24, de 10, ru 3, en 3, th 1, it 1);
  extracts archived in `data/research/s27_raw/*wiki_extract*.json`.
- Narissara Kaewma: th-wiki gives the Buddhist-era year (2539) → recorded as 1996-04-11; corroborated by women.volleybox.net roster (born 1996).
  Never place a BE year within 45 chars after "born" in evidence text (validator age guard).

## Apply (`scripts/session27_apply.py`)
- Dry-run then live. +41 entries W-2026-2005..2045 (social; 40 IG, 2 TT), +3 queue R-2026-257..259 (scope-ambiguous:
  Satoyuri comedian, Kiiara singer, Melanie Hasler bobsledder).
- Categories: Volleyball/Athlete/Sports ×40 (+College Athlete ×7), Beach Volleyball ×1 (Miki Ishii).
- Flags: AGE_EVIDENCE_WIKIPEDIA_ONLY ×41. Ages 26–38.
- IRR-2026-09-06-029.

## Spot-checks
Minori Wada 1996-02-21, Miki Ishii 1989-11-07, Narissara Kaewma 1996-04-11, Gabriella Vico 1987-12-04, Kaori Mabashi 1996-11-18,
Liza Kastrup 1999-10-05, An Hye-jin 1998-02-16, Symone Speech 1997-05-29, Viktoria Russu 1999-02-16 — all matched.

## Catalog after this session
**2044** entries, **1852** social, **192** reference, **247** review, **29** IRR. Validator errors=0.
Directory: `directory/` 159 known-count pages, `directory-unknown/` 1,693 unknown-count pages.

## Next
Model / fitness / pageant / creator Wikidata pool beyond Q123694020: en-wiki 3,157 / non-en-wiki 2,415 items
(`data/research/urls/s27b_count_*.url`); page 1 query `data/research/urls/s27b_model_gt_off0.url` → Session 28.
