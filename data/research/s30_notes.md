# Session 30 (2026-09-06)

Wikidata model pool — **Japanese-Wikipedia slice, page 1** (no en-wiki article), line-by-line ja-wiki lead verdicts.

## Why
Session 29 (en-wiki page 2) was celebrity-heavy → pivot to the 2,415-item non-en-wiki pool.
Per-site COUNT (same filters as `urls/s27b_count_model_nonen.url`, GROUP BY sitelink site): ja 1168, zh 343, zh-yue 242,
es 233, id 207, ko 185, de 117, fr 97, pt 94, it 85, ms 79, ar/ru 56, he 54, th 52, vi 44, mad 39, arz 36, cs 32, uk 28 …

## Harvest
- `urls/s30_model_jawiki_off0.url` — tsv, `?p ?dob |?ig |?tt |?wiki`, ja sitelink required, en-wiki excluded, ORDER BY ?p LIMIT 150 OFFSET 0.
- Raw chunks `s30_raw/model_ja_chunk0..2.txt` (3 fetch_page chunks). Parsed → `model_ja_rows.json` (150) → `model_ja_people.json`
  (148 unique; 2 people with two IG handles) → `model_ja_new.json` (135 after Q-ID / en-name / ja-title / handle dedup; 13 known).
- **Renderer gotcha:** when a row has a TikTok handle the tsv renderer glues it onto the ja URL (`…%E5%B8%8Cirie_misaki_official`).
  Repaired by regex (percent-encoded title + ascii tail); confirmed against `wbgetentities` (Q100453681 P7085 = irie_misaki_official).
  ASCII titles (Kirari) need a manual split.
- Labels / kana / citizenship: `urls/s30_ja_labels_135.url` → `s30_raw/ja_labels_chunk0..1.txt` → `ja_labels.json`.

## Verification
- ja-wiki extracts (`exintro&exsentences=2&exlimit=20`): `urls/s30_jawiki_extract_batch0..6.url` → `s30_raw/jawiki_b0..b6.json` → `model_ja_checked.json`.
- Lead date regex `(\d{4})年(?:〈…〉)?(\d{1,2})月(\d{1,2})日` vs Wikidata: 128 match / 3 no full date / 4 conflict.
- `scripts/session30_verdicts.py` → `verification_s30_log.tsv` (135: 110 PROMOTE / 24 REVIEW / 1 REJECT) + `s30_verify_buckets.json`.
- Scope: グラビアアイドル (swimsuit-magazine model) and レースクイーン (promotional model) = in scope; idol/singer/actress/announcer-only → scope-ambiguous;
  AV女優 named in lead → scope-ambiguous, manual decision (3: MINAMO, Sakura Misaki, Emiri Okazaki).

## Apply (`scripts/session30_apply.py`, dry-run then live)
- +110 entries W-2026-2206..2315 (social; 112 IG / 38 TT handles), +24 queue R-2026-380..403, IRR-2026-09-06-032.
- New flag `MULTIPLE_IG_HANDLES_DOCUMENTED` (Michelle Kinoshita, Kotao Tomozawa — second IG recorded with "current-use status unverified").
- Flags: AGE_EVIDENCE_WIKIPEDIA_ONLY ×110, NAME_ALIAS_IN_WIKIPEDIA ×8, COUNTRY_NOT_RECORDED ×1. Ages 18–41 (five turned 18 in Jan–Jul 2026).
- Validator gotcha: numeric TikTok string after "DOB" in evidence text was read as a birth year → reworded. errors=0.

## Spot-checks
10/10 (`urls/s30_spotcheck.url`): Kinon Fujimura 2005-04-08, Kurumi Nakata 1991-12-21, Elly Trần 1987-08-06, Rino Natsume 2004-06-15,
Arisa 1991-05-13, Eri Tokita 1992-03-06, Ayumi Seko 1990-10-18, Juliana Minato 1988-09-16, Narumi Nakakita 1989-10-26, Aira Nakajima 1995-05-28.

## Catalog after this session
**2314** entries, **2122** social, **192** reference, **391** review, **32** IRR. Directory 159 known / 1,963 unknown pages.

## Next
ja slice `OFFSET 150` (same URL with the offset changed; ~8 pages total), then zh / es / id / ko slices (`schema:isPartOf <https://zh.wikipedia.org/>` etc.).
Deferred: en-wiki page 3 cursor `FILTER(STR(?p) > ".../Q16065114")`. Next IDs W-2026-2316 / R-2026-404 / IRR-…-033.
