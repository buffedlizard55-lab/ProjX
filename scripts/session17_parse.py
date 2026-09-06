#!/usr/bin/env python3
"""Session 17 - parse the P54 club-roster harvest into s17_master.tsv.

Pool: female items with an Instagram/TikTok handle that are members (P54) of a team whose
sport (P641) includes volleyball/beach volleyball, WITHOUT any volleyball occupation/sport
statement of their own (the population the s16 occupation/sport sweep could not see).

Raw inputs (escapes preserved as fetched):
  s17_pool_new.txt          candidate QIDs (227, none previously cited in the catalog)
  s17_det00..05.txt         qid|name|dob|ig|x|tt|countryQID|gender##   (country as Q-ID)
  s17_tm00..05.txt          qid|T/B|teamQID##   (T=indoor team, B=beach team)
  s17_tmL0/1.txt            teamQID|label##
  s17_tmS0/1.txt            teamQID|sportCount##  (number of distinct P641 sports)
  s17_cty.txt               countryQID|label##
  s17_ev6.txt               qid|S/U/W|value##   (only fetched for volleyball-corroborated rows)
  s17_cls6.txt              qid|occs|sports##   (only fetched for volleyball-corroborated rows)

Output: data/research/s17_master.tsv
  qid|name|dob|ig|x|tt|countries|srcs|urls|wiki|teams|occs|sports|status
where status is:
  volleyball            member of a volleyball-only club (sportCount==1) and no contradicting
                        personal sport/athlete occupation
  volleyball-no-label   as above but the item has no English label (display name unknowable
                        without guessing -> not catalogued, retained here)
  sport-conflict        single-sport volleyball club member whose own P106/P641 names a
                        different sport (cross-sport club artifact)
  umbrella-only         only multi-sport club memberships (university/omnisport umbrellas)
"""
from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(ROOT, "data", "research")

# occupation/sport Q-IDs that contradict a volleyball claim (different sport family)
VOLLY_FAMILY = {"Q1734", "Q4543", "Q597628"}          # volleyball, beach volleyball, sitting volleyball
OTHER_SPORT_OCC_PREFIXES = {
    "Q3665646": "basketball player", "Q937857": "association football player",
    "Q16947675": "gymnast", "Q24037210": "rhythmic gymnast", "Q12840545": "handball player",
    "Q57749966": "beach handball player", "Q13474373": "professional wrestler",
    "Q2066131": "athlete",  # generic athlete = ambiguous, allowed (not a contradiction)
    "Q28971125": "cheerleader",  # cheerleader for a volleyball team is not a volleyball player
}


def unescape(text: str) -> str:
    return re.sub(r"\\([|_#*`\[\]])", r"\1", text)


def rows_of(path):
    if not os.path.exists(path):
        return []
    out = []
    for row in re.split(r"##|\n", unescape(open(path, encoding="utf-8").read())):
        row = row.strip()
        if row and not row.startswith("#"):
            out.append(row.split("|"))
    return out


