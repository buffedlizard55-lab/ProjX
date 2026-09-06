# Session 18 reconnaissance (2026-09-07, after session 17 commit c1437bb)

Goal: next +100-profile pass over the fashion/fitness focus categories
(swimwear, bikini/beachwear, fitness model, modeling) from FamousBirthdays
(the directory sessions 8-14 used for W-2026-8xx entries).

## Confirmed URL scheme (probed live 2026-09-07)
- Person pages: https://www.famousbirthdays.com/people/<slug>.html
  (verified: olivia-ponton.html renders full profile).
- Person pages expose: profession link, exact birthday (month day + year), age,
  birthplace, "About" text with publicly-observed rounded follower counts
  ("over 2.7 million followers", "over 7 million fans on TikTok") - the
  evidence format already used by catalog entries W-2026-8xx.
- Profession pages exist at /profession/<slug>.html with NO hyphens and
  NO spaces, e.g. /profession/instagramstar.html (linked from person pages).
- 404 probes (do NOT retry these exact slugs):
  /categories/swimwear.html, /profession/swimsuit-model.html,
  /profession/swimsuitmodel.html, /profession/fitnessmodel.html.

## Next steps (session 18 proper)
1. Slug discovery: open person pages of already-catalogued fitness/model
   creators (e.g. natasha-aughey, kyla-dodds, victoria-xavier) and read their
   profession-group links (fitness instructor? model? instagramstar?).
2. Fetch /profession/model.html + the fitness profession page(s); persist each
   response IMMEDIATELY to data/research/s18_prof_<slug>.txt (same
   fetch->save discipline as s17; save before the next fetch).
3. Build s18 pool: female, 18+, IG/TikTok-bearing; dedupe vs catalog names,
   handles, FB person URLs already cited (843+ FB-cited entries exist, so
   expect heavy dedupe - lesser-known/low-rank profiles are the priority).
4. Per-candidate verification fetch of their person page (birthday + age +
   handles + follower observation), one fetch per candidate, saved to
   data/research/s18_ppl/<slug>.txt before moving on.
5. Then Wikidata is EXHAUSTED for volleyball (occupation/sport sweeps s13-s16
   + club-roster sweep s17 all done); fashion/fitness FB sweep is the growth
   area, plus European volleyball leagues via volleybox (s13 pattern) if new
   names surface.

## State at handoff
- Catalog: 1187 entries (995 social + 192 reference), 133 review, 22 IRR;
  validator errors=0; commit c1437bb pushed on arena/01a077e7-projx.
- Next identifiers: W-2026-1189, R-2026-146, IRR-2026-09-07-023.
- s17 master statuses: 202 umbrella-only, 8 sport-conflict, 4 volleyball
  (3 promoted + 1 queued), 13 volleyball-no-label (Belarusian roster cohort,
  future label pass).
