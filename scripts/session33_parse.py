#!/usr/bin/env python3
"""
Session 33 — parse the fetch_page rendering of a WDQS tsv page (Japanese-Wikipedia slice
of the Wikidata model pool, page 4, OFFSET 450) into per-person rows.

The rendering glues everything into one line: every record starts with
``http://www.wikidata.org/entity/Q…`` followed by the ISO DOB, then ``\\|ig\\|tt\\|wiki``;
when the ``tt`` slot is empty the TikTok value (if any) is appended *after* the wiki URL.
The wiki URL is ``https://ja.wikipedia.org/wiki/<title>`` where the title consists of
percent-escaped UTF-8 bytes, ``\\_`` separators and ``(...)`` disambiguation groups — anything
else after the URL is the glued TikTok handle. Fully-ASCII titles cannot be told apart from
a glued handle: they are flagged ``ascii-title`` and cross-checked against the Wikidata label
later in the pipeline (never guessed).

Usage: python3 scripts/session33_parse.py --chunks a.txt b.txt c.txt --rows rows.json --people people.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse

REC_START = "http://www.wikidata.org/entity/"
WIKI_PREFIX = "https://ja.wikipedia.org/wiki/"
HANDLE_RE = re.compile(r"^[A-Za-z0-9._]+$")
DOB_RE = re.compile(r"^(Q\d+)(\d{4}-\d{2}-\d{2})T00:00:00Z$")


def unescape(s: str) -> str:
    return s.replace("\\_", "_").replace("\\|", "|")


def split_wiki_tail(rest: str) -> tuple[str, str]:
    """rest = text after WIKI_PREFIX (already unescaped). Returns (title_encoded, tail)."""
    i = 0
    n = len(rest)
    while i < n:
        ch = rest[i]
        if ch == "%" and i + 2 < n + 0 and re.match(r"%[0-9A-Fa-f]{2}", rest[i:i + 3]):
            i += 3
        elif ch == "_" and i + 1 < n and rest[i + 1] in "%(":
            i += 1
        elif ch == "(":
            j = rest.find(")", i)
            if j == -1:
                break
            i = j + 1
        else:
            break
    return rest[:i], rest[i:]


def parse_records(blob: str) -> list[dict]:
    parts = blob.split(REC_START)
    rows: list[dict] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        fields = part.split("\\|")
        if len(fields) != 4:
            rows.append({"raw": part, "error": f"expected 4 fields, got {len(fields)}"})
            continue
        head, ig, tt_slot, wiki_and_tail = fields
        m = DOB_RE.match(head)
        if not m:
            rows.append({"raw": part, "error": "bad head"})
            continue
        qid, dob = m.group(1), m.group(2)
        ig = unescape(ig).strip()
        tt_slot = unescape(tt_slot).strip()
        wt = unescape(wiki_and_tail)
        if not wt.startswith(WIKI_PREFIX):
            rows.append({"raw": part, "qid": qid, "error": "wiki prefix missing"})
            continue
        title_enc, tail = split_wiki_tail(wt[len(WIKI_PREFIX):])
        flags: list[str] = []
        tt = tt_slot or ""
        if title_enc == "" and tail:
            # fully ASCII title: cannot separate a glued handle — keep whole tail as title
            title_enc, tail = tail, ""
            flags.append("ascii-title")
        if tail:
            if tt_slot:
                flags.append(f"tail-with-explicit-tt:{tail}")
            elif HANDLE_RE.match(tail):
                tt = tail
            else:
                flags.append(f"tail-not-a-handle:{tail}")
        title = urllib.parse.unquote(title_enc)
        rows.append({
            "qid": qid, "dob": dob, "ig": ig or None, "tt": tt or None,
            "title": title, "url": WIKI_PREFIX + title_enc, "flags": flags,
        })
    return rows


def merge_people(rows: list[dict]) -> list[dict]:
    people: dict[str, dict] = {}
    for r in rows:
        if "error" in r:
            continue
        p = people.setdefault(r["qid"], {"qid": r["qid"], "dobs": [], "igs": [], "tts": [],
                                          "title": r["title"], "url": r["url"], "flags": []})
        for key, val in (("dobs", r["dob"]), ("igs", r["ig"]), ("tts", r["tt"])):
            if val and val not in p[key]:
                p[key].append(val)
        for f in r["flags"]:
            if f not in p["flags"]:
                p["flags"].append(f)
        if p["title"] != r["title"]:
            p["flags"].append(f"title-variant:{r['title']}")
    return list(people.values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", nargs="+", required=True)
    ap.add_argument("--rows", required=True)
    ap.add_argument("--people", required=True)
    a = ap.parse_args()
    blob = "".join(open(c, encoding="utf-8").read().strip() for c in a.chunks)
    rows = parse_records(blob)
    errs = [r for r in rows if "error" in r]
    people = merge_people(rows)
    json.dump(rows, open(a.rows, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(people, open(a.people, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"rows={len(rows)} errors={len(errs)} people={len(people)}")
    for r in errs:
        print("ERR", r)
    for p in people:
        if p["flags"] or len(p["igs"]) > 1 or len(p["dobs"]) > 1 or len(p["tts"]) > 1:
            print("FLAG", p["qid"], p["title"], p["igs"], p["tts"], p["dobs"], p["flags"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