def main():
    pool = [l.strip() for l in open(os.path.join(RESEARCH, "s17_pool_new.txt")) if l.strip()]

    det = {}
    for n in range(6):
        for p in rows_of(os.path.join(RESEARCH, f"s17_det{n:02d}.txt")):
            if len(p) < 8:
                print("!! det row:", p)
                continue
            qid, name, dob, ig, x, tt, cty, gender = p[:8]
            r = det.setdefault(qid, {"names": set(), "dob": "", "ig": "", "x": "", "tt": "",
                                     "ctys": [], "gender": ""})
            if name and not name.startswith("Q"):
                r["names"].add(name)
            if not r["dob"]:
                r["dob"] = dob
            for k, v in (("ig", ig), ("x", x), ("tt", tt)):
                r[k] = r[k] or v
            if cty and cty not in r["ctys"]:
                r["ctys"].append(cty)
            r["gender"] = r["gender"] or gender

    cty_label = {p[0]: p[1] for p in rows_of(os.path.join(RESEARCH, "s17_cty.txt")) if len(p) == 2}
    team_label = {}
    for n in range(2):
        for p in rows_of(os.path.join(RESEARCH, f"s17_tmL{n}.txt")):
            if len(p) == 2:
                team_label[p[0]] = p[1]
    single_sport = set()
    for n in range(2):
        for p in rows_of(os.path.join(RESEARCH, f"s17_tmS{n}.txt")):
            if len(p) == 2 and p[1] == "1":
                single_sport.add(p[0])

    teams_of = {}
    for n in range(6):
        for p in rows_of(os.path.join(RESEARCH, f"s17_tm{n:02d}.txt")):
            if len(p) == 3:
                teams_of.setdefault(p[0], []).append((p[1], p[2]))  # (tag, teamQID)

    ev = {}
    for p in rows_of(os.path.join(RESEARCH, "s17_ev6.txt")):
        if len(p) != 3 or p[1] not in ("S", "U", "W"):
            print("!! ev row:", p)
            continue
        r = ev.setdefault(p[0], {"srcs": [], "urls": [], "wiki": []})
        if p[1] == "S":
            label, _, url = p[2].partition("~")
            if label and label not in r["srcs"]:
                r["srcs"].append(label)
            if url and url not in r["urls"]:
                r["urls"].append(url)
        elif p[1] == "U" and p[2] not in r["urls"]:
            r["urls"].append(p[2])
        elif p[1] == "W" and p[2] not in r["wiki"]:
            r["wiki"].append(p[2])

    cls = {}
    for p in rows_of(os.path.join(RESEARCH, "s17_cls6.txt")):
        if len(p) != 3:
            print("!! cls row:", p)
            continue
        r = cls.setdefault(p[0], {"occs": [], "sports": []})
        if p[1] != "NONE" and p[1] not in r["occs"]:
            r["occs"].append(p[1])
        if p[2] != "NONE" and p[2] not in r["sports"]:
            r["sports"].append(p[2])

    def status(qid):
        ts = teams_of.get(qid, [])
        single = [t for _, t in ts if t in single_sport]
        if not single:
            return "umbrella-only", []
        c = cls.get(qid, {"occs": [], "sports": []})
        sport_keys = {v.split("=")[0] for v in c["sports"]}
        occ_keys = {v.split("=")[0] for v in c["occs"]}
        # contradicting personal sport statements (outside the volleyball family)
        contra = (sport_keys - VOLLY_FAMILY) or {
            k for k in occ_keys
            if k in OTHER_SPORT_OCC_PREFIXES and k not in ("Q2066131",)
            and OTHER_SPORT_OCC_PREFIXES[k] != "athlete"
        }
        if contra:
            return "sport-conflict", sorted(contra)
        return "volleyball", [team_label.get(t, t) for t in single]

    out_path = os.path.join(RESEARCH, "s17_master.tsv")
    counts = {}
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("# s17 master: P54 club-roster pool, 14 cols as s16 + status in col 14\n")
        fh.write("# qid|name|dob|ig|x|tt|countries|srcs|urls|wiki|teams|occs|sports|status\n")
        for qid in pool:
            d = det.get(qid)
            if d is None:
                print("!! no detail row for", qid)
                continue
            names = sorted(d["names"])
            name = names[0] if names else qid  # no English label -> Q-ID placeholder
            st, contra = status(qid)
            if st == "volleyball" and name == qid:
                st = "volleyball-no-label"
            counts[st] = counts.get(st, 0) + 1
            allteams = []
            for _, t in teams_of.get(qid, []):
                lbl = team_label.get(t, t)
                if lbl not in allteams:
                    allteams.append(lbl)
            c = cls.get(qid, {"occs": [], "sports": []})
            e = ev.get(qid, {"srcs": [], "urls": [], "wiki": []})
            fh.write("|".join([
                qid, name, d["dob"], d["ig"], d["x"], d["tt"],
                ";".join(cty_label.get(cq, cq) for cq in d["ctys"]),
                ";".join(e["srcs"]), ";".join(e["urls"]), ";".join(e["wiki"]),
                ";".join(allteams),
                ";".join(c["occs"]), ";".join(c["sports"]),
                st + ((",conflict:" + ",".join(contra)) if contra else ""),
            ]) + "\n")
    print("master rows:", len(pool), "status counts:", counts, "->", os.path.relpath(out_path, ROOT))


if __name__ == "__main__":
    main()
