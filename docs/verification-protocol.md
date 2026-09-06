# Verification protocol

This project may only publish records that satisfy all checks below. If any check fails, the row must not be published and the issue must be captured in `data/catalog.json` under `irregularities` or in `docs/review-log.md`.

## Required checks before adding a row

1. **Adult-only verification**
   - Confirm the person is 18+ from an official or trusted source.
   - Accepted evidence examples: official site bio, agency profile, platform age gate with official ownership, reputable interview/profile stating date of birth, or other authoritative source.
   - Do not infer age from appearance, school year, follower count, clothing, location, or user comments.

2. **Real-person and non-AI verification**
   - Confirm the record is not AI-generated, synthetic, a deepfake, an impersonator, or a repost account.
   - Prefer official cross-links among personal site, agency, platform verification badge, and reputable press.

3. **Consent or professional/public context**
   - Include only opt-in submissions or people who are clearly operating professional/public creator, model, entertainment, athletic, or public-figure pages.
   - Do not collect private individuals, private social profiles, leaked material, or non-consensual reposts.

4. **Official source links**
   - Store direct URLs to sources that a human reviewer can open.
   - Each source needs a `relationship` value in the schema: `official`, `verified-platform`, `agency`, `press`, `age-evidence`, or `other-trusted`.

5. **No hallucinations**
   - Do not add a row unless every factual field is supported by its source links.
   - Any uncertainty must become a flag or irregularity, not a guessed value.

## Minimum row fields

See `data/schema.json`. Every row must include:

- `id`
- `displayName`
- `categories`
- `legalAdultEvidence`
- `sources`
- `verificationStatus`
- `lastReviewed`
- `flags`

## Review status guidance

- `verified`: All required checks passed, source links work, and no unresolved flags remain.
- `needs-review`: Some evidence exists but one or more checks remain incomplete.
- `blocked`: The record should not be published because it lacks consent/professional context, lacks age proof, appears synthetic/impersonated, uses non-consensual material, or otherwise violates project scope.
