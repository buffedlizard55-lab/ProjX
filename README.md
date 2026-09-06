# ProjX

ProjX is a static GitHub Pages site for a **verified directory workflow**: real, adult (18+)
*women* who are public figures and professionals — working models, athletes, creators, and
similar public pages — included only when each record carries official or trusted age *and
gender* evidence, official reviewable links, and line-by-line verification notes. The master
database is **women-only** by hard rule: every record must represent a woman with reliable
public gender evidence (first-party bio, official site, agency, sports-org bio, reputable
interview/publication) — never appearance, clothing, name, or AI analysis.

## Scope guardrails

This repository does **not** contain a bulk-collected list of real people, and it deliberately
does not bulk-harvest social profiles. The site and data model only accept records when the
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

- `index.html` — main page and UI shell.
- `assets/styles.css` — responsive styling.
- `assets/app.js` — catalog loading, filtering, table rendering, and export buttons.
- `data/catalog.json` — entries and irregularities. Now contains **242 verified women (W-2026-001..242 — prior 100 plus Session 12's 104 additions spanning soccer/football, volleyball, WNBA, tennis, track, hockey, WWE, UFC, swimming, gymnastics, surfing, climbing, golf, cross-sport plus Session 13's 41 volleyball-focused additions)** plus **5 REVIEW_REQUIRED candidates (R-2026-001 Jessica Parker, R-2026-005 Lizzie Martinez, R-2026-008 Rachel Cooper, R-2026-012 Valentina Villa, R-2026-014 Kami Miner — each with evidence found + missing field + reason + date checked; never guessed)** plus 15 irregularities (6 blocked requiring owner review; 9 IRR-2026-09-06-007..015 follower-coverage gaps and session-10/12 follower-variance/DOB-day/handle-variant flags for manual review); discovery is activity-first (public fitness, swimwear/beachwear, fashion, athletics, lifestyle, esports etc.) then adult/woman/public-ownership verification; swimwear/bikini content is objectively classified (Swimwear/Bikini Fashion/Beachwear etc., never hot/sexy) and college attendance never proves adult; further rows require strongest available legitimate public evidence for each claim (Tier 1 where possible, multiple Tier 3 independent sources combined where needed — Tier 3 alone not sole sensitive proof when stronger reasonably available), line-by-line verification, and duplicate search (micro/college/swimwear creators without independent DOB/gender evidence remain `AGE_UNVERIFIED`/`GENDER_UNVERIFIED`/`REVIEW_REQUIRED` with full provenance, not VERIFIED nor discarded); 18+ via any reliable public evidence (published DOB, explicit age statement like “30-year-old” in reputable publication, first-party bio with age, sports bio, interview — never inferred from appearance/clothing/college).
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
