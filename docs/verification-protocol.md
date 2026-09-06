# Verification protocol

This project may only publish records that satisfy **all** checks below. If any check fails, the row must not be published and the issue must be captured in `data/catalog.json` under `irregularities` or in `docs/review-log.md`. The project is **women-only**; see check 2.

## Required checks before adding a row

1. **Adult-only verification (18+)**
   - Confirm the person is 18+ from an official or trusted source — never from appearance.
   - Accepted evidence: official site bio with DOB/age, agency profile, sports-organization bio, platform age gate with proven official ownership, reputable interview/profile stating DOB, or other authoritative public biographical source.
   - Do not infer adulthood because someone looks mature, is described as a “college girl,” attends college, models, or posts adult-themed material.

2. **Women-only inclusion — gender verification**
   - Every master-database record must represent a woman.
   - Acceptable gender evidence: first-party biography, official personal website, professional agency biography, official sports/organization biography, reputable interview or publication, or consistent public biographical information from reliable sources.
   - Do NOT determine gender from appearance, clothing, body shape, name alone, AI image analysis, username alone, comments from strangers, or guesswork.
   - If gender cannot be reliably established → `GENDER_UNVERIFIED` / `REVIEW_REQUIRED`; do not publish.
   - Explicit exclusions: men, male models/athletes/influencers/creators, couples, group accounts where the individual woman cannot be separately identified, gender-ambiguous profiles without reliable supporting information, organizations rather than individual women.

3. **Real-person and non-AI verification**
   - Confirm the record is a real, living woman — not AI-generated, synthetic, virtual influencer, deepfake, impersonator, or repost account.
   - Prefer official cross-links among personal site, agency, platform verification badge, and reputable press; check for consistent identity, name/username, biography, and photographs across sources.

4. **Consent or professional/public context**
   - Include only opt-in submissions or people who are clearly operating professional/public creator, model, entertainment, athletic, fashion, lifestyle, or public-figure pages.
   - Do not collect private individuals, private social profiles, leaked material, non-consensual reposts, or home addresses / phone numbers / private contact / passwords / sensitive personal information unrelated to the project.

5. **Official source links and objective categories**
   - Store direct URLs to sources that a human reviewer can open. Each source needs a `relationship` value: `official`, `verified-platform`, `agency`, `press`, `age-evidence`, or `other-trusted`.
   - Prioritize Tier 1 (official personal site, official agency, official sports/org, official verified social, first-party bio, university athletic profile) over Tier 2 (established publications/interviews/databases/reputable interviews) over Tier 3 (public creator directories/secondary databases/public search results) — Tier 3 alone should not be the sole basis for a sensitive eligibility determination (gender, identity, adult status) when stronger evidence is reasonably available; when Tier 1 DOB is not in an official bio, use multiple independent Tier 3 sources combined and record them.
   - Categories must be objective (Model, Fitness, Athlete, Fashion, Lifestyle, Creator, Entertainment, College athlete, Public personality, Other) — never subjective attractiveness labels such as hot/sexy/most attractive.

6. **No hallucinations and line-by-line review**
   - Do not add a row unless every factual field is supported by its source links. No invented women, names, ages, DOBs, URLs, usernames, occupations, verification statuses, sources, or account relationships.
   - Before publishing, verify line by line: gender, adult status, identity/real person, profile ownership, category, sources (primary + supporting where appropriate, URLs recorded exactly, verification date recorded), duplicate search (name, Instagram, TikTok, website, other usernames, record ID), and flags.
   - Any uncertainty becomes a flag or irregularity (`GENDER_UNVERIFIED`, `AGE_UNVERIFIED`, `IDENTITY_UNCERTAIN`, `POSSIBLE_IMPERSONATION`, `POSSIBLE_AI`, `DUPLICATE`, `BROKEN_LINK`, `CONFLICTING_INFORMATION`, `PROFILE_UNVERIFIED`, `SOURCE_UNRELIABLE`, `OTHER`) — never a guessed value. Missing or conflicting evidence → `REVIEW_REQUIRED` / `needs-review` or `blocked`, not a verified row.

## Minimum row fields

See `data/schema.json`. Every row must include:

- `id`
- `displayName`
- `categories` (objective, see §5)
- `legalAdultEvidence` (`summary`, `sourceLabel`, `sourceUrl`, `checkedAt`)
- `sources[]` (`label`, `platform`, `url`, `relationship`)
- `verificationStatus` (`verified` | `needs-review` | `blocked`)
- `lastReviewed`
- `flags`
- `notes` (optional) — additional gender-verification, identity, or category evidence should be cited here with source URLs when not in `legalAdultEvidence`/`sources`.

Duplicate prevention: search existing records by name, Instagram/TikTok/website/other usernames, and record ID before adding; consolidate multiple verified accounts belonging to the same woman into one record only when the relationship is reliably verified.

## Review status guidance

- `verified`: All required checks (1–6) passed, every source link resolves and names the person, no unresolved flags remain.
- `needs-review`: Some evidence exists but one or more checks remain incomplete (e.g., `GENDER_UNVERIFIED`, `AGE_UNVERIFIED`, broken link).
- `blocked`: The record should not be published because it lacks verifiable gender/adult/identity evidence, lacks consent/professional context, appears synthetic/impersonated, includes men/couples/group/org or gender-ambiguous profiles without reliable evidence, uses non-consensual material, or otherwise violates scope. At-scale autonomous candidates that cannot meet Tier-1 evidence requirements are `blocked` in bulk — see `docs/review-log.md` Sessions 01–03.

## Discovery methodology (activity-first)

