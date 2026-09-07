# Session 31 (2026-09-06)

Wikidata model pool — **Japanese-Wikipedia slice, page 2 (OFFSET 150)**, line-by-line ja-wiki lead verdicts. Continuation of Session 30.

## Harvest
- `urls/s31_model_jawiki_off150.url` (Session 30 query, `LIMIT 150 OFFSET 150`) → `s31_raw/model_ja2_chunk0..2.txt` → `model_ja2_rows.json` (150)
  → `model_ja2_people.json` (150 unique) → `model_ja2_new.json` (145 after Q-ID / handle / title dedup; 5 known).
- Page ends at **Q11533992** (柚木しおり). Next page = `OFFSET 300`.
- Labels: `urls/s31_ja_labels_145.url` → `s31_raw/ja_labels_chunk0..1.txt` → `ja_labels.json` (parse regex: Q-ID, country, ja label, en label, `||||`, kana).

## Verification
- `urls/s31_jawiki_extract_batch0..7.url` → `s31_raw/jawiki_b0..b7.json` → `model_ja2_checked.json` (143 match / 2 no date / 0 conflict).
- `scripts/session31_verdicts.py` → `verification_s31_log.tsv` (145: 127 PROMOTE / 18 REVIEW) + `s31_verify_buckets.json`.
- Apply: `scripts/session31_apply.py` (copy of session30_apply with s31 paths / IDs / IRR-033) — dry-run then live.

## Result
+127 entries W-2026-2316..2442 (126 IG / 14 TT), +18 queue R-2026-404..421 (16 scope-ambiguous, 2 AGE_PARTIAL), IRR-2026-09-06-033.
Flags: AGE_EVIDENCE_WIKIPEDIA_ONLY ×127, NAME_ALIAS_IN_WIKIPEDIA ×4. Ages 21–41.
Name disambiguation: `Natsumi Saito (斎藤夏美)` / `Natsumi Saito (斉藤夏海)` (both in batch), `Yui Koike (小池由)` (≠ W-2026-1900 小池唯).
Validator gotcha (again): keep Q-IDs / digit strings out of the 45 chars after "DOB" in evidence text. errors=0.
Spot-checks 10/10 (`urls/s31_spotcheck.url`).

## Catalog after this session
**2441** entries, **2249** social, **192** reference, **409** review, **33** IRR. Directory 159 known / 2,090 unknown pages.

## Next
ja `OFFSET 300` (≈6 more pages of 150), then zh / es / id / ko slices. Next IDs W-2026-2443 / R-2026-422 / IRR-…-034.
