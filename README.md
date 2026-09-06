# ProjX

ProjX is a static GitHub Pages site for a **verified directory workflow**: real, adult (18+)
*women* who are public figures and professionals — working models, athletes, creators, and
similar public pages — included only when each record carries official or trusted age *and
gender* evidence, official reviewable links, and line-by-line verification notes. The master
database is **women-only** by hard rule: every record must represent a woman with reliable
public gender evidence (first-party bio, official site, agency, sports-org bio, reputable
interview/publication) — never appearance, clothing, name, or AI analysis.

## Scope guardrails

Discovery may be **systematic** (public structured-data queries over federation, league, club, university and
volleyball-database records — see `docs/verification-protocol.md` §“Structured public-data discovery”), but
**acceptance is never bulk**: social platforms are never scraped, no access control is bypassed, and every row is
verified individually with its own cited age and gender evidence, a dedupe check on name *and* every handle, and
`UNKNOWN` instead of a guess for anything not observable. The site and data model only accept records when the
person is:

- a real, non-AI individual **and is a woman** with reliable public gender evidence (see
  `docs/verification-protocol.md` §2 — not inferred from appearance, clothing, body shape,
  name, AI image analysis, or username);
- confirmed 18+ through an official or trusted public biographical source (never inferred from
  appearance, “college girl” status, content, school year, or follower counts);
- operating a public-figure/professional page in an objective category (Model, Fitness,
  Athlete, Fashion, Lifestyle, Creator, Entertainment, College athlete, Public personality,
  Other — never “hot/sexy” ranking) or clearly opted in — private individuals are never
  inferred into the table; men, couples, group/org accounts, and gender-ambiguous profiles
  without reliable evidence are explicitly excluded;
- represented by direct official links (official, verified-platform, agency, press, or
  age-evidence) suitable for manual review under the 3-tier source hierarchy; and
- reviewed line by line, with missing or ambiguous evidence recorded as a flagged
  irregularity (`GENDER_UNVERIFIED`, `AGE_UNVERIFIED`, `IDENTITY_UNCERTAIN`, etc.) instead of
  a guessed catalog row.

Bulk autonomous collection of real people's profiles into a searchable directory is
intentionally not implemented, even when reframed with objective categories. On 2026-09-06
three requests for ~1,000 women-focused entries were reviewed and logged as blocked
irregularities `IRR-2026-09-06-002`, `IRR-2026-09-06-003`, and `IRR-2026-09-06-004` (the last a
detailed women-only spec with line-by-line checks and a “quality over quantity” rule); see
[docs/review-log.md](docs/review-log.md). After owner confirmation (“yes” on 2026-09-06) to
proceed with the compliant alternative, **4 initial verified women** (Serena Williams, Simone
Biles, Naomi Osaka, Alex Morgan — professional athletes, each with official/Tier-1 age,
gender, identity and category evidence) were added per `data/catalog.json` as a demonstration;
quality and verification take priority over quantity. Sessions 05–07 expanded the set
iteratively via activity-first discovery (fitness/swimwear/athletics → verify eligibility),
maintaining **two distinct datasets**: `VERIFIED` and `REVIEW_REQUIRED` — promising but
incomplete candidates are never discarded, always flagged (`AGE_UNVERIFIED` etc.) and queued
for further research. **Session 08 (2026-09-06, up-to-1,000 target reaffirmed with
quality-over-quantity)** added **21 more line-by-line verified women (W-2026-014..034)**,
**Session 09 (2026-09-06)** added follower-count schema/fields + website follower filter/sort/distribution UI, backfilled publicly observed counts for existing rows (never estimated), and **+12 verified women (W-2026-035..046)** including IFBB Bikini Olympia athletes, Monday Swimwear co-founders, Blogilates, and Nebraska WBB college athlete Kendall Coley (~4K IG — small-creator priority). Catalog reached **46 VERIFIED** and **9 REVIEW_REQUIRED**. **Session 10 (2026-09-06)** continued activity-first research with second-pass verification: **5 queue promotions** (Melissa Bender DOB 1983 via 2 biographies; Kahdia via explicit '25-year-old' she/her profile, IG 6,604 recorded exactly; Olivia Vance DOB 2001 via volleybox + two athlete profiles; Emersen "Emmy" Schrom DOB 2006 via Tier-1 Duquesne roster; Jade Haliburton née Jones — surname conflict resolved, DOB 1998) and **+4 newly discovered verified creators** (Jen Selter DOB 1993 x5 sources; Paige Hathaway DOB 1987 x5 sources; Joan MacDonald DOB 1946 + GMA/BI/KPRC press ages — senior-creator diversity; Sarah Stevenson "Sarah's Day" DOB 1992 x5 sources). Remaining 4 queue items enriched with new evidence (nothing guessed). Website gained follower-distribution **by-category and by-platform** breakdown panels. Catalog now **55 VERIFIED** and **4 REVIEW_REQUIRED** (**8 irregularities** for manual review).

