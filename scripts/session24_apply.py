#!/usr/bin/env python3
"""Session 24 — Apply verified candidate records to catalog.json, update metadata,
re-run split, rebuild directory pages, and validate.
"""
from __future__ import annotations

import json
import os
import re
import sys
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"
TODAY = date(2026, 9, 6)

sys.path.insert(0, str(ROOT / "scripts"))
import session24_build as s24
import session24_runner as s24r

def main():
    apply_changes = "--apply" in sys.argv
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    
    existing_names = {s24.norm_name(e["displayName"]) for e in catalog["entries"]}
    existing_qids = set()
    existing_handles = set()

    for e in catalog["entries"]:
        for s in e.get("sources", []):
            m = re.search(r"Q\d+", s.get("url", ""))
            if m: existing_qids.add(m.group(0))
            m2 = re.search(r"Q\d+", s.get("label", ""))
            if m2: existing_qids.add(m2.group(0))
        for a in e.get("socialAccounts", []):
            if a.get("username"): existing_handles.add(a["username"].lower().lstrip("@"))
        for s in e.get("sources", []):
            if s.get("platform") in ("Instagram", "TikTok") and s.get("url"):
                u = s["url"].rstrip("/").split("/")[-1].lower().lstrip("@")
                if u: existing_handles.add(u)

    pool_cands = s24r.load_pool_candidates()
    sparql_cands = []
    with open(ROOT / "data" / "research" / "s24_sparql_raw.txt", encoding="utf-8") as f:
        for line in f:
            c = s24r.parse_sparql_row(line)
            if c: sparql_cands.append(c)

    all_cands = pool_cands + sparql_cands
    valid_new = []
    seen_names = set()
    seen_handles = set()
    seen_qids = set()

    for c in all_cands:
        name_norm = s24.norm_name(c["name"])
        qid = c.get("qid")
        h_set = {h.lower().lstrip("@") for h in c.get("handles", {}).values() if h}
        if name_norm in existing_names or name_norm in seen_names: continue
        if qid and (qid in existing_qids or qid in seen_qids): continue
        if h_set & (existing_handles | seen_handles): continue
        if not h_set: continue
        
        # Guard: age 18+ check
        if s24.age_on(c["dob"], TODAY) < 18:
            continue
            
        seen_names.add(name_norm)
        if qid: seen_qids.add(qid)
        seen_handles.update(h_set)
        valid_new.append(c)

    print(f"Candidates to add: {len(valid_new)}")
    
    # Generate sequential IDs starting after max ID
    current_max_id = max(int(e["id"].split("-")[-1]) for e in catalog["entries"])
    next_id_num = current_max_id + 1
    
    new_entries = []
    for cand in valid_new:
        entry_id = f"W-2026-{next_id_num:03d}"
        entry = s24.build_entry_record(entry_id, cand)
        new_entries.append(entry)
        next_id_num += 1

    print(f"Generated {len(new_entries)} new entries from {new_entries[0]['id']} to {new_entries[-1]['id']}")
    
    if not apply_changes:
        print("\n[dry run] Re-run with --apply to commit changes.")
        return 0

    # Append to catalog
    catalog["entries"].extend(new_entries)
    catalog["metadata"]["entryCount"] = len(catalog["entries"])
    catalog["metadata"]["generatedAt"] = TODAY.isoformat()
    catalog["metadata"]["summary"] += (
        f" Session 24 expanded coverage with {len(new_entries)} new verified adult female creator "
        f"profiles across NCAA volleyball, beach volleyball, European and international women's "
        f"volleyball leagues, fitness models, swimwear / bikini fashion creators, and fashion models. "
        f"All records have documented Instagram / TikTok profiles and verified 18+ dates of birth."
    )
    
    # Record irregularity note
    irr = {
        "id": f"IRR-2026-09-07-{len(catalog.get('irregularities', [])) + 1:03d}",
        "detectedAt": TODAY.isoformat(),
        "severity": "info",
        "title": "Session 24: High-precision expansion of Volleyball, Fitness, Swimwear, and Modeling",
        "details": (
            f"Added {len(new_entries)} unique verified creator records (W-2026-{current_max_id + 1:03d}.."
            f"W-2026-{next_id_num - 1:03d}) focusing on NCAA volleyball, beach volleyball, European/international "
            f"leagues, fitness, and fashion/swimwear creators. All rows carry Instagram or TikTok accounts and "
            f"are classified catalogType=social. Verified birth dates ensure all creators are adult women (18+)."
        ),
        "resolution": f"Catalog now contains {len(catalog['entries'])} verified entries."
    }
    catalog.setdefault("irregularities", []).append(irr)

    # Write updated catalog
    with open(CATALOG, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Updated {CATALOG} with {len(catalog['entries'])} total entries.")

    # Re-run split script to rebuild catalog-social, catalog-social-known, catalog-social-unknown, catalog-reference, and directory/ pages
    print("Running session15_split.py...")
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "session15_split.py")])
    
    # Run validator
    print("Running validate_catalog.py...")
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "validate_catalog.py")])
    
    print("\nSession 24 completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
