# Session 18 (2026-09-07)

Goal: +100 unique Instagram/TikTok profiles in fashion / fitness-model / modeling
after volleyball 2003–08 IG/TikTok saturation.

## Method
Wikidata P106 sweep: female items whose occupation is model (Q4610556), fashion
model (Q3357567), personal trainer (Q762121), bodybuilder (Q15982795) or fitness
model (Q124408963); DOB 1985–2008; Instagram or TikTok handle; P854 reference URL
**or** English Wikipedia sitelink; pornographic-film (Q488111) and erotic-
photography (Q3286043) occupations excluded. Queries:
`data/research/urls/s18_prom_off{0,50,100,150,200}.url`.

Q-ID extraction uses `REPLACE(STR(?p), "http://www.wikidata.org/entity/", "")`
— never `SUBSTR(..., 34)`.

## Outcome
- Promoted: **138** (W-2026-1189..1326). Audit: `s18_selected.tsv`.
  Master: `s18_master.tsv` (138 unique QIDs). Builder: `scripts/session18_build.py`.
- Queued: **8** (R-2026-146..153) — six AGE_CONFLICTING_VALUES, Nanami Sakuraba
  NAME_MISMATCH_IN_CITED_SOURCE, Dana Heath AGE_SOURCE_IDENTITY_UNRESOLVED
  (Wikipedia sitelink redirects to the Nickelodeon series *Danger Force*).
- IRR-2026-09-07-023: exclusions (babesdirectory/listal/mypmates/reddit never
  used as age evidence; Swayam Bhatia 2007-10-08 minor; Charlbi Dean and
  Nightbirde deceased; Anllela Sagra already catalogued).
- Catalog after split: **1325** entries, **1133** social, **192** reference,
  **141** review, **23** IRR. Validator errors=0.

## Spot-checks (opened pages matched)
- Sita Abellán Wikipedia 27 March 1993
- Jade Cargill Wikipedia 3 June 1992
- Amandine Petit Wikipedia 30 September 1997
- Kaycee Rice FamousBirthdays 21 October 2002

## FamousBirthdays profession pages
- `/profession/model.html` chunk 0: celebrity-dominated; **minors skip**
  Ava/Leah Rose Clements 16, Ella Gross 17, Ülkü Hilal Çiftçi 17.
- Confirmed 404s (do not retry): `/categories/swimwear.html`,
  `/profession/swimsuit-model.html`, `/profession/swimsuitmodel.html`,
  `/profession/fitnessmodel.html`, `/profession/fitness.html`.

## Still unfetched / uncatalogued
- Promo SPARQL OFFSET 250 and 300 (URL files exist).
- `s18_inf_off*` influencer occupation queries (not fetched).
- `s18_fm_off120` failed once (one retry allowed); off160/200 not fetched.
- Handle-lookup ground-truth map (Sayaka Nishiwaki, Chika Arakawa, …) still
  uncatalogued — rewrite if a later pass uses `s18_master` for that pool.
- Volleyball 2003–08 IG/TikTok: exhausted. Do not retry P854 GROUP BY LIMIT 50
  OFFSET 0.

## Transport
fetch_page only. No raw HTTP from this environment (curl SSL_ERROR_SYSCALL).