**Session 11 (2026-09-06)** continued the activity-first expansion push toward ~100 verified profiles, in two batches of newly audited research: **Batch 1 (+23, W-2026-056..078)** — fitness/fashion creators (Anllela Sagra 27.1M IG; Katya Elise Henry 7.8M; Amanda Elise Lee 11M+; Mia Sand; Dee Marie Ditt; Clara Lindblom; Yovanna Ventura 5.3M+), volleyball (Kathryn Plummer 42.4K; Andrea Drews; Justine Wong-Orantes 55K; Winifer Fernández 24K), women's Valorant esports (Petra Stoker; Sarah "sarahcat" Simpson — Liquipedia-sourced DOBs), surfing (Caroline Marks; Tatiana Weston-Webb — WSL Tier-1 bios), WNBA (Kysre Gondrezick 598K; Didi Richards 146K), CrossFit/fitness (Dani Speegle; Demi Bagby 2.7M), beach volleyball (Sara Hughes; Kelly Cheng — FIVB/USAV/AVP Tier-1), SI Swimsuit cover model Brooks Nader, and swimmer Regan Smith (Olympedia Tier-1). **Batch 2 (+22, W-2026-079..100)** — YouTube fitness/yoga creators (Adriene Mishler 13M+; Maddie Lymburner "MadFit" 7.3M+; Natacha Océane 1.6M+; Chloe Ting 26.1M; Anna Engelschall "growingannanas" 7M+; Caroline Girvan 4M, snapping a Wikipedia source), artistic gymnasts (Suni Lee; Livvy Dunne 8M TikTok/5.4M IG; Jordan Chiles live displays IG 2M/X 100.4K/FB 82K; Jade Carey), long jump queen Tara Davis-Woodhall (live IG 1M, Threads 284.6K, plus noted joint account), heptathlon/hurdles (Anna Hall; Masai Russell), golf Nelly Korda, tennis Iga Świątek/Emma Raducanu (WTA official), soccer Trinity Rodman (Britannica), basketball Paige Bueckers/Angel Reese, and swimmers Kate Douglass/Torri Huske (live IG 108K)/Gretchen Walsh. Every row carries per-platform publicly-observed counts only — never estimated, never summed (41 profiles have genuinely unknown follower ranges and are recorded as UNKNOWN rather than guessed). Three DOB-year conflicts (Mia Sand, Dani Speegle, Brooks Nader — adult either way), a Jade Carey handle anomaly, and snapshot variances are logged as **IRR-2026-09-06-009/010**. Catalog reached **100 VERIFIED** and **4 REVIEW_REQUIRED** (**10 irregularities** for manual review).
**Session 12 (2026-09-06)** answered the follow-up request to *speed up search and verification without skipping line-by-line checks* through a new **reusable validator (`scripts/validate_catalog.py`)**, structured/Tier-1 pipelines (volleybox/volleyballworld JSON-LD, FBref/basketball-reference DOB+IG single views, FotMob/leaderbiography/Red Bull JSON-LD, official league/team pages), UNKNOWN-count honesty instead of extra fetch rounds, and id-asserted batch scripts. Four audited batches added **+38 verified women (W-2026-101..138)**: USWNT & legacy US soccer (Girma, Swanson, Smith, captain Lindsey Heaps née Horan — live IG 406K, Naeher, Lavelle, Dunn, Davidson, Fox, Sonnett, Shrader née Albert, Coffey), US volleyball (Robinson Cook, Bartsch-Hackley, Larson, Thompson), WNBA/cross-sport (Clark, Gauff, Sabalenka, Richardson, McLaughlin-Levrone, Carissa Moore, A'ja Wilson, Knight, Coyne Schofield), WWE champions (Ripley, Belair, Lynch, Flair, Bayley, Liv Morgan), UFC champions (Grasso, Namajunas), skiing Vonn, swimmer Manuel, striker Sam Kerr, surfer Gilmore, climber Garnbret. The dup-guard caught **13 big-name re-verifications already in catalog** (excluded rather than duplicated), every approximation is verbatim/rounded or UNKNOWN (never invented), and day-level DOB/place/handle variances are logged as **IRR-2026-09-06-011..014** (14 irregularities total, none blocking). Catalog now **138 VERIFIED** and **4 REVIEW_REQUIRED**; validator reports **errors=0**.

**Session 12 continuation (2026-09-06, batches E–P)** kept the accelerated pipeline and added **+52 more verified women (W-2026-139..190)** across twelve audited batches: NWSL/USWNT roster runs (+14), a WNBA roster run via basketball-reference (+6), track & field via World Athletics/European Athletics official profiles (+6), LPGA golf (+4), USWNT legacy tier (+4), WWE champions wave 2 (+4), US volleyball via volleybox/volleyballworld structured JSON-LD (+4), WTA tennis (+4), women's swimming via olympics.com.au/nbcolympics structured bios (+2), US gymnastics via members.usagym.org official athlete profiles (Konnor McClain with self-registered socials + live X count 1,786; Shilese Jones IG count held in notes only — no handle captured) (+2), and women's football via players.fcbarcelona.com official club bios (3x Ballon d'Or winner Aitana Bonmatí; Caroline Graham Hansen) (+2). The dup-guard prevented **9 more re-additions** across E–P (e.g. Kelsey Robinson Cook, Kate Douglass, Gretchen Walsh, Suni Lee via URL-guard) — every script asserts id + displayName + source-URL uniqueness before touching the catalog, and the validator still reports **errors=0** before every commit. Session 12 total: **+94 verified profiles** (96 → 190). A second continuation (batches Q–V) added **+10 more verified women (W-2026-191..200)** — PWHL hockey (Sarah Fillier via the official pwhl.com athlete page), WSL surfing (2025 world champion Molly Picklum via the official WSL bio + Red Bull structured data), F1 Academy champion Abbi Pulling, skateboarder Rayssa Leal (verified 18+ via Britannica’s explicit age plus published DOB), rugby star Ilona Maher (IG/X handles via structured sameAs), alpine legend Mikaela Shiffrin, USC basketball’s JuJu Watkins (official USC roster prose DOB + structured IG/X sameAs), freestyle skier Eileen Gu, cricketer Smriti Mandhana and badminton double-Olympic-medalist PV Sindhu. 3 more dup catches (Naomi Osaka, Faith Kipyegon, Femke Bol) and two DOB outliers resolved against official sources. **Catalog milestone: 200 VERIFIED** and **4 REVIEW_REQUIRED**; irregularities remain **15**.

**Session 13 (2026-09-06, UPDATED)** answered the owner's volleyball-only directive (NCAA indoor → beach volleyball → European leagues → any other women's leagues; "aim to add 100 new... work until the search is complete and thorough; verify no hallucinations"). Batches G–W had already reached **201** before the pivot (gymnastics: Shilese Jones & Konnor McClain — USAG official bio, live X 1,786; football: Bonmatí & Graham Hansen — official Barça bios; PWHL Fillier; WSL champ Picklum; F1 Academy champ Pulling; skater Leal; Maher; Shiffrin; Watkins; Gu; Mandhana; Sindhu = 200 milestone; Katie Taylor = 201). The volleyball sprint then added **+41 verified women (W-2026-202..242)**: NCAA indoor stars (Murray, Babcock, Reilly, Hudson, Mruzik — live X 1,334, Rubin, DeBeer), beach NCAA then pro (Nuss-Cruz, Kloth-Brasher, Kraft, Cannon, Maple, Scoles, Denaburg, Anderson — official USC/FSU bios with structured IG/X handles), US pro leagues (O'Neal — live X 4,606, Beason, Rodriguez, White — lovb/auprosports/provolleyball official) and European/international league stars across IT/TUR/SRB/POL/NED/GER/CAN/JPN/DOM/BRA/SWE (Orro, Güneş, Haak, Wołosz, Antropova, Bosetti, Omoruyi, Lubian, Bošković, Stysiak, Vargas — IG+YT, Karakurt, Koga — IG 650K rounded via famousbirthdays, Castillo, Ognjenović, Van Ryk, Lippmann, Weitzel, Gabi Guimarães, Ana Cristina Souza). Pipelines: volleybox/beach.volleybox JSON-LD (birthDate + gender Female + sameAs handles), volleyballworld/CEV/FIVB official registries, official club pages (Imoco, Vakıfbank), AVP/LOVB/PVF official athletes, university and national-federation bios (USC, FSU, Michigan, Louisville, Volleyball Canada). Validator at **errors=0** for every commit; one drafting artifact self-caught in W-2026-225's notes and fixed in a dedicated honesty commit; conflict flags noted in-entry (Karakurt year outlier, Buijs birthplace variance). Review queue 4→5 (R-2026-014 Kami Miner, AGE_UNVERIFIED — official roster silent on DOB). Catalog state at end of volleyball sprint **301 VERIFIED** and **5 REVIEW_REQUIRED** (Kami Miner's R-2026-014 still pending); irregularities remain **15**.

**Session 13 update (waves 28-48)**: the volleyball sprint continued from 242 to **301 verified** (+59 further since the paragraph above, for +100/100 — GOAL REACHED at W-2026-301 (wave 48)): additional NCAA indoor (Franklin — 2023 AVCA National POY, Stafford), NCAA beach (Newberry, Whitmarsh, Simo, DeBerg), PVF/LOVB-US pros (Sponcil — dup-block handled for Poulter W-2026-180, Monserez, Grubbs, McGraw, Bergmark), international leagues (Herbots BEL, Miyabe JPN, Montibeller BRA — sportsxm 1.2M IG noted, De la Cruz DOM, Li CHN, Gicquel FRA — CNOSF structured handles, Cazaute FRA, Baladın & Cebecioğlu & Özbay & Aydemir TUR, Ungureanu ROU, Pietrini & Gennari & Sylla ITA, Stigrot & Kästner & Pogany GER, Lohuis & Baijens & van Aalen NED, Van Avermaet BEL, Herbots, Stevanović & Aleksić & Kurtagić SRB, Schoon & van Driel NED beach, Wilkerson & Humana-Paredes CAN — official federation + AVP, Ana Patrícia & Duda & Tainara & Bergmann BRA — Olympic gold, Koga & Hayashi & Nagaoka JPN, Graudina & Samoilova LAT — beach world champs, Erdem & Czyrniańska & Butigan & Planinšec & Korneluk). Multiple dup-block saves recorded (Stysiak→W-2026-228, Poulter→W-2026-180, Koga→W-2026-231 with X-handle consolidation, surname-only check Dani Drews vs Annie Drews). Validator errors=0 for every commit; follower counts kept in notes-only where third-party-reported; MINUTE flags on Cazaute/Sponcil/Cebecioğlu/Stigrot minor-DOB-conflict entries.
**Session 13 continuation (2026-09-06, structured-data volleyball pass)** took the owner's directive — *college
sports first (NCAA volleyball, beach volleyball), then European volleyball and any other women's volleyball leagues;
add ~100 new unique profiles per pass and keep searching until the search is honestly complete; verify no
hallucinations* — and ran an exhaustive sweep of the **publicly documented + publicly social** women's volleyball
population rather than a sample: three Wikidata SPARQL pools (female volleyball players in US women's college teams
with an Instagram handle; female beach volleyball players with any public handle; female indoor players in
international leagues with an Instagram handle, all in the adult birth-date window) produced **279 candidates**, every
one of which was then resolved to the *reference of its own date-of-birth statement* (`S` named database, `U`
reference URL, `I` import provenance), to its English Wikipedia article (`W`), to its team memberships (`T`) and to
its X/TikTok/Facebook/YouTube handles. Outcome: **+257 verified women (W-2026-302..558)** — 142 citing an external
reference URL (Big Ten/SEC/ACC/Pac-12 university athletics rosters, CEV, FIVB/Volleyball World, the German
Bundesliga, Slovak/Swedish/Norwegian/Dutch/Spanish/Belarusian/Turkish/Brazilian/Canadian/Japanese federations and
leagues, Olympedia, women.volleybox.net, bvbinfo.com), 54 of them also with an English Wikipedia article, 25 more on
Wikipedia alone, and 92 promoted **with the flag `AGE_EVIDENCE_SECONDARY_SOURCES`** because their birth date is
referenced to a named database that attaches no URL (a human click-through is still owed). **19 candidates were
refused promotion** and queued as `AGE_SOURCE_NOT_RECORDED` instead of being guessed, 3 handle-less candidates were
dropped, and the dup-guard found no collisions with the existing 301 rows. A four-way spot-check audit opened the
primary pages (English Wikipedia, women.volleybox.net, bvbinfo.com, a Louisville athletics roster) and matched every
published field exactly; one self-caught integrity event (16 team labels drafted from inference during transcription)
was detected and deleted before generation and is logged as **IRR-2026-09-06-017**. Follower counts stay honest:
Instagram/TikTok/X/YouTube/Facebook refuse automated retrieval here, so only three publicly displayed analytics
snapshots were captured (@a.fed.10 346,337; @mhicaelabelen 431,914; @elenaascott 93,568 — each `countType: exact`
with its snapshot date) and the other 254 rows keep `FOLLOWER_COUNT_UNKNOWN` / `FOLLOWER_RANGE_UNKNOWN` with a
`sourceNote` explaining why. Reproducible artifacts: `scripts/session13_volleyball.py` (dry-run by default),
`scripts/session13_followers.py` (id+name+username asserted), `data/research/s13_selected.tsv` (per-entry audit
sheet), `data/research/s13_*.tsv` + `data/research/urls/*.url` (raw harvest and the exact queries). Validator
`errors=0` at every step; catalog **558 VERIFIED / 24 REVIEW_REQUIRED / 17 IRR**.

**Session 16 (2026-09-07, deep Wikidata sweep)** ran the "keep searching" request to a structured
conclusion: instead of re-querying single birth-year bands, the whole female volleyball /
beach-volleyball population was enumerated via its graph (occupations Q15117302/Q17361156, sports
Q1734/Q4543, plus the Instagram/X/TikTok follow-graphs of the beach scene), then every candidate was
re-fetched item-by-item for name, DOB, handles, citizenship, sex/gender, birth-date references,
English-Wikipedia sitelinks and NCAA roster rows (queries archived in `data/research/urls/s16_*.url`,
raw harvest in `data/research/s16_*.txt`, collapsed master `data/research/s16_master.tsv`,
per-entry audit `data/research/s16_selected.tsv`). Result: **+341 verified profiles
(W-2026-845..1185: 4 NCAA, 112 beach, 225 European/international indoor; 311 with Instagram/TikTok
published records, 30 X-only reference profiles)**, **+46 REVIEW_REQUIRED rows** (R-2026-098..143,
all `AGE_SOURCE_NOT_RECORDED` — DOB present but no reference/URL/sitelink, never guessed), 24
duplicate-QID and 34 duplicate-name/handle skips (Charlotte Flair W-2026-127 and Abby Hornacek
W-2026-675 correctly re-found and kept single). Evidence tiers per IRR-2026-09-07-020; category
extensions only from occupation statements (model → Modeling, personal trainer/bodybuilder →
Fitness; dual beach+indoor statements get both sport tags). Data-shape flags on affected entries:
SUSPECT_HANDLE_VERIFY_FORMAT (Q98082815, Q110272655), DOB_JAN1_POSSIBLE_YEAR_PRECISION (4),
NAME_ALIAS_IN_WIKIPEDIA (Q19577569 Pischke/"Taylor Wilson"), NON_ENGLISH_LABEL_SOURCE (3),
COUNTRY_NOT_RECORDED, AGE_EVIDENCE_NAMED_SOURCE_ONLY, CONFLICTING_IG_STATEMENTS — all listed in
IRR-2026-09-07-021. The TikTok-only band was finally resolved: the archived query was malformed (UNION group after
the FILTER), not an endpoint failure; the corrected query returned exactly 3 QIDs — all already
catalogued — so that population is confirmed exhausted. Validator errors=0 (1184 entries /
131 review / 21 irregularities); `session15_split.py` re-derived the social/reference partition
(992 social + 192 reference = 1184). A pre-existing validator crash on `largestPublicFollowing: null`
(null-guard fix) was found and fixed. No follower counts were publicly observed for this batch:
every count recorded as FOLLOWER_COUNT_UNKNOWN / FOLLOWER_RANGE_UNKNOWN — never estimated.

**Session 18 (2026-09-07, fashion / fitness-model Wikidata P106 sweep)** pivoted after volleyball
2003–08 Instagram/TikTok saturation: female items whose occupation is model, fashion model,
personal trainer, bodybuilder or fitness model, with a documented DOB 1985–2008, an Instagram
or TikTok handle, and a P854 reference URL or English Wikipedia sitelink (pornographic-film and
erotic-photography occupations excluded). Queries `data/research/urls/s18_prom_off*.url`; master
`data/research/s18_master.tsv`; builder `scripts/session18_build.py`; audit
`data/research/s18_selected.tsv`. **+138 verified (W-2026-1189..1326)**, all Instagram/TikTok so
they stay on the Published catalog (**1325 VERIFIED / 1133 social / 192 reference**). Spot-checks
matched Sita Abellán (27 March 1993), Jade Cargill (3 June 1992), Amandine Petit (30 September 1997)
and Kaycee Rice (21 October 2002). **8 queued (R-2026-146..153)** rather than guessed (conflicting
DOBs, Nanami Sakuraba vs Hitomi Miyauchi, Dana Heath sitelink redirecting to *Danger Force*).
Exclusions in IRR-2026-09-07-023: babesdirectory/listal/mypmates/reddit never used as age evidence;
Swayam Bhatia (2007-10-08) skipped as a minor; Charlbi Dean and Nightbirde deceased; Anllela Sagra
already catalogued. Validator **errors=0** (1325 / 141 review / 23 IRR). Modeling 73→210, Fashion
38→174. Follower counts unobserved — FOLLOWER_COUNT_UNKNOWN / FOLLOWER_RANGE_UNKNOWN.

**Session 19 (2026-09-07, fashion/fitness continuation OFFSET 250–400)** kept searching the same
P106 pool past the Session 18 cutoff. Queries `s18_prom_off{250,300,350,400}.url` plus influencer
P854 slice `s18_inf_off0.url`. **+129 verified (W-2026-1327..1455)**, all Instagram/TikTok
(**1454 VERIFIED / 1262 social / 192 reference**). Spot-checks matched Harnaaz Sandhu (3 March 2000),
Doutzen Kroes (23 January 1985) and Nagi Inoue (17 February 2005). Andrea Aguilera skipped as a
name duplicate. **R-2026-154 Wioleta Psiuk** queued for three conflicting P569 dates. Minors not
added: Havan Flores (2007-11-20) and Akari Toyofuku (2008-12-14). babesdirectory / listal /
pornhub / Playboy-magazine citations never used as age evidence. Validator **errors=0**
(1454 / 142 review / 24 IRR). Modeling 210→335, Fashion 174→299. Volleyball 839 unchanged
(2003–08 IG/TikTok still exhausted).

**Session 15 (2026-09-07, Instagram/TikTok split)** answered the request to keep **only profiles
with an Instagram or TikTok account** in the primary "Catalog / Published records" table, moving
everything else (Wikipedia, personal/agency websites, X, YouTube, Facebook, press, or no public
social account) to a separate **Reference profiles** subpage. Every entry stays in the single master
`data/catalog.json` (no data loss) and is tagged with a computed `catalogType`: **social** (681,
has a documented Instagram or TikTok profile) or **reference** (162, no Instagram/TikTok — documented
via Wikipedia/website/X/YouTube/Facebook/press). A derived `data/catalog-reference.json` (162 rows,
independent feed) powers the new `reference.html` subpage; the frontend was refactored into a shared
`assets/catalog.js` driven by `<body data-view="catalog|reference">`. `scripts/session15_split.py`
(no dry-run by default, `--dry-run` to preview) recomputes the tags idempotently. Hallucination
audit: 0 platform/host mismatches, 0 required-field gaps, split is a pure partition
(681 + 162 = 843, no entry appears on both sides, no entry lost), validator errors=0 for both the
master and the reference file.

**Session 14 (2026-09-07, saturation audit + creator push)** confirmed the documented volleyball
population is now essentially exhausted: a structured-data re-enumeration of the female indoor + beach
cohorts returned 34 curated candidates, **32 of which were duplicate-name** already catalogue rows, and
yielded only **2 genuinely new beach-volleyball players** (Denyse Mutatsimpundu W-2026-742 — a lesser-known
Rwandan regional beach player, and Charlotte Sider W-2026-743 — Canada via the official volleyball.ca
reference) before the catalog already held **500 Volleyball + 76 Beach Volleyball** rows. Discovery therefore
pivoted to the under-covered fitness / bikini / swimwear-fashion / modeling / lifestyle creator categories,
adding **43 line-by-line verified creators (W-2026-744..785, minus the demoted W-2026-752)** — fitness &
wellness athletes (Natalie Matthews, Shanique Grant, Ariel Khadr, Angelica Teixeira, Renee Jewett,
Francielle Mattos, Andrea Shaw, Melissa Truscott, Vanessa Christine, Casi Davis), bikini/each IFBB bikini
competitors (Courtney King, Janet Layug, Beatriz Biscaia), college-athlete-turned-fitness-creators (Jordan
Edwards, Brittne Babe), and swimwear / bikini-fashion / modeling / lifestyle creators (Bianka Wieland, Jade
Ramey, Kayla Davies, Bruna Lima, Kirsten Wright, Sabrina Sablosky, Jessica Bartlett, Summer Lopez, Summer
Bianca, Samyra Miller, Behwah, gissydoll, Mazzy Joya, kikiiib, _tk_fit_, Summer_fit, Ashley Garcia, Emma Kotos,
Heather Summers, Brittany Williams, Meg Kylie, Francesca Aiello, Elizabeth LiSi, Summer Harte, __BeingBrittany,
iamnevaehakira) — each with a cited documented DOB + documented woman/gender + real public profile,
pre-checked on name and every handle. Follower counts stayed honest: only publicly observed figures were
recorded (`@roxyqueflexx` 1,009,340 `exact`; `@therealfitnessbeauty` 330K, `@franciellemattos` 1.2M,
`@ifbbmissytruscott` 137K, `@brittnebabe` 1.9M, `@xoobruna` 3.8M, `@kirstentoosweet` 3.4M, `@frankiesbikinis`
1.5M, `@_li.si_` 470K, `@summerharte_` 130K, `@therealnevaehakira` 60K — all `rounded` except the exact
`@roxyqueflexx`), the rest `FOLLOWER_COUNT_UNKNOWN`; never estimated, never summed. A DOB-year conflict on Yarishna Ayala (`DOB_YEAR_CONFLICT`: Famous Birthdays
1991 vs Generation Iron 1992 — adult either way) was **not** promoted: her earlier promoted row was demoted
from the verified catalog and moved to `REVIEW_REQUIRED` (R-2026-097) until the year is reconciled, per the
rule that a DOB-year conflict must be resolved before verification. The creator generator was fixed to
route any `flags`-marked pool entry to the review queue instead of promoting it. A candidate with an
unresolvable 1994/1995 birth date was routed to review rather than guessed, and a glamour/"exotic dancer"
candidate was declined as outside the opt-in public-creator guardrail. Validator: **754 VERIFIED /
85 REVIEW_REQUIRED / 20 IRR, errors=0**; `scripts/session14_build.py` + `scripts/session14_creators.py` are
idempotent, dry-run default, with audit sheets under `data/research/s14_*_selected.tsv`.

bringing the catalog to **34 VERIFIED** (W-2026-001..034) and **9 REVIEW_REQUIRED**
(R-2026-001..012, three promoted after research): new verified rows span fitness and
fitness-model creators (Shay Williams, Dammy Fitness, Alyssa Germeroth, Ashley Flores, Evana,
Summer Fit, Valeriia Litvinova RDN), swimwear/bikini-fashion models (Alyssa Scott, Kiki Ruby,
Kayla Simmons), women's college and pro volleyball/basketball (Lexi Sun — huskers.com Tier-1,
Alexis Dacosta — Auburn official Tier-1, Alyssa Ustby, Victoria Garrick Browne, Sedona Prince —
the latter three **promoted from the review queue** after DOB research), a basketball creator
(Jenna Bandy — NBA Creator Cup), a body-positive surfer (Elizabeth Sneed), a travel/fashion
blogger (Amy Bell), a yoga/wellness creator (Meghan Currie), and women's esports (Michaela
"mimi" Lintrup, Lee "Jennlee" Jeong-hyun — Liquipedia DOBs). Set spans ~2.7K-follower micro
creators to established professionals, ages 22–47, across the US, Brazil, Canada, Scotland,
Denmark, South Korea and Ukraine; two minors discovered during research (Sabre Norris b. 2005,
Sky Brown b. 2008) were **rejected, never added**.

## Site

Plain HTML/CSS/JavaScript, served directly by GitHub Pages from the repository root.
Published at <https://buffedlizard55-lab.github.io/ProjX/>.

- `index.html` — main page and UI shell (Catalog Published records = Instagram/TikTok).
- `directory/index.html` — Instagram/TikTok profile directory (same columns/filters as the catalog, A–Z jump, name links).
- `directory/W-2026-*.html` — one static subpage per social catalog record; rebuild with `python3 scripts/build_directory.py`.
- `assets/styles.css` — responsive styling.
- `assets/catalog.js` — shared renderer (catalog + directory + reference views), driven by `<body data-view="catalog|directory|reference">` and optional `data-base`; handles loading, filtering, sorting, follower distributions, table rendering, and JSON/CSV export.
- `assets/app.js` — superseded legacy renderer; no longer referenced by any HTML (kept only as historical artifact).
- `data/catalog.json` — master entries and irregularities. Now contains **1454 verified women**,
  tagged `catalogType` = social (1262, has Instagram/TikTok) or reference (192, no Instagram/TikTok);
  this single file + `reference.html` + `data/catalog-reference.json` + `data/catalog-social.json`
  + `directory/` implement the Session 15 Instagram/TikTok split and the profile-directory subpages
  (see Session 15 note above). Detail: (W-2026-001..844 as before, plus Session 16's W-2026-845..1185 deep structured sweep; previously W-2026-001..798, with W-2026-752 demoted to REVIEW_REQUIRED — the prior 301 plus Session 13's structured-data volleyball passes: +257 (65 NCAA/US college indoor, 49 international beach, 143 international indoor league players across ~30 countries), +116 in pass 2 (every league and country in the 1996-1999 birth-year band whose item links an Instagram, X or TikTok handle) and +25 in pass 3 (the remaining NCAA/US-college cohort, both disciplines, including players whose only public handle is on X or TikTok — a pass that also showed this college population is now essentially exhausted: 81 of its 120 candidates were already catalogued by Q-ID) and +39 in pass 4 (2026-09-07: international birth-year bands 2000-2002 with no country restriction, the sport-statement-only gap population, the X-only/TikTok-only cohort that the Instagram-centric passes could not return, and — for the first time — a re-test of the review-queue backlog against the same evidence standard, which promoted 2 of its 52 Q-ID-bearing rows). Pass 4 generated 40 and published 39: the 40th was withdrawn by the pass-4 spot-check because opening its single cited primary source showed a page titled “Bamba, Yurika” where the structured record says “Yurika Yokoishi” (same birth date and nationality, different family name), so it was routed to review as R-2026-096 with both names preserved and the batch renumbered), and pass 4b (same day) promoted 3 of the queued candidates — Demi Korevaar, Kyriaki Terzoglou and Rebecca Piva — by opening each player's profile on Volleyball World, the FIVB's official competition platform, and confirming that the birth date it publishes agrees exactly with the untraceable value in the structured item)** plus **142 REVIEW_REQUIRED candidates (R-2026-001..096 plus R-2026-097 added in Session 14 when the Yarishna Ayala DOB-year-conflict row was demoted from the verified catalog and routed to review — each with evidence found + missing field + reason + date checked; never guessed; 118 of them `AGE_SOURCE_NOT_RECORDED` (46 added by Session 16) — a birth date exists in the structured record but carries no reference — plus 4 `SPORT_NOT_CORROBORATED` (their only date-of-birth citations are Japanese idol-group artist pages or an Alabama women's *tennis* roster, so the sport claim is not corroborated by any volleyball document), 1 `AGE_CONFLICTING_VALUES` (Q58885490 Rhamat Alhassan, two different dates of birth in one item, re-confirmed by the pass-4 re-harvest), 1 `AGE_SOURCE_IDENTITY_UNRESOLVED` (Q61667862 Ezgi Kara, whose only reference is an ilan.gov.tr court notice on correcting a population record — a legitimate public page that says nothing about this athlete), 1 `NAME_MISMATCH_IN_CITED_SOURCE` (the Yurika Yokoishi / “Bamba, Yurika” withdrawal), and Session 18's R-2026-146..153 (conflicting dates of birth, a Wikipedia-title/label mismatch, and a sitelink that redirected to a TV series))** plus 23 irregularities (6 blocked requiring owner review; IRR-2026-09-07-021 logs the session-16 sweep's data-shape flags and the resolved TikTok-only gap; IRR-2026-09-06-007..015 follower-coverage gaps and session-10/12 variance flags; IRR-2026-09-06-016 evidence-tier register + spot-check audit for the Session-13 batch; IRR-2026-09-06-017 self-caught transcription risk, resolved; IRR-2026-09-06-018 pass-2 evidence tiers, the conflicting-DOB candidate and the remaining unsearched bands; IRR-2026-09-06-019 pass-3 duplicate-person merge (Kelsey Robinson / Kelsey Robinson Cook), the strengthened alias dedupe, a 36-entry wording correction and the both-disciplines correction; IRR-2026-09-07-020 pass-4 — the discarded draft transcription after an unordered fetch returned overlapping chunks, the identity mismatch withdrawn to R-2026-096, the refused ilan.gov.tr promotion, the four `SPORT_NOT_CORROBORATED` exclusions, a committed `SyntaxError` in the shared entry builder found and fixed, the `College Athlete` correction on W-2026-708, the pass-4 date-stamp decision, three suspect-shaped X handles recorded verbatim, and a pre-existing duplicate review-queue identifier (R-2026-014) flagged but deliberately not renumbered); discovery is activity-first (public fitness, swimwear/beachwear, fashion, athletics, lifestyle, esports etc.) then adult/woman/public-ownership verification; swimwear/bikini content is objectively classified (Swimwear/Bikini Fashion/Beachwear etc., never hot/sexy) and college attendance never proves adult; further rows require strongest available legitimate public evidence for each claim (Tier 1 where possible, multiple Tier 3 independent sources combined where needed — Tier 3 alone not sole sensitive proof when stronger reasonably available), line-by-line verification, and duplicate search (micro/college/swimwear creators without independent DOB/gender evidence remain `AGE_UNVERIFIED`/`GENDER_UNVERIFIED`/`REVIEW_REQUIRED` with full provenance, not VERIFIED nor discarded); 18+ via any reliable public evidence (published DOB, explicit age statement like “30-year-old” in reputable publication, first-party bio with age, sports bio, interview — never inferred from appearance/clothing/college).
- `data/schema.json` — JSON Schema for catalog entries and `reviewQueue` (includes optional `genderEvidence` for women-only verification and objective-category description; `reviewQueue` items record name/username/platform/profileUrl/discoveryCategory/evidenceFound/missingEvidence/flags/lastChecked).
- `docs/verification-protocol.md` — line-by-line verification requirements (women-only, objective categories, no hallucinations, scale limits, iterative activity-first methodology).
- `docs/review-log.md` — review notes and irregularity log (Sessions 01–07, with Session 07 discovery queue).

## Local preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open <http://localhost:8000>.

## GitHub Pages deployment

Pages serves from the `main` branch repository root; the site is `index.html`.

## Data quality rules

1. No record is added unless the person is a verified adult (18+) woman — gender and age are
   never inferred from appearance, clothing, body type, bikini/swimwear photos, name, or AI;
   18+ must be independently established via first-party bio with age/public birth date/
   official creator bio/sports or university-athletic profile/reputable interview/established
   publication — not college attendance or “college girl” or facial estimate.
2. No record is added from appearance-only searches, inferred identity, or unattributed social
   handles; discovery is activity-first (public fitness, fashion, modeling, swimwear/beachwear,
   athletics, college athletics, lifestyle, travel, etc. → then eligibility verification).
3. Every link is recorded exactly for manual review; use the strongest legitimate public
   evidence actually available for each person (Tier 1 official bio/site/social/agency/university
   sports org → Tier 2 reputable interview/publication → Tier 3 public creator directory/
   secondary DB/search result — Tier 3 alone not sole sensitive proof when stronger is
   reasonably available; multiple independent Tier 3 sources combined where Tier 1 DOB is absent,
   never celebrity-level documentation required, but never guessed).
4. Categories are objective (Fitness/Fitness Model/Athlete/College Athlete/Fashion/Swimwear/
   Bikini Fashion/Beachwear/Modeling/Lifestyle/Travel/Wellness/Beauty/Creator/etc.), never
   subjective attractiveness labels or hot/sexy rankings; bikini/swimwear is classified by content,
   not body description.
5. Conflicting, missing, or ambiguous evidence is recorded as an irregularity or as a `reviewQueue` entry (`GENDER_UNVERIFIED`,
   `AGE_UNVERIFIED`, `IDENTITY_UNCERTAIN`, `PROFILE_UNVERIFIED`, `POSSIBLE_AI`, `BROKEN_LINK`, etc.) with full provenance (name, username, platform, profile URL, discovery category, evidence found, missing field with reason, date checked) instead of a guessed catalog row; promising candidates are never discarded — they go to `REVIEW_REQUIRED`.
6. No generated, AI, deepfake, impersonator, leaked, private, or non-consensual material is
   accepted; no home addresses, phones, private contact, or passwords are collected.
7. No autonomous bulk collection of real people's profiles — even with a 1,000-row target;
   records require opt-in or clear professional/public-figure context and are verified
   individually, line by line; the workflow is iterative `Discover → inspect → verify → classify (VERIFIED / REVIEW_REQUIRED / REJECTED / DUPLICATE) → deduplicate → record` with diverse queries (fitness micro, swimwear, college, lifestyle etc.) until no promising candidates remain. Duplicates are prevented by pre-search on name and all usernames. Follower count is a classification/filter attribute (not an eligibility requirement); counts are never invented.
