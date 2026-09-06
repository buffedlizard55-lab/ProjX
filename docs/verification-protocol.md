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
