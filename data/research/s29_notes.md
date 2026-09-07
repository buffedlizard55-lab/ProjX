# Session 29 (2026-09-06)

Wikidata model / fitness-model / pageant / creator pool — page 2 beyond Q134404200 (English-Wikipedia items) with line-by-line verdicts.

## Harvest
- Query `data/research/urls/s29_model_gt_off0.url` (female; P106 Q4610556/Q3357567/Q762121/Q15982795/Q124408963; born 1985–2008;
  P2003 or P7085; en-wiki sitelink; `FILTER(STR(?p) > ".../Q134404200")`; `ORDER BY ?p LIMIT 150`; `BIND("|")` separator columns).
- Raw: `data/research/s29_raw/model_gt2_chunk0..2.txt` (two chunk-boundary splits glued; five rows had a second IG handle glued
  onto the article URL → title repaired: Tatjana Saphira, Valentina Zenere, CJ Perry, Deepika Padukone, Sakurako Ohara)
  → `model_gt2_rows.json` (150 rows) → `model_gt2_new.json` (145 unique, 139 new; dupes Poppy Delevingne, Gabriela Markus,
  Nana Meriwether, Hinarani de Longeaux, Taťána Kuchařová by Q-ID, Lauren Drain by handle).
- Duplicate Wikidata DOBs kept as `otherDobs`: Heather Marks (1987-05-27 / 1988-07-25), Karen Ghrawi (1991-01-01 / 1991-07-10).
- Last Q-ID on this page: **Q16065114** (Helly Luv) → page 3 starts `STR(?p) > ".../Q16065114"`.

## Verification
- en-wiki lead extracts (exsentences=2) in 7 batches: `data/research/urls/s29_enwiki_extract_batch0..6.url`,
  archived `data/research/s29_raw/enwiki_b0..b6.json`; joined in `model_gt2_checked.json`.
- Undated leads: infobox wikitext `s29_enwiki_infobox_batch0..1.url` (rvsection=0, 19 titles) — full infobox dates matching
  Wikidata → PROMOTE (Beenish Chohan, Eva Klímková, Jannatul Ferdous Peya, Cherry Ngan, Amna Ilyas); empty birth_date →
  AGE_PARTIAL (Salma Ranggita, Zhao Na, Yasmine Petty, Kate Stoltz, Ayyan, Nichole Sakura, Apple Chan); year-only → AGE_PARTIAL
  (Charlotte Grant 2000, Erika Linder 1990); age-derived → AGE_PARTIAL (Jamie Brewer); no infobox → AGE_PARTIAL (Mariluz Bermúdez,
  Indira Joshi); infobox date ≠ Wikidata → DOB_CONFLICT (Airin Sultana 1988-12-27 vs 1988-09-04); Nadia Hilker infobox 1988-12-01
  matches but lead is actress-only → scope-ambiguous.
- Verdict table: `scripts/session29_verdicts.py` → `data/research/verification_s29_log.tsv` (139 rows
  `qid|name|dob|verdict|category|evidence|source_url`) + `data/research/s29_verify_buckets.json`.
- Verdicts: PROMOTE 76, REVIEW 62, REJECT 1 (Q137459163 "Princess Kill" = twin-sister duo item, not a person), MINOR 0.
- Jan-1 Wikidata value replaced by the cited en-wiki date (flag MINOR_SOURCE_CONFLICT_NOTED): Sadia Jahan Prova 1988-03-30.
- Group accounts deliberately NOT recorded: TikTok PrincessKilltown (duo) on Nutnacha Krusagayavong; TikTok rahajengsisters on
  Agnes Rahajeng; IG babymetal_official on Moa Kikuchi (queued without handle).
- New queue flag: GENDER_EVIDENCE_REVIEW (Jade Runk — article uses they/them, Wikidata says female; plus DOB conflict) — held
  for manual first-party confirmation, nothing inferred.
- Scope rule kept the celebrities out: Dove Cameron, Ariana Grande, Madison Beer, Danna Paola, Shraddha Kapoor, Deepika Padukone,
  Seulgi, Liza Soberano, Kat Graham, CJ Perry … → REVIEW scope-ambiguous (lead documents no modeling/creator activity).
  Kendall Jenner promoted (lead: model).

## Apply (`scripts/session29_apply.py`, copied from session28_apply.py; adds MINOR_SOURCE_CONFLICT_NOTED when evidence says
"preferred over Wikidata")
- Dry-run then live. +76 entries W-2026-2130..2205 (social; 76 IG, 3 TT), +62 queue R-2026-318..379.
- Queue flags (overlapping): scope-ambiguous 37, AGE_PARTIAL 15, DOB_CONFLICT 14, WIKI_REDIRECT 3, GENDER_EVIDENCE_REVIEW 1.
- Entry flags: AGE_EVIDENCE_WIKIPEDIA_ONLY ×76, MINOR_SOURCE_CONFLICT_NOTED ×1. Ages 20–40. 40 countries.
- IRR-2026-09-06-031.

## Spot-checks (live, exsentences=1, `data/research/urls/s29_spotcheck.url`)
Ella Morgan 1993-12-27, Gaby Guha 1999-10-01, Fátima Bosch 2000-05-19, Olandria 1998-05-29, Bhavitha Mandava 2000-02-03,
Sóldís Ívarsdóttir 2006-04-23, Alexina Graham 1990-03-03, Sadia Jahan Prova 1988-03-30, Rolene Strauss 1992-04-22,
Helly Luv 1988-11-16 — all matched.

## Distribution note
This page was celebrity-heavy; the promoted set is national pageant titleholders + working models. Next pass must re-balance
toward micro/emerging creators (non-en-wiki pool = regional creators; then non-Wikidata sources).

## Catalog after this session
**2204** entries, **2012** social, **192** reference, **367** review, **31** IRR. Validator errors=0.
