# Session 20 (2026-09-06)

Instagram/TikTok directory lockstep + fashion/fitness-model Wikidata P106 OFFSET 450.

## Site
- Directory CTA at the top of the main site: banner, nav `Instagram / TikTok directory`, hero primary.
- Same nav-cta on `reference.html` and `directory/index.html`.
- Profile pages (`directory/W-2026-*.html`) now include the same nav-cta.
- `scripts/session15_split.py` rebuilds `directory/` via `scripts/build_directory.py` unless `--no-directory`.

## Backfill
- `scripts/backfill_ig_tt_accounts.py` copied already-stored Instagram/TikTok source URLs into `socialAccounts` for 19 early social rows (W-2026-008/009/015/016/018–029/032–034).
- Handles taken only from those URLs. Counts: `FOLLOWER_COUNT_UNKNOWN`.

## Wikipedia handle harvest (existing reference rows)
Opened pages; retrieved content had **no** instagram.com / tiktok.com profile URL. Handles were **not** invented; rows stay `catalogType=reference`:
- Paige Bueckers, Aryna Sabalenka, Liv Morgan, Hilary Knight, Shilese Jones.

## SPARQL OFFSET 450
- Query: `data/research/urls/s18_prom_off450.url`
- Master: `data/research/s20_master.tsv` (39 unique QIDs)
- Promoted **39** (W-2026-1456..1494). Audit: `data/research/s20_selected.tsv`.
- Queued 0. Skipped 0.
- IRR-2026-09-07-025.

## Spot-checks
Deva Cassel 2004-09-12, Tao Tsuchiya 1995-02-03, Becky Armstrong 2002-12-05 — all matched.

## Flags / exclusions
- Gwendolyne Fourniol 2000-01-01 → `DOB_JAN1_POSSIBLE_YEAR_PRECISION`.
- NAME_ALIAS_IN_WIKIPEDIA: Rebecca Patricia Armstrong / Becky Armstrong; Rina Sawayama / Rina Sawayama (model); Kaede / Kaede (dancer); ELLI-ROSE / Elli Rose; Sofía Depassier / Sofia Depassier.
- Aubri Ibrag P854 `famousbirthdays.com/people/amina-ibrag.html` names a different given name — **not** used as age evidence; English Wikipedia used instead.
- babesdirectory / listal / pornhub / Playboy-magazine never used as age evidence.
- fm_off120 Playboy-adjacent pool not auto-promoted.
- Dana Heath not restored.

## Catalog after this session
**1493** entries, **1301** social, **192** reference, **142** review, **25** IRR.

## Still open
influencer OFFSET 40/80; fm_off160/200; promo OFFSET 500+. Volleyball IG/TikTok structured population exhausted.
