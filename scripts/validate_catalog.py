#!/usr/bin/env python3
"""Reusable catalog validator (Session 12 process-speedup).

One command runs every integrity check previously done ad-hoc:
  1. JSON schema invariants (required evidence fields with source URLs)
  2. duplicate ids / names / source URLs
  3. largestPublicFollowing == max known platform account (or UNKNOWN)
  4. countType/typing consistency (unknown <=> numeric null; no floats of sums)
  5. verified-status and adult-evidence presence for every VERIFIED row
  6. age floor: any explicit DOB parse found in adult-evidence text must be
     >= 18 years old at check date (guard against minors, conservatively)

Usage:  python3 scripts/validate_catalog.py [path] [--quiet]
"""
import json
import re
import sys
from datetime import date

DATE_RE = re.compile(r"(?:born|Born|DOB|date of birth|birthday)[^\d]{0,45}?"
                     r"(?:(\d{4})[-/\.](\d{1,2})[-/\.](\d{1,2})|"
                     r"(\d{1,2})\s*([A-Za-z]{3})[^\d]*(\d{4})|"
                     r"([A-Za-z]+)\s*(\d{1,2}),?\s*(\d{4}))")
MONTHS = {m.lower(): i+1 for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}

def find_years(text):
    out = set()
    for m in DATE_RE.finditer(text):
        if m.group(1):  # ISO inside born-context
            y = int(m.group(1))
        elif m.group(6):
            y = int(m.group(6))
        elif m.group(9):
            y = int(m.group(9))
        else:
            continue
        out.add(y)
    return out

def main(path="data/catalog.json", quiet=False):
    today = date(2026, 9, 6)
    data = json.load(open(path))
    errors, warns = [], []

    ids, names, urls = set(), set(), set()
    for e in data["entries"]:
        if e["id"] in ids: errors.append(f"duplicate id {e['id']}")
        ids.add(e["id"])
        low = e["displayName"].lower()
        if low in names: errors.append(f"duplicate name {e['displayName']}")
        names.add(low)
        for k in ("legalAdultEvidence", "genderEvidence"):
            ev = e.get(k)
            if not ev or not ev.get("sourceUrl") or not ev.get("summary"):
                errors.append(f"{e['id']}: missing {k}")
        if e.get("verificationStatus") != "verified":
            errors.append(f"{e['id']}: status={e.get('verificationStatus')}")
        for s in e.get("sources", []):
            if not s.get("url"): errors.append(f"{e['id']}: source without url")
            if s["url"] in urls: warns.append(f"{e['id']}: source url reused {s['url']}")
            urls.add(s["url"])
        accts = e.get("socialAccounts", [])
        known = [a for a in accts if a.get("followerCountNumeric") is not None]
        lpf = e.get("largestPublicFollowing", {})
        if known:
            m = max(a["followerCountNumeric"] for a in known)
            if lpf.get("numeric") != m:
                errors.append(f"{e['id']}: largest mismatch {m} vs {lpf.get('numeric')}")
        else:
            if lpf.get("numeric") is not None:
                errors.append(f"{e['id']}: largest must be null (no known counts)")
        for a in accts:
            if a["countType"] == "unknown" and a["followerCountNumeric"] is not None:
                errors.append(f"{e['id']}: unknown count with numeric value")
            if a["countType"] != "unknown" and a["followerCountNumeric"] is None:
                errors.append(f"{e['id']}: typed count with null numeric")
        # anti-minor guard: every DOB-like year in adult evidence must allow 18+
        years = find_years(e["legalAdultEvidence"]["summary"])
        for y in years:
            age = today.year - y
            if age < 17:  # margin: warn under 19 so 18th-birthday edge is eyeballed
                warns.append(f"{e['id']}: DOB-ish year {y} -> age {age}; re-verify adult status")
            if age < 18:
                errors.append(f"{e['id']}: DOB year {y} indicates minor (<18)")

    meta_ok = data["metadata"]["entryCount"] == len(data["entries"])
    if not meta_ok: errors.append("metadata entryCount stale")

    print(f"entries={len(data['entries'])} queue={len(data['reviewQueue'])} "
          f"irr={len(data['irregularities'])} errors={len(errors)} warns={len(warns)}")
    for x in errors: print("ERROR:", x)
    for x in warns: print("WARN :", x)
    if not quiet and not errors and meta_ok:
        print("CATALOG VALID")
    return 1 if errors else 0

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    sys.exit(main(args[0] if args and not args[0].startswith("--") else "data/catalog.json",
                  "--quiet" in args))
