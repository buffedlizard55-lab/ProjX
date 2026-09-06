# ProjX

ProjX is a static GitHub Pages site for a **verified directory workflow**: real, adult (18+)
public figures and professionals — working models, athletes, creators, and similar public
pages — included only when each record carries official or trusted age evidence, official
reviewable links, and line-by-line verification notes.

## Scope guardrails

This repository does **not** contain a collected list of real people, and it deliberately does
not bulk-harvest social profiles. The site and data model only accept records when the person
is:

- a real, non-AI individual;
- confirmed 18+ through an official or trusted public source (never inferred from appearance,
  content, school year, or follower counts);
- operating a public-figure/professional page or clearly opted in — private individuals are
  never inferred into the table;
- represented by direct official links (official, verified-platform, agency, press, or
  age-evidence) suitable for manual review; and
- reviewed line by line, with missing or ambiguous evidence recorded as an irregularity
  instead of a guessed catalog row.

Bulk collection of real people's profiles into a searchable, appearance-based directory is
intentionally not implemented. On 2026-09-06 a request for ~1,000 such entries was reviewed
and logged as irregularity `IRR-2026-09-06-002` (blocked); see
[docs/review-log.md](docs/review-log.md).

## Site

Plain HTML/CSS/JavaScript, served directly by GitHub Pages from the repository root.
Published at <https://buffedlizard55-lab.github.io/ProjX/>.

- `index.html` — main page and UI shell.
- `assets/styles.css` — responsive styling.
- `assets/app.js` — catalog loading, filtering, table rendering, and export buttons.
- `data/catalog.json` — entries and irregularities. Empty of entries by design pending
  compliant opt-in or professional/public records.
- `data/schema.json` — JSON Schema for catalog entries.
- `docs/verification-protocol.md` — line-by-line verification requirements.
- `docs/review-log.md` — review notes and irregularity log.

## Local preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open <http://localhost:8000>.

## GitHub Pages deployment

Pages serves from the `main` branch repository root; the site is `index.html`.

## Data quality rules

1. No record is added unless the person is verified 18+ from official/trusted sources.
2. No record is added from appearance-only searches or inferred identity.
3. Every link must be official, platform-verified, or cross-linked from an official source.
4. Conflicting, missing, or ambiguous evidence is recorded as an irregularity instead of a
   catalog entry.
5. No generated, AI, deepfake, impersonator, leaked, private, or non-consensual material is
   accepted.
6. No autonomous bulk collection of real people's profiles; records require opt-in or clear
   professional/public-figure context.
