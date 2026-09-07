# Session 28 (2026-09-06)

Wikidata model / fitness-model / pageant / creator pool — page 1 beyond Q123694020 (English-Wikipedia items) with line-by-line verdicts.

## Harvest
- Query `data/research/urls/s27b_model_gt_off0.url` (female; P106 Q4610556/Q3357567/Q762121/Q15982795/Q124408963; born 1985–2008;
  P2003 or P7085; en-wiki sitelink; `FILTER(STR(?p) > ".../Q123694020")`; `ORDER BY ?p LIMIT 150`; `BIND("|")` separator columns).
- Raw: `data/research/s27_raw/model_gt_off0_chunk0.txt` (chunk-boundary record repaired by hand) → `model_gt_off0_rows.json` (150 rows)
  → `model_gt_off0_new.json` (147 unique, 143 new; dupes Jordan Carver, Eliška Bučková, Iryna Zhuravska, Renae Ayris).
- Last Q-ID on this page: **Q134404200** (Danielle St James) → page 2 starts `STR(?p) > ".../Q134404200"`.

## Verification
- en-wiki lead extracts (exsentences=2) in 8 batches of 20 + 1 single: `data/research/urls/s27b_enwiki_extract_batch0..8.url`,
  archived `data/research/s27_raw/enwiki_b0..b7.json`; joined in `model_gt_off0_checked.json` (status MATCH 111 / NODATE 17 / DIFF 15).
- Undated / differing pages: infobox wikitext `s27b_enwiki_infobox_batch0..1.url` (rvsection=0) and short descriptions
  `s27b_enwiki_shortdesc_batch0.url`.
- `data/research/verification_s28_log.tsv` — 143 rows `qid|name|dob|verdict|category|evidence|source_url`.
- Verdicts: PROMOTE 84, REVIEW 57, REJECT 1 (Landy Párraga, d. 2024-04-28), MINOR_UNDERAGE 1 (Ella Gross 2008-12-01).
- Jan-1 Wikidata values replaced by the cited en-wiki date (flag MINOR_SOURCE_CONFLICT_NOTED): Deba Hekmat 2001-11-14,
  Savannah Gankiewicz 1995-11-28, María Alejandra Camargo 1997-09-24, Rhea Singha 2004-12-10, Winta Zesu 2000-11-01.
- Two different full dates (en-wiki vs Wikidata) → REVIEW DOB_CONFLICT even when both adult (13 rows).
- Lead-only scope rule: actresses/singers/idols/TV personalities/athletes with no modeling or creator activity in the lead →
  REVIEW scope-ambiguous (42 rows incl. Tasha Ghouri, Demi Sims, Ashley Tisdale, Ella Purnell, Irene, Raisa, Nyusha, Noor Pahlavi).
- Pechaya Wattanamontree → REVIEW LEGAL_PROCEEDINGS_NOTED (lead: arrested, detained pending trial) — not published.
- Validator age guard: an "18th birthday 2026-06-28" phrase in the Rainy evidence tripped the born-context year regex → reworded.

## Apply (`scripts/session28_apply.py`)
- Dry-run then live. +84 entries W-2026-2046..2129 (social; 84 IG, 27 TT), +58 queue R-2026-260..317.
- Queue flags: scope-ambiguous 42, DOB_CONFLICT 13, AGE_PARTIAL 10, WIKI_REDIRECT 1, LEGAL_PROCEEDINGS_NOTED 1, MINOR_UNDERAGE 1.
- MINOR rows are queued without handle / profile URL (script guard added).
- Flags: AGE_EVIDENCE_WIKIPEDIA_ONLY ×84, MINOR_SOURCE_CONFLICT_NOTED ×5. Ages 18–41.
- IRR-2026-09-06-030.

## Spot-checks (live, exsentences=1)
Eve Gilles 2003-07-09, Ella-Mae Rayner 1995-04-24, Chelsea Manalo 1999-10-14, Leah Halton 2001-01-06, Haruka Sakuraba 2006-01-29,
Valentina Alekseeva 2006-08-11, Victoria Kjær Theilvig 2003-11-13, Alla Bruletova 1999-09-15, Nicole Bahls 1985-11-15,
Danielle St James 1992-04-18 — all matched.

## Catalog after this session
**2128** entries, **1936** social, **192** reference, **305** review, **30** IRR. Validator errors=0.
Directory: `directory/` 159 known-count pages, `directory-unknown/` 1,777 unknown-count pages.

## Next
Page 2: same query with `STR(?p) > "http://www.wikidata.org/entity/Q134404200"`; then the 2,415-item non-en-wiki pool.
