#!/usr/bin/env python3
"""Session 26 — Parse raw SPARQL harvests, dedupe against catalog, emit candidate lists.

Raw harvest format (one row per '##' segment, pipe-separated, backslash-escaped):
  qid|name|dob|ig|tt|occL|refUrl|wiki
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "data/catalog.json").read_text())
RESEARCH = ROOT / "data/research"

def unescape(s: str) -> str:
    return s.replace("\\|", "|").replace("\\_", "_")

def parse_file(path: Path) -> list[dict]:
    raw = path.read_text()
    rows = []
    for seg in raw.split("##"):
        seg = unescape(seg).strip()
        if not seg:
            continue
        parts = seg.split("|")
        if len(parts) < 8:
            continue
        rows.append({
            "qid": parts[0],
            "name": parts[1],
            "dob": parts[2],
            "ig": parts[3],
            "tt": parts[4],
            "occ": parts[5],
            "refUrl": parts[6],
            "wiki": parts[7],
            "slice": path.stem,
        })
    return rows

def catalog_index():
    names, handles, qids = set(), set(), set()
    def add_handle(h):
        if h:
            handles.add(re.sub(r"^@+", "", h.strip().lower()))
    for e in CATALOG["entries"]:
        for s in e.get("sources", []):
            txt = f'{s.get("label","")} {s.get("url","")}'
            for m in re.findall(r"Q\d{6,}", txt):
                qids.add(m)
        if e.get("notes"):
            for m in re.findall(r"Q\d{6,}", e["notes"]):
                qids.add(m)
        dn = e.get("displayName", "")
        names.add(re.sub(r"\s+", " ", dn.lower().strip()))
        for sa in e.get("socialAccounts", []):
            add_handle(sa.get("username"))
    for r in CATALOG.get("reviewQueue", []):
        names.add(re.sub(r"\s+", " ", (r.get("name") or "").lower().strip()))
        add_handle(r.get("username"))
    return names, handles, qids

def is_dupe(row, names, handles, qids):
    if row["qid"] in qids:
        return "qid"
    nm = re.sub(r"\s+", " ", row["name"].lower().strip())
    if nm and nm in names:
        return "name"
    for h in (row["ig"], row["tt"]):
        h = re.sub(r"^@+", "", h.strip().lower())
        if h and h in handles:
            return "handle"
    return None

def main():
    names, handles, qids = catalog_index()
    all_rows = []
    for f in sorted(RESEARCH.glob("s26_*.tsv")):
        all_rows.extend(parse_file(f))
    # per-qid consolidation: prefer row with both handles; keep all ref/wiki URLs
    by_qid = {}
    for r in all_rows:
        e = by_qid.setdefault(r["qid"], {**r, "refUrls": set(), "wikis": set()})
        if r["refUrl"]:
            e["refUrls"].add(r["refUrl"])
        if r["wiki"]:
            e["wikis"].add(r["wiki"])
        if (r["ig"] and not e["ig"]) or (r["tt"] and not e["tt"]):
            e["ig"] = e["ig"] or r["ig"]
            e["tt"] = e["tt"] or r["tt"]
        if not e["occ"] and r["occ"]:
            e["occ"] = r["occ"]
    dup_counts = {}
    new_rows, dup_rows = [], []
    for qid, e in sorted(by_qid.items()):
        e["refUrls"] = sorted(e["refUrls"])
        e["wikis"] = sorted(e["wikis"])
        d = is_dupe(e, names, handles, qids)
        if d:
            dup_counts[d] = dup_counts.get(d, 0) + 1
            dup_rows.append({**e, "dupReason": d})
        else:
            new_rows.append(e)
    out = {
        "totalRows": len(all_rows),
        "uniqueQids": len(by_qid),
        "dupes": dup_counts,
        "new": new_rows,
        "dupesList": dup_rows,
    }
    dest = ROOT / "data/research/s26_candidates.json"
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"rows={out['totalRows']} uniqueQids={out['uniqueQids']} dupes={dup_counts} new={len(new_rows)}")
    for e in new_rows:
        print(f"  {e['qid']} | {e['name']} | {e['dob']} | ig={e['ig'] or '-'} tt={e['tt'] or '-'} | {e['occ']} | ref={len(e['refUrls'])} wiki={len(e['wikis'])}")

if __name__ == "__main__":
    main()
