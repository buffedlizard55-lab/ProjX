#!/usr/bin/env python3
"""Session 27 — parse the flattened WDQS csv/tsv output saved under data/research/s27_raw/.

The fetch tool strips delimiters, so each row arrives as one glued string:
  http://www.wikidata.org/entity/Q123Name1999-01-01T00:00:00Zhandle[handle2]
We split on the entity URL, then on the ISO timestamp. Underscores are escaped as "\\_".
Rows are deduplicated against every catalog Wikidata Q-ID, normalised display name and
Instagram/TikTok handle (socialAccounts, source URLs, reviewQueue). Output:
data/research/s27_candidates.json.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"
RAW_DIR = ROOT / "data" / "research" / "s27_raw"
OUT = ROOT / "data" / "research" / "s27_candidates.json"


def norm(s: str) -> str:
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", s.lower()).strip()


def load_known():
    d = json.load(open(CATALOG))
    qids, names, handles = set(), set(), set()
    for e in d["entries"]:
        names.add(norm(e["displayName"]))
        for sa in e.get("socialAccounts", []):
            handles.add((sa.get("username") or "").lstrip("@").lower())
        for s in e.get("sources", []):
            u = s.get("url", "")
            m = re.search(r"wikidata\.org/wiki/(Q\d+)", u)
            if m:
                qids.add(m.group(1))
            m = re.search(r"instagram\.com/([^/?]+)", u)
            if m:
                handles.add(m.group(1).lower())
            m = re.search(r"tiktok\.com/@([^/?]+)", u)
            if m:
                handles.add(m.group(1).lower())
        m = re.search(r"(Q\d+)", e.get("notes", "") or "")
        if m and "Wikidata" in (e.get("notes") or ""):
            qids.add(m.group(1))
    for r in d["reviewQueue"]:
        names.add(norm(r.get("displayName") or r.get("name") or ""))
        handles.add((r.get("handle") or "").lstrip("@").lower())
        ev = r.get("evidenceFound")
        u = ev.get("sourceUrl", "") if isinstance(ev, dict) else ""
        m = re.search(r"wikidata\.org/wiki/(Q\d+)", u)
        if m:
            qids.add(m.group(1))
        m = re.search(r"Q-ID (Q\d+)", r.get("notes", "") or "")
        if m:
            qids.add(m.group(1))
    handles.discard("")
    names.discard("")
    return qids, names, handles


def parse(files):
    rows = []
    for f in files:
        txt = Path(f).read_text().replace("\\_", "_")
        for seg in re.split(r"http://www\.wikidata\.org/entity/", txt):
            seg = seg.strip()
            if not seg:
                continue
            m = re.match(r"(Q\d+?)(\D.*?|)(\d{4}-\d{2}-\d{2})T00:00:00Z(.*)$", seg, re.S)
            if not m:
                print("UNPARSED:", seg[:80], file=sys.stderr)
                continue
            qid, name, dob, h = m.groups()
            rows.append({"qid": qid, "name": name.strip(), "dob": dob,
                         "handles": h.strip(), "file": Path(f).name})
    return rows


def main():
    global CATALOG, OUT
    args = sys.argv[1:]
    # optional: --catalog PATH (dedup baseline, default data/catalog.json), --out PATH
    if "--catalog" in args:
        i = args.index("--catalog"); CATALOG = Path(args[i + 1]); del args[i:i + 2]
    if "--out" in args:
        i = args.index("--out"); OUT = Path(args[i + 1]); del args[i:i + 2]
    files = args or sorted(str(p) for p in RAW_DIR.glob("vb_wiki_off*_chunk0.txt"))
    qids, names, handles = load_known()
    rows = parse(files)
    seen, new, dup = set(), [], {"qid": 0, "name": 0, "handle": 0}
    for r in rows:
        if r["qid"] in seen:
            continue
        seen.add(r["qid"])
        if r["qid"] in qids:
            dup["qid"] += 1
        elif r["name"] and norm(r["name"]) in names:
            dup["name"] += 1
        elif r["handles"] and r["handles"].lower() in handles:
            dup["handle"] += 1
        else:
            new.append(r)
    summary = {"files": [Path(f).name for f in files], "totalRows": len(rows),
               "uniqueQids": len(seen), "dupes": dup, "new": len(new)}
    json.dump({"summary": summary, "candidates": new}, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(json.dumps(summary))
    for r in new:
        print(f"{r['qid']} | {r['name']} | {r['dob']} | {r['handles']}")


if __name__ == "__main__":
    main()
