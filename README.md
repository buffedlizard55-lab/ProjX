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
quality and verification take priority over quantity, so 4 — not 1,000 — is the correct
verified count.

## Site

Plain HTML/CSS/JavaScript, served directly by GitHub Pages from the repository root.
Published at <https://buffedlizard55-lab.github.io/ProjX/>.

- `index.html` — main page and UI shell.
- `assets/styles.css` — responsive styling.
- `assets/app.js` — catalog loading, filtering, table rendering, and export buttons.
- `data/catalog.json` — entries and irregularities. Now contains **7 verified women (W-2026-001..007 — Serena Williams, Simone Biles, Naomi Osaka, Alex Morgan, Megan Rapinoe, Katie Ledecky, Chloe Kim)** plus 5 blocked irregularities; swimwear/bikini content is objectively classified (Swimwear/Bikini Fashion/Beachwear etc., never hot/sexy) and college attendance never proves adult; further rows require opt-in or professional/public context with line-by-line Tier-1 verification (micro/college/swimwear creators without Tier-1 DOB/gender evidence remain `REVIEW_REQUIRED`, not VERIFIED).
- `data/schema.json` — JSON Schema for catalog entries (includes optional `genderEvidence` for women-only verification and objective-category description).
- `docs/verification-protocol.md` — line-by-line verification requirements (women-only, objective categories, no hallucinations, scale limits).
- `docs/review-log.md` — review notes and irregularity log (Sessions 01–05).

## Local preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open <http://localhost:8000>.

## GitHub Pages deployment

Pages serves from the `main` branch repository root; the site is `index.html`.

## Data quality rules

1. No record is added unless the person is a verified adult (18+) woman from official/trusted
   sources — gender and age are never inferred from appearance, clothing, name, or AI.
2. No record is added from appearance-only searches, inferred identity, or unattributed social
   handles.
3. Every link must be official, platform-verified, agency, or press — or cross-linked from an
   official source — and recorded exactly for manual review; Tier-3 alone never proves gender,
   identity, or adult status.
4. Categories are objective (Model/Fitness/Athlete/Fashion/Lifestyle/Creator/etc.), never
   subjective attractiveness labels.
5. Conflicting, missing, or ambiguous evidence is recorded as an irregularity (`GENDER_UNVERIFIED`,
   `AGE_UNVERIFIED`, `IDENTITY_UNCERTAIN`, `POSSIBLE_AI`, `BROKEN_LINK`, etc.) instead of a
   catalog entry; no hallucinations.
6. No generated, AI, deepfake, impersonator, leaked, private, or non-consensual material is
   accepted; no home addresses, phones, private contact, or passwords are collected.
7. No autonomous bulk collection of real people's profiles — even with a 1,000-row target;
   records require opt-in or clear professional/public-figure context and are verified
   individually, line by line. Duplicates are prevented by pre-search on name and all usernames.
