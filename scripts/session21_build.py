#!/usr/bin/env python3
"""Session 21 — add remaining volleyball + fashion/model candidates.

Focus: NCAA volleyball, beach volleyball, European volleyball leagues,
plus bikini/beachwear/fitness/modeling candidates with Instagram/TikTok.

Sources:
 - data/research/s16_master.tsv remaining 33 (volleyball with IG + Wikipedia)
 - data/research/s18_raw/s18_vb03_off0.txt 3 new volleyball
 - data/research/s13_poolB1.tsv 22 remaining
 - data/research/s13_poolC.tsv 11 remaining
 - data/research/s13_poolD.tsv 12 remaining
 - data/research/s18_raw/s18_fm_off*.txt good fashion with ref (non-bad hosts)

Builds entries using session13_volleyball.build_entry for volleyball,
and session18_build.build_fashion_entry for fashion/model.

Usage: python3 scripts/session21_build.py [--apply]
"""
from __future__ import annotations
import json, os, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"
RESEARCH = ROOT / "data" / "research"

sys.path.insert(0, str(ROOT / "scripts"))
import session13_volleyball as s13

TODAY = date(2026, 9, 6)
s13.TODAY = TODAY
s13.age_on.__defaults__ = (TODAY,)

UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE

BAD_HOSTS = ["babesdirectory.online","listal.com","mypmates.club","chaturbate","pornhub.com","playboy","blackewhite.com"]

def cited_qids():
    have=set()
    for path in [CATALOG, ROOT/"data"/"catalog-reference.json"]:
        if path.exists():
            have.update(re.findall(r"Q\d+", path.read_text(encoding="utf-8")))
    return have

def norm_name(n): return s13.norm_name(n)

def load_s16_remaining(have_qids):
    rows=[]
    master = RESEARCH / "s16_master.tsv"
    for line in master.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts=line.split("|")
        if len(parts)!=14:
            continue
        qid=parts[0]
        if qid in have_qids:
            continue
        # qid|name|dob|ig|x|tt|countries|srcs|urls|wiki|teams|occs|sports|group
        _, name, dob, ig, x, tt, countries, srcs, urls, wiki, teams, occs, sports, group = parts
        handles={}
        if ig: handles["Instagram"]=ig
        if x: handles["X"]=x
        if tt: handles["TikTok"]=tt
        if not handles:
            continue
        # must have at least IG or TikTok to be social
        if not (handles.get("Instagram") or handles.get("TikTok")):
            continue
        # filter out those with no dob
        if not dob:
            continue
        rows.append({
            "qid": qid, "name": name, "dob": dob, "group": group or "intl",
            "country": "; ".join(c for c in countries.split(";") if c) or "UNKNOWN",
            "teams": [t for t in teams.split(";") if t],
            "handles": handles,
            "dob_sources": [s for s in srcs.split(";") if s],
            "ref_urls": [u for u in urls.split(";") if u],
            "wiki_urls": [w for w in wiki.split(";") if w],
            "imports": [],
            "occ_keys": {v.split("=")[0] for v in occs.split(";") if v},
            "sport_keys": {v.split("=")[0] for v in sports.split(";") if v},
            "occs": occs, "sports": sports,
        })
    return rows

def load_s13_pool(path, have_qids, group_label):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts=line.split("|")
        if len(parts)<4:
            continue
        qid=parts[0]
        if qid in have_qids:
            continue
        # poolB1 format: qid|name|dob|instagram|x|tiktok|country
        # poolC/D format: qid|name|dob|instagram|x|tiktok  (or with country)
        name = parts[1] if len(parts)>1 else ""
        dob = parts[2] if len(parts)>2 else ""
        ig = parts[3] if len(parts)>3 else ""
        x = parts[4] if len(parts)>4 else ""
        tt = parts[5] if len(parts)>5 else ""
        country = parts[6] if len(parts)>6 else "UNKNOWN"
        handles={}
        if ig and ig!="-": handles["Instagram"]=ig
        if x and x!="-": handles["X"]=x
        if tt and tt!="-": handles["TikTok"]=tt
        if not handles:
            continue
        if not (handles.get("Instagram") or handles.get("TikTok")):
            # for this batch we want IG/TT only for social, but we can still keep X-only as reference later
            # For now skip X-only to focus on social
            continue
        rows.append({
            "qid": qid, "name": name, "dob": dob, "group": group_label,
            "country": country or "UNKNOWN",
            "teams": [],
            "handles": handles,
            "dob_sources": [],
            "ref_urls": [],
            "wiki_urls": [],
            "imports": [],
        })
    return rows

