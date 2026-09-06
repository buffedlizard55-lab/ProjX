#!/usr/bin/env python3
"""Build the Instagram/TikTok profile directory.

Writes:
  data/catalog-social.json     — derived social subset (catalogType=social)
  directory/{id}.html          — one static subpage per social catalog entry

Does not invent people, ages, follower counts, or URLs. Only fields already
stored on catalogType=social rows are rendered.

Usage:
  python3 scripts/build_directory.py [--dry-run]
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import date
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "catalog.json")
SOCIAL_JSON = os.path.join(ROOT, "data", "catalog-social.json")
DIRECTORY = os.path.join(ROOT, "directory")
TODAY = date.today().isoformat()

ID_RE = re.compile(r"^W-2026-\d+$")
SOCIAL_PLATFORMS = ("Instagram", "TikTok")


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def safe_url(value: str | None) -> str:
    if not value:
        return ""
    try:
        parsed = urlparse(value)
    except ValueError:
        return ""
    if parsed.scheme not in ("http", "https"):
        return ""
    if not parsed.netloc:
        return ""
    return value


def chip(label: str, href: str | None = None) -> str:
    text = esc(label)
    url = safe_url(href) if href else ""
    if url:
        return (
            f'<a class="chip" href="{esc(url)}" rel="noopener noreferrer" '
            f'target="_blank">{text}</a>'
        )
    return f'<span class="chip">{text}</span>'


def chips(items: list, empty: str = "None") -> str:
    values = [item for item in items if item]
    if not values:
        return f'<span class="chip">{esc(empty)}</span>'
    return (
        '<ul class="flag-list">'
        + "".join(f"<li>{chip(item)}</li>" for item in values)
        + "</ul>"
    )


def status_pill(status: str) -> str:
    normalized = status if status in ("verified", "needs-review", "blocked") else "needs-review"
    labels = {
        "verified": "Verified",
        "needs-review": "Needs review",
        "blocked": "Blocked",
    }
    return f'<span class="status-pill {normalized}">{labels[normalized]}</span>'


def evidence_block(title: str, evidence: dict | None) -> str:
    if not evidence:
        return (
            f'<section class="panel"><h2>{esc(title)}</h2>'
            f'<p><span class="status-pill needs-review">Missing evidence</span></p>'
            f"</section>"
        )
    url = safe_url(evidence.get("sourceUrl"))
    source = chip(evidence.get("sourceLabel") or "Source", url)
    checked = esc(evidence.get("checkedAt") or "Unknown")
    summary = esc(evidence.get("summary") or "Evidence recorded")
    return f"""<section class="panel">
        <h2>{esc(title)}</h2>
        <p>{summary}</p>
        <dl class="dl-meta">
          <dt>Source</dt><dd>{source}</dd>
          <dt>Checked</dt><dd>{checked}</dd>
        </dl>
      </section>"""


def account_card(account: dict, featured: bool = False) -> str:
    platform = account.get("platform") or "Platform"
    username = account.get("username") or ""
    display = account.get("followerCountDisplay") or "FOLLOWER_COUNT_UNKNOWN"
    count_type = account.get("countType") or "unknown"
    size = account.get("followerSizeRange") or "FOLLOWER_RANGE_UNKNOWN"
    checked = account.get("checkedAt") or "Unknown"
    note = account.get("sourceNote") or ""
    url = safe_url(account.get("profileUrl"))
    klass = "account-card featured" if featured else "account-card"
    open_link = (
        f'<p><a class="button secondary" href="{esc(url)}" rel="noopener noreferrer" '
        f'target="_blank">Open {esc(platform)} profile</a></p>'
        if url
        else ""
    )
    user_line = f"<p>{esc(username)}</p>" if username else ""
    note_line = f"<p>{esc(note)}</p>" if note else ""
    return f"""<article class="{klass}">
        <h3>{esc(platform)}</h3>
        {user_line}
        <p><strong>Followers:</strong> {esc(display)} · {esc(count_type)} · {esc(size)}</p>
        <p><small>Checked {esc(checked)}</small></p>
        {note_line}
        {open_link}
      </article>"""


def source_list(sources: list) -> str:
    if not sources:
        return '<span class="status-pill needs-review">No sources</span>'
    items = []
    for source in sources:
        label = source.get("label") or source.get("platform") or "Source"
        rel = source.get("relationship") or ""
        platform = source.get("platform") or ""
        text = label if not rel else f"{label} ({rel})"
        if platform and platform not in text:
            text = f"{text} · {platform}"
        items.append(f"<li>{chip(text, source.get('url'))}</li>")
    return f'<ul class="source-list">{"".join(items)}</ul>'


def first_letter(name: str) -> str:
    ch = (name or "").strip()[:1].upper()
    return ch if "A" <= ch <= "Z" else "#"


def render_profile(entry: dict, prev_entry: dict | None, next_entry: dict | None) -> str:
    name = entry.get("displayName") or "Unnamed record"
    entry_id = entry.get("id") or ""
    status = entry.get("verificationStatus") or "needs-review"
    categories = entry.get("categories") or []
    flags = entry.get("flags") or []
    notes = entry.get("notes") or ""
    last_reviewed = entry.get("lastReviewed") or "Not reviewed"
    accounts = entry.get("socialAccounts") or []
    sources = entry.get("sources") or []
    featured = [a for a in accounts if a.get("platform") in SOCIAL_PLATFORMS]
    other = [a for a in accounts if a.get("platform") not in SOCIAL_PLATFORMS]
    # Also surface IG/TikTok that only exist as sources (early rows).
    featured_platforms = {a.get("platform") for a in featured}
    for source in sources:
        if source.get("platform") in SOCIAL_PLATFORMS and source.get("platform") not in featured_platforms:
            featured.append(
                {
                    "platform": source.get("platform"),
                    "username": "",
                    "profileUrl": source.get("url"),
                    "followerCountDisplay": "FOLLOWER_COUNT_UNKNOWN",
                    "countType": "unknown",
                    "followerSizeRange": "FOLLOWER_RANGE_UNKNOWN",
                    "checkedAt": last_reviewed,
                    "sourceNote": "Documented as an official/source link (no separate socialAccounts row).",
                }
            )
            featured_platforms.add(source.get("platform"))

    largest = entry.get("largestPublicFollowing") or {}
    size = entry.get("overallFollowerSizeRange") or "FOLLOWER_RANGE_UNKNOWN"
    largest_line = "FOLLOWER_COUNT_UNKNOWN"
    if largest.get("display"):
        bits = [str(largest.get("display"))]
        if largest.get("platform"):
            bits.append(f"({largest.get('platform')})")
        if largest.get("username"):
            bits.append(str(largest.get("username")))
        largest_line = " ".join(bits)

    prev_link = (
        f'<a class="button secondary" href="{esc(prev_entry["id"])}.html">← {esc(prev_entry["displayName"])}</a>'
        if prev_entry
        else '<span class="button secondary" aria-disabled="true">← Start of directory</span>'
    )
    next_link = (
        f'<a class="button secondary" href="{esc(next_entry["id"])}.html">{esc(next_entry["displayName"])} →</a>'
        if next_entry
        else '<span class="button secondary" aria-disabled="true">End of directory →</span>'
    )

    notes_html = (
        f'<section class="panel"><h2>Review notes</h2><p class="notes-block">{esc(notes)}</p></section>'
        if notes
        else ""
    )
    other_html = (
        '<section class="panel"><h2>Other documented accounts</h2>'
        f'<div class="account-grid">{"".join(account_card(a) for a in other)}</div></section>'
        if other
        else ""
    )
    featured_html = (
        "".join(account_card(a, featured=True) for a in featured)
        if featured
        else '<p><span class="chip follower-unknown">No Instagram/TikTok socialAccounts row — see official links.</span></p>'
    )

    letter = first_letter(name)
    title = f"{name} — ProjX profile"

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{esc(name)} — verified ProjX Instagram/TikTok catalog record {esc(entry_id)}." />
    <title>{esc(title)}</title>
    <link rel="stylesheet" href="../assets/styles.css" />
  </head>
  <body class="profile-page">
    <a class="skip-link" href="#profile">Skip to profile</a>
    <header class="site-header">
      <nav class="nav" aria-label="Primary navigation">
        <a class="brand" href="../" aria-label="ProjX home">
          <span class="brand-mark" aria-hidden="true">PX</span>
          <span>
            <strong>ProjX</strong>
            <small>Verified Directory</small>
          </span>
        </a>
        <div class="nav-links">
          <a href="../index.html">Catalog</a>
          <a href="./">Profile directory</a>
          <a href="../reference.html">Reference profiles</a>
        </div>
      </nav>
      <section class="profile-hero" id="profile">
        <p class="eyebrow">Catalog published record · {esc(letter)}</p>
        <h1>{esc(name)}</h1>
        <div class="profile-meta">
          <span class="chip">{esc(entry_id)}</span>
          {status_pill(status)}
          {chips(categories, "Uncategorized")}
        </div>
        <p class="muted">Last reviewed {esc(last_reviewed)}. Largest public following: {esc(largest_line)} · {esc(size)} (single platform, never summed).</p>
        <div class="profile-pager">
          {prev_link}
          <a class="button primary" href="./">All profiles</a>
          {next_link}
        </div>
      </section>
    </header>
    <main class="profile-grid">
      <section class="panel">
        <h2>Instagram &amp; TikTok</h2>
        <div class="account-grid">
          {featured_html}
        </div>
      </section>
      {evidence_block("Age evidence", entry.get("legalAdultEvidence"))}
      {evidence_block("Gender evidence", entry.get("genderEvidence"))}
      <section class="panel">
        <h2>Official links</h2>
        {source_list(sources)}
      </section>
      {other_html}
      <section class="panel">
        <h2>Status &amp; flags</h2>
        <dl class="dl-meta">
          <dt>Verification</dt><dd>{status_pill(status)}</dd>
          <dt>Catalog type</dt><dd><span class="chip">social</span></dd>
          <dt>Flags</dt><dd>{chips(flags, "No flags")}</dd>
        </dl>
      </section>
      {notes_html}
    </main>
    <footer class="site-footer">
      <p>
        Static record generated from <a href="../data/catalog.json">data/catalog.json</a>.
        Fields are copied as stored — nothing is estimated.
      </p>
    </footer>
  </body>
</html>
"""


