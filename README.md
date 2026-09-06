# ProjX

ProjX is now a static GitHub Pages-ready site for a verified adult creator directory workflow.

## Important scope

This repository does **not** include a collected list of real people. The site and data model are designed for an ethical, opt-in directory that only accepts records when each person is:

- a real, non-AI individual;
- confirmed to be 18+ through an official or trusted public source;
- represented by official links suitable for manual review;
- included with consent or a clear professional/public listing context; and
- reviewed line by line with flags recorded for any irregularities.

Bulk collection of social media profiles for sexualized ranking or non-consensual profiling is intentionally not implemented.

## Site

The site is plain HTML/CSS/JavaScript and can be served directly by GitHub Pages from the repository root.

- `index.html` — main page and UI shell.
- `assets/styles.css` — responsive styling.
- `assets/app.js` — catalog loading, filtering, table rendering, and export buttons.
- `data/catalog.json` — verified entries and irregularities. It is currently empty pending opt-in verified records.
- `data/schema.json` — schema for future catalog entries.
- `docs/verification-protocol.md` — line-by-line verification requirements.
- `docs/review-log.md` — review notes and irregularity log.

## Local preview

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000`.

## GitHub Pages deployment

A GitHub Actions workflow is included at `.github/workflows/pages.yml`. It packages the static site and deploys it to GitHub Pages when changes land on `main` or this Arena branch, depending on repository Pages settings.

Expected Pages URL for this repository:

<https://buffedlizard55-lab.github.io/ProjX/>

## Data quality rules

1. No record is added unless the person is verified 18+ from official/trusted sources.
2. No record is added from appearance-only searches or inferred identity.
3. Every link must be official, platform-verified, or cross-linked from an official source.
4. Conflicting, missing, or ambiguous evidence is recorded as an irregularity instead of a catalog entry.
5. No generated, AI, deepfake, impersonator, leaked, private, or non-consensual material is accepted.
