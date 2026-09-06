# Review log

## 2026-09-06

### Session 01 — repository review and 1,000-profile bulk-collection request

**Request.** The owner asked the project to autonomously search, collect, and organize ~1,000
"new entries" of real women described as "models, college girls, hot girls" across Instagram,
TikTok, Facebook, Reddit, and elsewhere online, using appearance criteria such as bikinis,
workout/athletic content, yoga pants, tight clothing, lace, and sheer clothing, and to mark
each entry "verified 18+" with official source links for manual review.

**What was done.**

- Reviewed the repository. Confirmed the existing scope: an opt-in / professional-context
  directory of adult (18+) public figures with official age-and-identity evidence, verified
  line by line from stored source URLs. Confirmed GitHub Pages is published from `main` at
  https://buffedlizard55-lab.github.io/ProjX/.
- Verified the static site serves correctly and validated `data/catalog.json`,
  `data/schema.json`, and `assets/app.js`.
- Completed site work requested alongside the collection work: the UI now makes the
  eligibility and manual-review rules explicit, adds a docs/data section, and keeps an empty
  catalog with a clear explanation. `data/catalog.json` and this log document the outcome.

**What was not done, and why.**

- The ~1,000-entry appearance-based collection was **not executed**, and zero records were
  published. Reasons, recorded as `IRR-2026-09-06-002`:
  1. The subjects are identifiable private individuals, and aggregating their public photos
     into a searchable, looks-based list is not an opt-in or professional/public-figure
     context. Such lists enable harassment, stalking, and non-consensual exposure.
  2. Official or trusted 18+ verification for that population cannot be performed
     autonomously and truthfully at scale. Fabricating "verified 18+" badges to satisfy the
     count would violate the project's own no-hallucination rule.
  3. Content style (bikinis, tight clothing, athletic wear) is not evidence of consent to
     directory listing, adult status, or authenticity.
- Each such candidate would fail the verification protocol and would be recorded as
  `blocked`, never published. Any future scope change requires owner review and, for real
  people, evidence of opt-in consent or clear professional/public-figure status plus official
  18+ documentation.

**References for manual review**

- Repository: https://github.com/buffedlizard55-lab/ProjX
- Published site: https://buffedlizard55-lab.github.io/ProjX/
- Verification protocol: https://github.com/buffedlizard55-lab/ProjX/blob/main/docs/verification-protocol.md
- Catalog data (entries + irregularities): https://github.com/buffedlizard55-lab/ProjX/blob/main/data/catalog.json
- Data schema: https://github.com/buffedlizard55-lab/ProjX/blob/main/data/schema.json

**Irregularities logged**

- `IRR-2026-09-06-001` — blocked: no bulk social-profile entries were added (original scope
  decision).
- `IRR-2026-09-06-002` — blocked: 2026-09-06 request for ~1,000 appearance-based profiles of
  real women was reviewed and not executed, with reasons above. Status:
  `requires-owner-review`.

### Session 02 — resubmission of the 1,000-profile request with new framing

**Request.** The owner resubmitted the same task the same day with additional framing:
"this is not a sex or stalking project," "if their profile is set to public, then that is
public," and "it's not a look based list." The concrete task was otherwise unchanged: search
and collect ~1,000 real women ("models, college girls, hot girls") from Instagram, TikTok,
Facebook, Reddit, and similar; inclusion guided by photos described as bikinis, workout/
athletic, yoga pants, tight clothing, lace, sheer clothing, and "sexy photos"; each row to be
marked "verified over 18" with official source links, with no manual input.

**Line-by-line response to the new claims** (recorded as `IRR-2026-09-06-003`, blocked).

1. *"Not a sex or stalking project."* Stated intent does not change what the artifact is:
   a searchable table of ~1,000 identifiable women keyed to sexualized appearance descriptors,
   with cross-platform links. Such lists are routinely used for unwanted contact regardless of
   the collector's intent, so intent alone is not a sufficient safeguard.
2. *"Public profile = public."* True but not sufficient. Public visibility means anyone can
   view the profile; it does not mean the person consented to being indexed in a directory of
   this kind. Platforms' own rules also prohibit exactly this sort of automated mass
   collection, so "official verified trusted sources" would not sanction the method.
3. *"Not a look based list."* The request's own inclusion criteria — bikinis, yoga pants,
   tight/see-through clothing, "sexy photos," "hot girls," "college girls" — are appearance-
   and demographic-based. The list is defined by looks, which is why the phrase "not a look
   based list" does not survive review.
4. *"Verified over 18," no manual input.* There is no official or trusted queryable source
   that confirms the age of everyday public social-media account holders. Producing 1,000
   "verified 18+" rows without manual input therefore requires inventing evidence — the
   hallucinations the project rules prohibit — and the same applies to "real, not AI"
   confirmation.
5. *"College girls" as a target category.* College enrollment and age band cannot be verified
   from a public profile, and aggregating that demographic by appearance is precisely the
   pattern this project excludes.

**Outcome.** No records were published; the catalog remains empty by design. The repository's
documentation and UI were updated to keep the decision auditable:
`IRR-2026-09-06-003` added to `data/catalog.json`, this session appended to
`docs/review-log.md`, and the site's empty state updated to reference both irregularity
records. Status: `requires-owner-review`.

### Earlier history

- Repository reviewed: initial repository contained only `README.md`.
- Created a GitHub Pages-ready static site with a clean table UI, filters, exports, schema,
  and verification documentation.
- No real-person records were added.
- Irregularity `IRR-2026-09-06-001` was recorded because bulk collection of sexualized
  social-media profiles of real people would create non-consensual profiling risk. Future
  records should be opt-in or clearly professional/public records with official 18+
  verification.
