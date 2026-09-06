#!/usr/bin/env python3
"""Session 16 - parse the raw harvest (detail rows + evidence rows) into one master TSV.

Raw inputs (all markdown-escaped as rendered by the fetch tool; escapes are stripped):
  data/research/s16_det00.txt .. s16_det11.txt   qid|name|dob|ig|x|tt|country##
  data/research/s16_ev0.txt   .. s16_ev4.txt     qid|tag|value##  (tag in {S,U,W,N})
  pool QID lists: s16_poolI_ig_ord{0,100,200,300}.txt, s16_poolI_xonly.txt, s16_poolH.tsv

Output: data/research/s16_master.tsv (one line per QID):
  qid|name|dob|ig|x|tt|countries;|srcs;|urls;|wiki|teams;
Rows are collapsed by QID (multi-citizenship and repeated evidence rows de-duplicated).
Handles are compared case-insensitively; DOBs keep Wikidata's recorded string.
"""
from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(ROOT, "data", "research")


def unescape(text: str) -> str:
    # the fetch renderer escapes markdown punctuation with backslashes
    return re.sub(r"\\([|_#*`\[\]])", r"\1", text)


def parse_rows(path: str):
    """Split a raw file into unescaped rows. Rows end with ## (CONCAT output) or with a
    newline (hand-collapsed files); comment lines start with '#'."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    raw = unescape(raw)
    for row in re.split(r"##|\n", raw):
        row = row.strip()
        if row and not row.startswith("#") and row != "row":
            yield row


def load_details():
    det = {}
    for n in range(15):
        path = os.path.join(RESEARCH, f"s16_det{n:02d}.txt")
        if not os.path.exists(path):
            continue
        for row in parse_rows(path):
            parts = row.split("|")
            if len(parts) < 7:
                print(f"  !! malformed detail row in s16_det{n:02d}: {row[:80]}")
                continue
            qid, name, dob, ig, x, tt, country = parts[:7]
            gender = parts[7] if len(parts) > 7 else ""  # det12/13 carry a gender column
            if not re.fullmatch(r"Q\d+", qid):
                print(f"  !! non-QID detail row in s16_det{n:02d}: {row[:80]}")
                continue
            rec = det.setdefault(qid, {"name": "", "dob": "", "ig": "", "x": "", "tt": "",
                                       "countries": [], "seen": [], "gender": ""})
            if not rec["name"]:
                rec["name"] = name
            if not rec["dob"]:
                rec["dob"] = dob
            if gender and not rec["gender"]:
                rec["gender"] = gender
            for key, val in (("ig", ig), ("x", x), ("tt", tt)):
                if val and val not in rec[key]:
                    rec[key] = rec[key] or val  # first value wins; later dup rows skipped
            if country:
                for c in country.split(";"):
                    if c and c not in rec["countries"]:
                        rec["countries"].append(c)
            rec["seen"].append(f"det{n:02d}")
    return det


def load_classes():
    """occupation (P106) / sport (P641) classification rows; 'NONE' = statement absent."""
    occ = {}
    for n in range(7):
        path = os.path.join(RESEARCH, f"s16_cls{n}.txt")
        if not os.path.exists(path):
            continue
        for row in parse_rows(path):
            parts = row.split("|")
            if len(parts) != 3 or not re.fullmatch(r"Q\d+", parts[0]):
                print(f"  !! unexpected class row in s16_cls{n}: {row[:80]}")
                continue
            qid, occv, sportv = parts
            rec = occ.setdefault(qid, {"occs": [], "sports": []})
            for tag, val, bucket in (("occ", occv, "occs"), ("sport", sportv, "sports")):
                if val and val != "NONE" and val not in rec[bucket]:
                    rec[bucket].append(val)
    return occ


COLLEGE_TEAM_RE = re.compile(
    r"cornhuskers|gators|bruins|trojans|nittany lions|golden gophers|boilermakers|"
    r"gauchos|seminoles|mountaineers|badgers|cardinal|longhorns|lady volunteers|"
    r"tigers|rams|fighting illini|ducks|razorbacks|aggies|crimson tide|pioneers|"
    r"long beach state|wisconsin badgers", re.I)


def classify(rec, clsrec):
    """objective group assignment: college team membership > beach markers > indoor."""
    teams = rec["teams"]
    college = [t for t in teams if COLLEGE_TEAM_RE.search(t)]
    beach = any(("Q17361156" in v) or ("Q4543" in v) for v in clsrec["occs"] + clsrec["sports"]) if clsrec else False
    indoor = any(("Q15117302" in v) or ("Q1734" in v) for v in clsrec["occs"] + clsrec["sports"]) if clsrec else False
    if college and not beach:
        group = "ncaa"
    elif beach:
        group = "beach"
    else:
        group = "intl"
    return group, college, beach, indoor


def load_evidence():
    ev = {}
    for n in range(6):
        path = os.path.join(RESEARCH, f"s16_ev{n}.txt")
        if not os.path.exists(path):
            continue
        for row in parse_rows(path):
            # some rows lost their leading "Q" in rendering; normalise
            if re.match(r"^\d+", row):
                row = "Q" + row
            parts = row.split("|")
            if len(parts) != 3:
                print(f"  !! malformed evidence row in s16_ev{n}: {row[:80]}")
                continue
            qid, tag, value = parts
            if not re.fullmatch(r"Q\d+", qid) or tag not in ("S", "U", "W", "N"):
                print(f"  !! unexpected evidence row in s16_ev{n}: {row[:80]}")
                continue
            rec = ev.setdefault(qid, {"srcs": [], "urls": [], "wiki": [], "teams": []})
            if tag == "S":
                label, _, url = value.partition("~")
                if label and label not in rec["srcs"]:
                    rec["srcs"].append(label)
                if url and url not in rec["urls"]:
                    rec["urls"].append(url)
            elif tag == "U":
                if value and value not in rec["urls"]:
                    rec["urls"].append(value)
            elif tag == "W":
                if value and value not in rec["wiki"]:
                    rec["wiki"].append(value)
            else:  # N - US collegiate / national team membership names
                if value and value not in rec["teams"]:
                    rec["teams"].append(value)
    return ev


def load_pool_qids():
    qids = set()
    for name in ("s16_poolI_ig_ord0.txt", "s16_poolI_ig_ord100.txt",
                 "s16_poolI_ig_ord200.txt", "s16_poolI_ig_ord300.txt",
                 "s16_poolI_xonly.txt"):
        path = os.path.join(RESEARCH, name)
        with open(path, encoding="utf-8") as fh:
            for tok in unescape(fh.read()).split():
                if re.fullmatch(r"Q\d+", tok):
                    qids.add(tok)
    with open(os.path.join(RESEARCH, "s16_poolH.tsv"), encoding="utf-8") as fh:
        for line in fh:
            for tok in unescape(line).split():
                if re.fullmatch(r"Q\d+", tok):
                    qids.add(tok)
    return qids


def main():
    det = load_details()
    ev = load_evidence()
    cls = load_classes()
    pool = load_pool_qids()
    everything = sorted(set(det) | set(ev) | pool, key=lambda q: int(q[1:]))

    print(f"detail QIDs      : {len(det)}")
    print(f"evidence QIDs    : {len(ev)}")
    print(f"class QIDs       : {len(cls)}")
    print(f"pool QIDs        : {len(pool)}")
    only_pool = sorted(pool - set(det) - set(ev), key=lambda q: int(q[1:]))
    print(f"pool with no detail AND no evidence row: {len(only_pool)} {only_pool}")
    no_dob = sorted(q for q in everything if q in ev and q not in det)
    print(f"evidence-but-no-detail (=> no DOB recorded): {len(no_dob)} {no_dob}")
    no_cls = sorted(set(everything) - set(cls))
    print(f"no classification row at all: {len(no_cls)} {no_cls}")

    out = os.path.join(RESEARCH, "s16_master.tsv")
    groups = {}
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("# qid|name|dob|ig|x|tt|countries|srcs|urls|wiki|teams|occs|sports|group  (session 16 master, collapsed by QID)\n")
        for qid in everything:
            d = det.get(qid, {})
            e = ev.get(qid, {"srcs": [], "urls": [], "wiki": [], "teams": []})
            c = cls.get(qid, {"occs": [], "sports": []})
            merged = {"teams": e["teams"]}
            group, college, beach, indoor = classify(merged, c)
            groups[group] = groups.get(group, 0) + 1
            fh.write("|".join([
                qid,
                d.get("name", ""),
                d.get("dob", ""),
                d.get("ig", ""),
                d.get("x", ""),
                d.get("tt", ""),
                ";".join(d.get("countries", [])),
                ";".join(e["srcs"]),
                ";".join(e["urls"]),
                ";".join(e["wiki"]),
                ";".join(e["teams"]),
                ";".join(c["occs"]),
                ";".join(c["sports"]),
                group,
            ]) + "\n")
    print(f"master rows      : {len(everything)} -> {os.path.relpath(out, ROOT)}")
    print(f"group counts     : {groups}")


if __name__ == "__main__":
    main()