def main() -> int:
    dry = "--dry-run" in sys.argv
    with open(CATALOG, "r", encoding="utf-8") as fh:
        catalog = json.load(fh)

    social = [e for e in catalog.get("entries", []) if e.get("catalogType") == "social"]
    social.sort(key=lambda e: ((e.get("displayName") or "").casefold(), e.get("id") or ""))

    bad_ids = [e.get("id") for e in social if not ID_RE.match(e.get("id") or "")]
    if bad_ids:
        print(f"ERROR: unexpected social ids: {bad_ids[:10]}")
        return 1

    social_catalog = {
        "metadata": {
            "title": "ProjX Instagram / TikTok Directory",
            "generatedAt": TODAY,
            "entryCount": len(social),
            "summary": (
                "Published catalog records with a documented Instagram or TikTok account. "
                "Derived from data/catalog.json (the single source of truth) by catalogType=social. "
                "Powers directory/index.html and directory/{id}.html. No fields are estimated."
            ),
            "sourceCatalog": "data/catalog.json",
        },
        "entries": social,
        "reviewQueue": [],
        "irregularities": [],
    }

    if dry:
        print(f"social={len(social)} would write {SOCIAL_JSON} and {len(social)} profile pages")
        return 0

    os.makedirs(DIRECTORY, exist_ok=True)
    with open(SOCIAL_JSON, "w", encoding="utf-8") as fh:
        json.dump(social_catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    wanted = {f"{entry['id']}.html" for entry in social}
    wanted.add("index.html")
    removed = 0
    for name in os.listdir(DIRECTORY):
        if not name.endswith(".html"):
            continue
        if name in wanted:
            continue
        if not ID_RE.match(name[: -len(".html")]):
            continue
        os.remove(os.path.join(DIRECTORY, name))
        removed += 1

    for i, entry in enumerate(social):
        prev_entry = social[i - 1] if i > 0 else None
        next_entry = social[i + 1] if i + 1 < len(social) else None
        path = os.path.join(DIRECTORY, f"{entry['id']}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(render_profile(entry, prev_entry, next_entry))

    print(f"social={len(social)} wrote {SOCIAL_JSON}")
    print(f"wrote {len(social)} profile pages in {DIRECTORY} (removed stale {removed})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
