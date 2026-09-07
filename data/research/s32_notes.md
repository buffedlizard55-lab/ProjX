# Session 32 (2026-09-06)

Wikidata model pool — **Japanese-Wikipedia slice, page 3 (OFFSET 300)**, line-by-line ja-wiki lead verdicts. Continuation of Sessions 30–31.

## Harvest
- `urls/s32_model_jawiki_off300.url` (same query, `LIMIT 150 OFFSET 300`) → `s32_raw/model_ja3_chunk0..2.txt` → `model_ja3_rows.json` (150)
  → `model_ja3_people.json` (150 unique) → `model_ja3_new.json` (140 after Q-ID / handle / title dedup; 10 known).
- Page ends at **Q11648411** (鈴木あや). Next page = `OFFSET 450`.
- Glued-TikTok repair: split the wiki URL at the first character that is neither a `%XX` byte, a `_` before `%`/`(`, nor a `(...)` group; the remainder is the TikTok handle (20 rows this page, 0 rejects).
- Labels: `urls/s32_ja_labels_140.url` → `s32_raw/ja_labels_chunk0..1.txt` → `ja_labels.json`.

## Verification
- `urls/s32_jawiki_extract_batch0..6.url` (+ `s32_jawiki_extract_extra.url`, exsentences=6, for 沢井彩華 / 瀬戸サオリ whose first sentence was truncated) → `s32_raw/jawiki_b0..b6.json`, `jawiki_extra.json` → `model_ja3_checked.json` (134 match / 3 no full date / 3 conflict).
- Date regex now tolerates era annotations in both fullwidth and ASCII parentheses with spaces: `1989年 (平成元年) 3月10日`.
- `scripts/session32_verdicts.py` → `verification_s32_log.tsv` (140: 111 PROMOTE / 29 REVIEW) + `s32_verify_buckets.json`; includes a DATE_RE pre-check assertion (0 risks).
- Apply: `scripts/session32_apply.py` (copy of session31_apply with s32 paths / IDs / IRR-034) — dry-run then live.

## Result
+111 entries W-2026-2443..2553 (111 IG / 10 TT), +29 queue R-2026-422..450 (24 scope-ambiguous, 3 AGE_PARTIAL, 3 DOB_CONFLICT), IRR-2026-09-06-034.
Flags: AGE_EVIDENCE_WIKIPEDIA_ONLY ×111, NAME_ALIAS_IN_WIKIPEDIA ×4. Ages 19–41.
New precedent: "former-activity-only" leads (all occupations 元, no current activity) → REVIEW scope-ambiguous, not PROMOTE.
DOB_CONFLICT (no value chosen): Q11558750 Emily Kaiho (lead 1983 / WD 1986), Q11566688 Mayu Seto (lead 1989 / WD 1985), Q11609105 Akari Mizuki (lead 1985 / WD 1987).
Name disambiguation: `Risa Watanabe (渡辺リサ)` (≠ R-2026-069 Sakurazaka46 idol), mononyms Kikka / Mana / Miyu / Satoumi with "(kanji, model)".
Spot-checks 10/10 (`urls/s32_spotcheck.url`). Validator errors=0 first try.

## Catalog after this session
**2552** entries, **2360** social, **192** reference, **438** review, **34** IRR. Directory 159 known / 2,201 unknown pages.

## Next
ja `OFFSET 450` (≈5 more pages of 150), then zh / es / id / ko slices. Next IDs W-2026-2554 / R-2026-451 / IRR-…-035.