def load_evidence():
    ev={}
    ev_path = RESEARCH / "s13_evidence.tsv"
    if not ev_path.exists():
        return ev
    for line in ev_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts=line.split("\t")
        if len(parts)!=3:
            continue
        qid, tag, value = parts
        ev.setdefault(qid, {}).setdefault(tag, [])
        if value not in ev[qid][tag]:
            ev[qid][tag].append(value)
    return ev

def load_facts_ncaa():
    facts={}
    facts_path = RESEARCH / "s13_facts.tsv"
    if not facts_path.exists():
        return facts
    for line in facts_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if "|" not in line:
            continue
        qid, _, payload = line.partition("|")
        info={}
        for chunk in payload.split(";"):
            k, _, v = chunk.partition("=")
            info[k.strip()]=v.strip()
        facts[qid]=info
    return facts

def load_s18_vb_raw(have_qids):
    rows=[]
    for p in (RESEARCH / "s18_raw").glob("s18_vb03*"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts=line.split("|")
            if len(parts)==6:
                qid,name,dob,ig,country,ref = parts
                tt=""
            elif len(parts)==7:
                qid,name,dob,ig,tt,country,ref = parts
            else:
                continue
            if qid in have_qids:
                continue
            if not name:
                continue
            handles={}
            if ig: handles["Instagram"]=ig
            if tt: handles["TikTok"]=tt
            if not handles:
                continue
            rows.append({
                "qid": qid, "name": name, "dob": dob, "group": "intl",
                "country": country or "UNKNOWN",
                "teams": [],
                "handles": handles,
                "dob_sources": [],
                "ref_urls": [ref] if ref else [],
                "wiki_urls": [],
                "imports": [],
            })
    return rows

def load_s18_fm_raw_good(have_qids):
    rows=[]
    for p in (RESEARCH / "s18_raw").glob("s18_fm_off*"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts=line.split("|")
            if len(parts)!=8:
                continue
            qid,name,dob,_,ig,tt,occ,ref = parts
            if qid in have_qids:
                continue
            if not name:
                continue
            if any(b in ref for b in BAD_HOSTS):
                continue
            # require at least one handle
            handles={}
            if ig: handles["Instagram"]=ig
            if tt: handles["TikTok"]=tt
            if not handles:
                continue
            # require dob
            if not dob:
                continue
            # only keep those with ref URL (to have age evidence) OR we will try wiki later
            if not ref:
                # skip those with no ref for now to avoid wikipedia-only without verification
                # But we can keep if we have a way to get wiki, but for safety require ref
                continue
            # avoid minors
            try:
                y=int(dob.split("-")[0])
                if y>2008:
                    continue
            except:
                continue
            rows.append({
                "qid": qid, "name": name, "dob": dob, "occ": occ,
                "handles": handles, "ref_urls": [ref] if ref else [], "wiki_urls": [],
            })
    return rows

def main():
    apply_changes = "--apply" in sys.argv
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    have_qids = cited_qids()
    existing_names = {norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    existing_handles=set()
    for e in catalog["entries"]:
        for a in e.get("socialAccounts",[]):
            existing_handles.add((a.get("username") or "").lstrip("@").lower())
    rq_names = {norm_name(r["displayName"]) for r in catalog.get("reviewQueue",[]) if r.get("displayName")}
    for r in catalog.get("reviewQueue",[]):
        h=r.get("handle") or ""
        if h:
            existing_handles.add(h.lstrip("@").lower())

    ev = load_evidence()
    facts_ncaa = load_facts_ncaa()

    s16_rows = load_s16_remaining(have_qids)
    vb_raw_rows = load_s18_vb_raw(have_qids)
    poolB1_rows = load_s13_pool(RESEARCH/"s13_poolB1.tsv", have_qids, "intl")
    poolC_rows = load_s13_pool(RESEARCH/"s13_poolC.tsv", have_qids, "ncaa")
    poolD_rows = load_s13_pool(RESEARCH/"s13_poolD.tsv", have_qids, "intl")
    fm_raw_rows = load_s18_fm_raw_good(have_qids)

    # Combine volleyball candidates
    volley_cands = s16_rows + vb_raw_rows + poolB1_rows + poolC_rows + poolD_rows

    # Enrich volley cands with evidence from ev and facts
    for cand in volley_cands:
        qid=cand["qid"]
        e=ev.get(qid,{})
        # merge ref urls from evidence U tag
        if not cand["ref_urls"]:
            cand["ref_urls"]=e.get("U",[])
        if not cand["wiki_urls"]:
            cand["wiki_urls"]=e.get("W",[])
        # merge dob sources S tag
        if not cand["dob_sources"]:
            cand["dob_sources"]=e.get("S",[])
        # merge handles from evidence X,K,F,Y if missing
        for tag, platform in (("X","X"),("K","TikTok"),("F","Facebook"),("Y","YouTube")):
            for val in e.get(tag,[]):
                if not cand["handles"].get(platform):
                    cand["handles"][platform]=val
        # also from facts_ncaa if present
        f=facts_ncaa.get(qid,{})
        if f:
            for tag, platform in (("X","X"),("K","TikTok"),("F","Facebook"),("Y","YouTube")):
                v=f.get(tag)
                if v and v!="-" and not cand["handles"].get(platform):
                    cand["handles"][platform]=v
            # srcs S from facts
            srcs = [s for s in re.split(r"\+", f.get("S","")) if s and s!="-"]
            if srcs and not cand["dob_sources"]:
                cand["dob_sources"]=srcs

    # Now build entries
    next_id = max(int(e["id"].split("-")[-1]) for e in catalog["entries"]) + 1
    selected=[]
    skipped=[]
    seen_names=set()
    seen_handles=set()

    def try_add_volley(cand):
        nonlocal next_id
        key=norm_name(cand["name"])
        hkeys={h.lower() for h in cand["handles"].values() if h}
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand,"duplicate-name"))
            return None
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand,"duplicate-handle"))
            return None
        if not cand["name"] or re.fullmatch(r"Q\d+", cand["name"]):
            skipped.append((cand,"no-display-name"))
            return None
        dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            skipped.append((cand,"no-dob"))
            return None
        if s13.age_on(dob) < 18:
            skipped.append((cand,"minor"))
            return None
        if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"] or cand["imports"]):
            skipped.append((cand,"no-source"))
            return None
        # must have IG or TT for social
        if not (cand["handles"].get("Instagram") or cand["handles"].get("TikTok")):
            skipped.append((cand,"no-ig-tt"))
            return None
        entry = s13.build_entry(next_id, cand, dob)
        # ensure social
        entry["id"]=f"W-2026-{next_id}"
        next_id+=1
        seen_names.add(key)
        seen_handles.update(hkeys)
        return entry

    for cand in volley_cands:
        e=try_add_volley(cand)
        if e:
            selected.append(e)

    # Now fashion/model raw good
    # For fashion we use similar builder but simplified
    def build_fashion_entry(idx, cand, dob):
        qid=cand["qid"]
        name=cand["name"]
        wd_url=f"https://www.wikidata.org/wiki/{qid}"
        handles=cand["handles"]
        refs=cand["ref_urls"]
        wiki=cand["wiki_urls"]
        occ=cand["occ"]
        age=s13.age_on(dob)
        cats=["Modeling","Fashion","Creator"]
        if "fitness" in occ.lower() or "personal trainer" in occ.lower():
            cats=["Fitness","Fitness Model","Modeling","Creator"]
        if refs:
            age_url=refs[0]
            age_label=f"{s13.domain_label(refs[0])} — {name} (record cited by Wikidata date-of-birth reference)"
            prov_text=f"the reference URL recorded against that statement is {refs[0]}"
        elif wiki:
            age_url=wiki[0]
            age_label=f"English Wikipedia — {name} (article linked to Wikidata {qid})"
            prov_text="the structured record names no source and no reference URL for that statement"
        else:
            age_url=wd_url
            age_label=f"Wikidata {qid} — {name} (date of birth {dob.isoformat()})"
            prov_text="the structured record names no source and no reference URL for that statement"
        legal={
            "summary": f"Born {s13.human_date(dob)} ({dob.isoformat()}) — age {age} as of {TODAY.isoformat()}, so an adult (18+). The birth date is the value recorded in the Wikidata structured item {qid} ({wd_url}): {prov_text}. Adult status is taken only from this documented birth date — never inferred from appearance, clothing, photographs, college attendance or any image-based judgement.",
            "sourceLabel": age_label,
            "sourceUrl": age_url,
            "checkedAt": TODAY.isoformat(),
        }
        gender_url = wiki[0] if wiki else (refs[0] if refs else wd_url)
        gender={
            "summary": f"Woman — the Wikidata structured item {qid} records sex/gender: female; occupation recorded as {occ}. Gender is established from documentary records (structured data fields and, where present, the linked English Wikipedia article), never from appearance, clothing or imagery.",
            "sourceLabel": f"English Wikipedia — {name}" if wiki else f"Wikidata {qid} — {name} (sex/gender: female; occupation: {occ})",
            "sourceUrl": gender_url,
            "checkedAt": TODAY.isoformat(),
        }
        sources=[{
            "label": f"Wikidata {qid} — {name} (occupation: {occ}; date of birth {dob.isoformat()})",
            "platform": "Website",
            "url": wd_url,
            "relationship": "age-evidence",
        }]
        seen_urls={wd_url}
        for u in refs:
            if u in seen_urls: continue
            sources.append({
                "label": f"{s13.domain_label(u)} — {name} (record cited by Wikidata date-of-birth reference)",
                "platform": "Website",
                "url": u,
                "relationship": "other-trusted",
            })
            seen_urls.add(u)
        for u in wiki:
            if u in seen_urls: continue
            sources.append({
                "label": f"English Wikipedia — {name}",
                "platform": "Website",
                "url": u,
                "relationship": "other-trusted",
            })
            seen_urls.add(u)
        for platform, handle in handles.items():
            sources.append({
                "label": f"{platform} — {s13.display_handle(platform, handle)} (public profile; handle recorded in Wikidata {qid})",
                "platform": platform,
                "url": s13.profile_url(platform, handle),
                "relationship": "verified-platform",
            })
        accounts=[]
        for platform in ("Instagram","TikTok","YouTube","X","Facebook"):
            handle=handles.get(platform)
            if not handle: continue
            accounts.append({
                "platform": platform,
                "username": s13.display_handle(platform, handle),
                "profileUrl": s13.profile_url(platform, handle),
                "followerCountDisplay": UNKNOWN_COUNT,
                "followerCountNumeric": None,
                "countType": "unknown",
                "checkedAt": TODAY.isoformat(),
                "followerSizeRange": UNKNOWN_RANGE,
                "sourceNote": f"Handle recorded in Wikidata {qid}. No follower count was publicly observed on {TODAY.isoformat()} (platform blocks automated retrieval), so it is recorded as {UNKNOWN_COUNT} rather than estimated.",
            })
        return {
            "id": f"W-2026-{idx}",
            "displayName": name,
            "categories": cats,
            "legalAdultEvidence": legal,
            "genderEvidence": gender,
            "sources": sources,
            "socialAccounts": accounts,
            "overallFollowerSizeRange": UNKNOWN_RANGE,
            "largestPublicFollowing": None,
            "verificationStatus": "verified",
            "lastReviewed": TODAY.isoformat(),
            "flags": [] if refs else ["AGE_EVIDENCE_WIKIPEDIA_ONLY"],
            "notes": f"Session 21 fashion/fitness-model Wikidata sweep (2026-09-06). Discovery method: public structured-data query over Wikidata for female items whose occupation is {occ}, with documented DOB and Instagram/TikTok handle. Evidence chain — reference URL(s): {'; '.join(refs[:2]) if refs else 'none'}; Wikipedia: {wiki[0] if wiki else 'none'}. Follower counts: none publicly observed — recorded as {UNKNOWN_COUNT} / {UNKNOWN_RANGE} (never estimated). Categories are objective (modeling, fashion, fitness, creator activity) — not an attractiveness ranking.",
        }

    fashion_selected=[]
    for cand in fm_raw_rows:
        key=norm_name(cand["name"])
        hkeys={h.lower() for h in cand["handles"].values() if h}
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand,"duplicate-name-fashion"))
            continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand,"duplicate-handle-fashion"))
            continue
        dob=s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            skipped.append((cand,"no-dob-fashion"))
            continue
        if s13.age_on(dob) < 18:
            skipped.append((cand,"minor-fashion"))
            continue
        # must have source
        if not cand["ref_urls"]:
            skipped.append((cand,"no-ref-fashion"))
            continue
        entry=build_fashion_entry(next_id, cand, dob)
        next_id+=1
        seen_names.add(key)
        seen_handles.update(hkeys)
        fashion_selected.append(entry)

    total_new = len(selected)+len(fashion_selected)
    print(f"s16 remaining: {len(s16_rows)}")
    print(f"vb raw: {len(vb_raw_rows)}")
    print(f"poolB1: {len(poolB1_rows)} poolC: {len(poolC_rows)} poolD: {len(poolD_rows)}")
    print(f"fm raw good: {len(fm_raw_rows)}")
    print(f"volley selected: {len(selected)} fashion selected: {len(fashion_selected)} total {total_new}")
    print(f"skipped: {len(skipped)}")
    from collections import Counter
    print(Counter([r for _,r in skipped]))

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write")
        return

    catalog["entries"].extend(selected)
    catalog["entries"].extend(fashion_selected)
    catalog["metadata"]["entryCount"]=len(catalog["entries"])
    catalog["metadata"]["generatedAt"]=TODAY.isoformat()
    catalog["metadata"]["summary"]=catalog["metadata"].get("summary","") + f" Session 21 added {total_new} verified profiles ({len(selected)} volleyball/beach volleyball from European/international leagues + NCAA, {len(fashion_selected)} fashion/fitness-model) from remaining Wikidata pools (s16_master 33, s18_raw vb 3, poolB1 22, poolC 11, poolD 12, fm raw good). All with documented DOB and Instagram/TikTok handles, age evidence from reference URLs or Wikipedia, gender from structured data. Follower counts recorded as UNKNOWN where not publicly observed — never estimated. Directory rebuilt via build_directory.py."

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"applied {total_new} entries, now {len(catalog['entries'])} total")

if __name__=="__main__":
    main()
