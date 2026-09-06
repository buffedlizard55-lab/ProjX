#!/usr/bin/env python3
"""Session 15 — Tag and split the catalog into SOCIAL (Instagram/TikTok) vs REFERENCE
(Wikipedia / personal-website / X / YouTube / Facebook / no-social) profile buckets.

Keeps data/catalog.json as the single master source of truth (no entries removed).
Every entry gets a computed `catalogType`:
  - "social"    : has at least one Instagram or TikTok profile (socialAccounts OR an
                  IG/TikTok-marked source). These are the "Catalog Published records".
  - "reference" : everything else (documented via Wikipedia, personal/agency website,
                  X, YouTube, Facebook, press, or no public social account).

Idempotent: re-running recomputes the same tags and rewrites the derived file.
Usage:
  python3 scripts/session15_split.py [--dry-run]
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "catalog.json")
REFERENCE = os.path.join(ROOT, "data", "catalog-reference.json")
TODAY = date.today().isoformat()

SOCIAL_PLATFORMS = {"Instagram", "TikTok"}


def has_instagram_or_tiktok(entry):
    # 1. explicit social account
    for acc in entry.get("socialAccounts", []):
        if acc.get("platform") in SOCIAL_PLATFORMS:
            return True
    # 2. a source explicitly tagged Instagram/TikTok (early entries store the account
    #    as a source rather than a socialAccount)
    for src in entry.get("sources", []):
        if src.get("platform") in SOCIAL_PLATFORMS:
            return True
    return False


def main():
    dry = "--dry-run" in sys.argv
    with open(CATALOG, "r", encoding="utf-8") as fh:
        catalog = json.load(fh)

    entries = catalog["entries"]
    social = []
    reference = []
    for entry in entries:
        entry["catalogType"] = "social" if has_instagram_or_tiktok(entry) else "reference"
        if entry["catalogType"] == "social":
            social.append(entry)
        else:
            reference.append(entry)

    catalog["metadata"]["socialEntryCount"] = len(social)
    catalog["metadata"]["referenceEntryCount"] = len(reference)
    if "catalogTypeSplitAt" not in catalog["metadata"]:
        catalog["metadata"]["catalogTypeSplitAt"] = TODAY

    # Derived reference file (read-only subset for the reference subpage)
    reference_catalog = {
        "metadata": {
            "title": "ProjX Reference Profiles",
            "generatedAt": TODAY,
            "entryCount": len(reference),
            "summary": (
                "Reference profiles without a documented Instagram or TikTok account — "
                "verified adult women (18+) documented via Wikipedia, personal/agency "
                "websites, X, YouTube, Facebook, press, or other trusted sources. Derived "
                "from data/catalog.json (the single source of truth) by catalogType=reference."
            ),
            "sourceCatalog": "data/catalog.json",
        },
        "entries": reference,
        "reviewQueue": [],
        "irregularities": [],
    }

    if dry:
        print(f"total={len(entries)} social={len(social)} reference={len(reference)}")
        return

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    with open(REFERENCE, "w", encoding="utf-8") as fh:
        json.dump(reference_catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"total={len(entries)} social={len(social)} reference={len(reference)}")
    print(f"wrote {CATALOG}")
    print(f"wrote {REFERENCE}")


if __name__ == "__main__":
    main()