- Discover **public creators by documented public activity** (fitness, fashion, modeling, swimwear/beachwear, athletics, college athletics, lifestyle, travel, etc.) — *not* by aggregating random women.
- For each discovered creator, then verify: real person → adult 18+ → woman → public account → account ownership → objective category → legitimate source evidence. Use the strongest legitimate public evidence actually available for that individual (Tier 1 official bio/site/social/agency/university/sports org; Tier 2 reputable interview/publication; Tier 3 public creator directory/secondary database/search result — use multiple independent Tier 3 sources when Tier 1 DOB is not in an official bio, but Tier 3 alone never proves a sensitive eligibility claim when stronger is reasonably available).
- Do **not** require celebrity-level evidence (Wikipedia/Britannica/agency/major publication/blue check/large following) — a micro/regional/independent creator can qualify if her identity, adult status, woman status, ownership, and category are all supported by enough legitimate public evidence to support the specific claims recorded.
- Swimwear/bikini/beachwear creators are in scope when publicly documented as swimwear/fashion activity; classify objectively as `Swimwear`, `Bikini/Swimwear Fashion`, `Beachwear`, `Fashion`, `Modeling`, `Fitness`, etc. — never sexual attractiveness ratings, body-part descriptions, or “hot/sexy” ranking. Bikini photos alone never prove adult or woman.
- College/college-athlete creators are in scope but `college student ≠ 18+` — adult must be independently verified via public birth date/official bio/reputable source, not “college girl” terminology.

## Scale and automation limits

- Bulk autonomous scraping of Instagram/TikTok/Facebook/Reddit/YouTube/X is prohibited by those platforms’ ToS and by this protocol. Do not bypass logins, CAPTCHAs, robots, or other access controls. Iterative public-web research (Search → inspect → verify → deduplicate → record) is the allowed loop — continue until no more qualifying profiles or target reached; do not claim 1,000 unless 1,000 actually passed verification.
- The master database target (e.g., 1,000) is a target, not a mandate to lower standards nor to artificially raise to celebrity-level documentation. If only N women can be independently verified with the strongest available legitimate public evidence, the verified count is N — never manufacture rows to reach a number and never infer missing fields. Quality and verification take priority over quantity. A hallucination audit must confirm no invented fields before any commit.

## Structured public-data discovery (added Session 13)

Systematic discovery over **public structured records** (Wikidata items built from federation, league, club,
university and volleyball-database sources) is an allowed discovery loop: it is not social-platform scraping, it
never bypasses an access control, and every query used is archived under `data/research/urls/` so the exact
population can be re-run and audited. Discovery scale never relaxes acceptance — each row still needs its own cited
age evidence, its own cited gender evidence, a dedupe check on name *and* every handle, and `UNKNOWN` instead of a
guess for anything not observable.

How the three source tiers map onto a structured birth-date statement:

| Tier | What the record cites | Example hosts seen in Session 13 |
| --- | --- | --- |
| 1 — official | the reference URL attached to the date-of-birth statement is a federation, league, club, NOC or university athletics page | `cev.eu`, `fivb.com`, `volleyball-bundesliga.de`, `slovakvolley.sk`, `svf.sk`, `bvf.by`, `teamnl.org`, `volleyball.ca`, `cpb.org.br`, `jva.or.jp`, `vleague.jp`, `olympic.ca`, `gocards.com`, `mutigers.com`, `arizonawildcats.com`, `seminoles.com`, `usctrojans.com`, `dscvolley.de` |
| 2 — reputable publication / encyclopedia | an English Wikipedia article is linked to the item, or a press page is cited | `en.wikipedia.org`, `lequipe.fr`, `eurosport.de`, `jornaldovolei.com.br`, `hlsports.de` |
| 3 — secondary volleyball database | the statement names a database, with or without a URL | `women.volleybox.net`, `bvbinfo.com` (Beach Volleyball Database), `worldofvolley.com`, InterSportStats, Olympedia, VBL/FIVB database records |

Rules that follow from that mapping:

1. A date of birth whose statement carries **no reference at all** is not evidence — the candidate goes to
   `reviewQueue` with `AGE_SOURCE_NOT_RECORDED`, never into the catalog with a guessed or unsourced date.
2. A date of birth referenced only to a **named database with no URL** may still verify adult status (the value is
   documented and traceable to a real source), but the row must carry the flag `AGE_EVIDENCE_SECONDARY_SOURCES` so a
   human reviewer knows the primary page still needs a click-through. Tier 3 alone is never presented as stronger
   than it is: the entry text says the value is "recorded in the structured item, whose reference names X", not
   "confirmed by X".
3. Gender evidence is documentary: the item's sex/gender field, women's-team roster membership, women's competition
   registries, or women's-database records. Where a cited URL is not explicitly a women's record, the entry must not
   describe it as one.
4. Social handles are recorded only when the structured record already links them (P2003/P2002/P7085/P2013/P2397);
   handle discovery is not a licence to scrape the platform. Follower counts are captured only from a page that
   publicly displays them (platform page or public analytics snapshot), with `checkedAt`, the snapshot date,
   `countType`, and a `sourceNote`; otherwise `FOLLOWER_COUNT_UNKNOWN` + `FOLLOWER_RANGE_UNKNOWN`.
5. Third-party analytics **content/AI category tags are never used as categories** — categories stay objective
   (`Athlete`, `Volleyball`, `Beach Volleyball`, `College Athlete`, `Creator`).
6. Every batch ships with a reproducible generator script, a per-entry audit sheet under `data/research/`, a
   spot-check audit of primary pages across different evidence types, and `validate_catalog.py` at `errors=0`.
   Transcription from a fetched result must be verbatim: any value that cannot be pointed at in the fetched output is
   deleted, and the incident is logged as an irregularity (see `IRR-2026-09-06-017`).
