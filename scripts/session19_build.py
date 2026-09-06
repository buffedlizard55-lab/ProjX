#!/usr/bin/env python3
"""Session 19 — continuation of the fashion / fitness-model Wikidata sweep.

Reads data/research/s19_master.tsv (P106 model / fashion model / personal
trainer / fitness model OFFSET 250–400, plus influencer / Internet-celebrity
rows that carry a P854 reference). Same promotion rules as session 18:

  - English display name from the Wikidata label (never guessed);
  - adult 18+ from the documented P569 date;
  - age evidence: P854 reference URL > English Wikipedia sitelink;
  - Wikipedia-only rows flagged AGE_EVIDENCE_WIKIPEDIA_ONLY;
  - January-1 DOBs flagged DOB_JAN1_POSSIBLE_YEAR_PRECISION;
  - babesdirectory / listal / mypmates / chaturbate refs never used as age evidence
    (those rows were excluded from the master);
  - dedupe on Q-ID, normalized name and every handle (catalog + review queue);
  - IG/TikTok-bearing rows are Published (catalogType social via session15_split);
  - follower counts: none observed → FOLLOWER_COUNT_UNKNOWN.

Usage: python3 scripts/session19_build.py [--apply]
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session13_volleyball as s13  # noqa: E402

ROOT = s13.ROOT
RESEARCH = os.path.join(ROOT, "data", "research")
CATALOG = s13.CATALOG
MASTER = os.path.join(RESEARCH, "s19_master.tsv")
AUDIT = os.path.join(RESEARCH, "s19_selected.tsv")

TODAY = date(2026, 9, 7)
s13.TODAY = TODAY
s13.age_on.__defaults__ = (TODAY,)

UNKNOWN_COUNT = s13.UNKNOWN_COUNT
UNKNOWN_RANGE = s13.UNKNOWN_RANGE
PASS_LABEL = "Session 19 fashion/fitness-model Wikidata continuation (2026-09-07)."

FITNESS_OCC = {"personal trainer", "fitness model", "bodybuilder"}
CREATOR_OCC = {"influencer", "Internet celebrity"}
JAN1_FLAG_QIDS = {
    "Q108599989",  # Amara Shune Lei
    "Q109332203",  # Sujita Basnet
    "Q109672951",  # Gabriella Lomm
    "Q109719791",  # Lavanya Sivaji
    "Q110645778",  # Aymen Saleem
    "Q111016301",  # Jareerat Petsom
    "Q111084288",  # Willow Allen
    "Q111650228",  # Neha Shetty
    "Q111650966",  # Malika El Maslouhi
}
WIKI_TITLE_NAME_QIDS = {
    "Q109322321": "Wikidata English label Cindy Obeñita; English Wikipedia article title Cinderella Obeñita",
    "Q109672951": "Wikidata English label Gabriella Lomm; English Wikipedia article title Gabriella Lomm Mann",
    "Q111600123": "Wikidata English label Anita Chukwumfumnanya Obidi; English Wikipedia article title Korra Obidi",
    "Q112147135": "Wikidata English label Lou-Anne Gleißenebner; English Wikipedia article title Lou-Anne Gleißenebner-Teskey",
    "Q109252450": "Wikidata English label Barbara Yasmin Cabrera; English Wikipedia article title Bárbara Cabrera",
    "Q111906330": "Wikidata English label Mae Mae Renfrow; English Wikipedia article title MaeMae Renfrow",
}

# Conflicting-DOB candidates from this continuation — queued, not guessed.
QUEUE_EXTRA = [
    {
        "qid": "Q108632653",
        "name": "Wioleta Psiuk",
        "ig": "wioleta_daria",
        "tt": "",
        "dob": "1991-07-16 / 1992-07-16 / 1990-01-01",
        "reason": "AGE_CONFLICTING_VALUES",
        "wiki": "",
        "note": "Wikidata P569 carries 16 July 1991, 16 July 1992 and 1 January 1990. Adult either way; the exact date is not chosen.",
    },
]


def load_master():
    rows = []
    with open(MASTER, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("|")
            if len(parts) != 8:
                raise SystemExit(f"bad master row ({len(parts)} cols): {line[:120]}")
            qid, name, dob, ig, tt, occ, ref, wiki = parts
            handles = {}
            if ig:
                handles["Instagram"] = ig
            if tt:
                handles["TikTok"] = tt
            rows.append({
                "qid": qid, "name": name, "dob": dob, "occ": occ,
                "handles": handles, "ref_urls": [ref] if ref else [],
                "wiki_urls": [wiki] if wiki else [],
                "dob_sources": [], "imports": [], "teams": [],
                "country": "UNKNOWN", "group": "fashion",
            })
    return rows


def categories_for(occ):
    if occ in FITNESS_OCC:
        cats = ["Fitness", "Fitness Model", "Creator"]
        if occ == "fitness model":
            cats.append("Modeling")
        return cats
    if occ in CREATOR_OCC:
        return ["Creator", "Lifestyle"]
    return ["Modeling", "Fashion", "Creator"]


def host_of(url):
    try:
        return urlparse(url).netloc.replace("www.", "").lower()
    except Exception:
        return ""


def relationship_for(url):
    host = host_of(url)
    if host.endswith("wikipedia.org"):
        return "other-trusted"
    if host in ("famousbirthdays.com", "programme-tv.net", "voici.fr", "elpopular.pe",
                "ascii.jp", "oricon.co.jp", "scmp.com", "rediff.com", "bolnews.com",
                "g1.globo.com", "telegrafi.com", "kimnereli.net", "csfd.cz",
                "themoviedb.org", "omfmedia.com", "girlfriend.com.au", "dicionariompb.com.br",
                "metropolitanafm.com.br", "natelinha.uol.com.br", "jagranjosh.com",
                "gistreel.com", "lepoint.fr", "larepublica.pe", "tvsa.co.za",
                "caras.uol.com.br", "mynet.com", "formulatv.com", "celebrityageinfo.com",
                "girlsnews.tv", "thefocus.news", "wearemitu.com", "fdb.cz",
                "adorocinema.com"):
        return "press"
    if host in ("kdash.jp", "just-pro.jp", "amuse.co.jp", "platinumproduction.jp",
                "trustar.co.jp", "niziu.com", "rbcasting.com", "jkt48.com",
                "miss-id.jp", "ena-group.jp", "horipro.co.jp", "avex-management.jp",
                "nogizaka46.com", "missczechrep.cz"):
        return "agency"
    if host.endswith(".com") and host.count(".") == 1 and any(
            tok in host for tok in ("matsushita-nao", "higamanami")):
        return "official"
    if "matsushita-nao.com" in host or "higamanami.com" in host:
        return "official"
    return "other-trusted"


def build_fashion_entry(idx, cand, dob):
    qid = cand["qid"]
    name = cand["name"]
    wd_url = f"https://www.wikidata.org/wiki/{qid}"
    handles = {p: h for p, h in cand["handles"].items() if h}
    refs = cand["ref_urls"]
    wiki = cand["wiki_urls"]
    age = s13.age_on(dob)
    occ = cand["occ"]
    cats = categories_for(occ)

    if refs:
        age_url = refs[0]
        age_label = f"{s13.domain_label(refs[0])} — {name} (record cited by the Wikidata date-of-birth reference)"
        prov_text = f"the reference URL recorded against that statement is {refs[0]}"
    elif wiki:
        age_url = wiki[0]
        age_label = f"English Wikipedia — {name} (article linked to Wikidata {qid})"
        prov_text = "the structured record names no source and no reference URL for that statement"
    else:
        raise SystemExit(f"{qid} has neither ref nor wiki — should not have been selected")

    extra = ""
    if wiki:
        extra += f" An English Wikipedia article covers this person ({wiki[0]})."
    if len(refs) > 1:
        extra += f" Further reference URLs recorded against the same item: {'; '.join(refs[1:3])}."

    legal = {
        "summary": (
            f"Born {s13.human_date(dob)} ({dob.isoformat()}) — age {age} as of {TODAY.isoformat()}, "
            f"so an adult (18+). The birth date is the value recorded in the Wikidata structured item "
            f"{qid} ({wd_url}): {prov_text}.{extra} Adult status is taken only from this documented "
            f"birth date — never inferred from appearance, clothing, photographs, college attendance "
            f"or any image-based judgement."
        ),
        "sourceLabel": age_label,
        "sourceUrl": age_url,
        "checkedAt": TODAY.isoformat(),
    }

    gender_url = wiki[0] if wiki else (refs[0] if refs else wd_url)
    gender = {
        "summary": (
            f"Woman — the Wikidata structured item {qid} records sex/gender: female; occupation "
            f"recorded as {occ}. Gender is established from documentary records (structured data "
            f"fields and, where present, the linked English Wikipedia article), never from "
            f"appearance, clothing or imagery."
        ),
        "sourceLabel": (
            f"English Wikipedia — {name}" if wiki else
            f"Wikidata {qid} — {name} (sex/gender: female; occupation: {occ})"
        ),
        "sourceUrl": gender_url,
        "checkedAt": TODAY.isoformat(),
    }

    sources = [{
        "label": (
            f"Wikidata {qid} — {name} (occupation: {occ}; date of birth {dob.isoformat()})"
        ),
        "platform": "Website",
        "url": wd_url,
        "relationship": "age-evidence",
    }]
    seen_urls = {wd_url}
    for u in refs:
        if u in seen_urls:
            continue
        sources.append({
            "label": f"{s13.domain_label(u)} — {name} (record cited by the Wikidata date-of-birth reference)",
            "platform": "Website",
            "url": u,
            "relationship": relationship_for(u),
        })
        seen_urls.add(u)
    for u in wiki:
        if u in seen_urls:
            continue
        sources.append({
            "label": f"English Wikipedia — {name}",
            "platform": "Website",
            "url": u,
            "relationship": "other-trusted",
        })
        seen_urls.add(u)
    for platform, handle in handles.items():
        sources.append({
            "label": (
                f"{platform} — {s13.display_handle(platform, handle)} "
                f"(public profile; handle recorded in Wikidata {qid})"
            ),
            "platform": platform,
            "url": s13.profile_url(platform, handle),
            "relationship": "verified-platform",
        })

    accounts = []
    for platform in ("Instagram", "TikTok", "YouTube", "X", "Facebook"):
        handle = handles.get(platform)
        if not handle:
            continue
        accounts.append({
            "platform": platform,
            "username": s13.display_handle(platform, handle),
            "profileUrl": s13.profile_url(platform, handle),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "countType": "unknown",
            "checkedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
            "sourceNote": (
                f"Handle recorded in Wikidata {qid}. No follower count was publicly observed on "
                f"{TODAY.isoformat()} (the platform blocks automated retrieval of the profile page), "
                f"so it is recorded as {UNKNOWN_COUNT} rather than estimated."
            ),
        })

    flags = []
    if not refs and wiki:
        flags.append("AGE_EVIDENCE_WIKIPEDIA_ONLY")
    if qid in JAN1_FLAG_QIDS:
        flags.append("DOB_JAN1_POSSIBLE_YEAR_PRECISION")
    if qid in WIKI_TITLE_NAME_QIDS:
        flags.append("NAME_ALIAS_IN_WIKIPEDIA")

    notes = [
        PASS_LABEL,
        "Discovery method: public structured-data query over Wikidata for female items whose occupation "
        "is model, fashion model, personal trainer, bodybuilder or fitness model, with a documented "
        "date of birth and at least one Instagram or TikTok handle "
        "(queries archived under data/research/urls/s18_prom_off*.url).",
        f"Occupation recorded in the structured item: {occ}.",
        "Evidence chain — "
        + (f"reference URL(s): {'; '.join(refs[:3])}" if refs else "no P854 reference URL")
        + (f"; English Wikipedia: {wiki[0]}" if wiki else "")
        + ".",
        f"Follower counts: none publicly observed for the listed account(s) — recorded as {UNKNOWN_COUNT} / "
        f"{UNKNOWN_RANGE} (never estimated, never summed across platforms).",
        "Categories are objective (modeling, fashion, fitness, creator activity) — this directory is not an "
        "attractiveness ranking.",
    ]
    if qid in WIKI_TITLE_NAME_QIDS:
        notes.append(WIKI_TITLE_NAME_QIDS[qid] + ".")
    if flags:
        notes.append("Flags: " + ", ".join(flags) + ".")

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
        "flags": flags,
        "notes": " ".join(notes),
    }


def cited_qids():
    have = set()
    for path in (CATALOG, os.path.join(ROOT, "data", "catalog-reference.json")):
        if os.path.exists(path):
            have.update(re.findall(r"Q\d+", open(path, encoding="utf-8").read()))
    return have


def main():
    apply_changes = "--apply" in sys.argv
    catalog = json.load(open(CATALOG, encoding="utf-8"))

    have_qids = cited_qids()
    existing_names = {s13.norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    rq_names = {s13.norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}
    existing_handles = set()
    for e in catalog["entries"]:
        for a in e.get("socialAccounts", []):
            existing_handles.add((a.get("username") or "").lstrip("@").lower())
    for r in catalog.get("reviewQueue", []):
        h = r.get("handle") or ""
        if h:
            existing_handles.add(h.lstrip("@").lower())

    rows = load_master()
    selected, queued, skipped = [], [], []
    next_id = max(int(e["id"].split("-")[-1]) for e in catalog["entries"]) + 1
    seen_names, seen_handles = set(), set()

    for cand in rows:
        key = s13.norm_name(cand["name"])
        hkeys = {h.lower() for h in cand["handles"].values() if h}
        if cand["qid"] in have_qids:
            skipped.append((cand, "duplicate-qid")); continue
        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name")); continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand, "duplicate-handle")); continue
        if not cand["handles"]:
            skipped.append((cand, "no-public-handle")); continue
        if re.fullmatch(r"Q\d+", cand["name"]) or not cand["name"]:
            skipped.append((cand, "no-display-name")); continue
        dob = s13.parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            queued.append((cand, "AGE_UNVERIFIED")); continue
        if s13.age_on(dob) < 18:
            queued.append((cand, "AGE_OUT_OF_RANGE_OR_MINOR")); continue
        if not (cand["ref_urls"] or cand["wiki_urls"]):
            queued.append((cand, "AGE_SOURCE_NOT_RECORDED")); continue

        entry = build_fashion_entry(next_id, cand, dob)
        selected.append((cand, dob, entry))
        seen_names.add(key)
        seen_handles |= hkeys
        have_qids.add(cand["qid"])
        next_id += 1

    rq = catalog.get("reviewQueue", [])
    rq_num = max((int(r["id"].split("-")[-1]) for r in rq
                  if isinstance(r, dict) and r.get("id") and re.fullmatch(r"R-\d{4}-\d+", r["id"])),
                 default=0) + 1

    REASON_TEXT = {
        "AGE_UNVERIFIED": "the structured item carries no date of birth.",
        "AGE_OUT_OF_RANGE_OR_MINOR": "the recorded date of birth is outside the adult 18+ scope.",
        "AGE_SOURCE_NOT_RECORDED": "a date of birth is recorded but no reference URL or English Wikipedia article is attached.",
        "AGE_CONFLICTING_VALUES": "two different dates of birth are recorded in the structured item; neither is chosen.",
        "NAME_MISMATCH_IN_CITED_SOURCE": "the cited English Wikipedia article title does not match the Wikidata English label.",
        "AGE_SOURCE_IDENTITY_UNRESOLVED": "the cited English Wikipedia sitelink does not identify this person or state her birth date.",
    }

    def append_queue(cand, reason, extra_note=""):
        nonlocal rq_num
        handles = {p: h for p, h in cand["handles"].items() if h}
        platform = "Instagram" if "Instagram" in handles else (sorted(handles)[0] if handles else "Instagram")
        handle = handles.get(platform, "")
        rq.append({
            "id": f"R-2026-{rq_num:03d}",
            "displayName": cand["name"],
            "handle": s13.display_handle(platform, handle) if handle else "",
            "platform": platform,
            "profileUrl": s13.profile_url(platform, handle) if handle else "",
            "discoveryCategory": "fashion/fitness model (P106)",
            "evidenceFound": {
                "summary": (
                    f"Wikidata item {cand['qid']} records a female {cand.get('occ', 'model')} "
                    f"with date of birth recorded as {cand.get('dob') or 'none'}."
                ),
                "sourceLabel": f"Wikidata {cand['qid']} — {cand['name']}",
                "sourceUrl": cand["wiki_urls"][0] if cand.get("wiki_urls") else f"https://www.wikidata.org/wiki/{cand['qid']}",
            },
            "missingEvidence": [reason],
            "flags": [reason],
            "lastChecked": TODAY.isoformat(),
            "notes": (
                f"{PASS_LABEL} Not promoted: {REASON_TEXT[reason]} "
                f"Candidate Q-ID {cand['qid']}. {extra_note}"
            ).strip(),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    for cand, reason in queued:
        append_queue(cand, reason)

    queued_extra_n = 0
    for item in QUEUE_EXTRA:
        key = s13.norm_name(item["name"])
        hkeys = {h.lower() for h in (item["ig"], item["tt"]) if h}
        if item["qid"] in have_qids or key in existing_names or key in rq_names or key in seen_names:
            continue
        if hkeys & (existing_handles | seen_handles):
            continue
        cand = {
            "qid": item["qid"], "name": item["name"], "dob": item["dob"],
            "occ": "model",
            "handles": {k: v for k, v in (("Instagram", item["ig"]), ("TikTok", item["tt"])) if v},
            "wiki_urls": [item["wiki"]] if item["wiki"] else [],
        }
        append_queue(cand, item["reason"], item["note"])
        queued_extra_n += 1
        seen_names.add(key)
        seen_handles |= hkeys

    with open(AUDIT, "w", encoding="utf-8") as fh:
        fh.write(f"# {PASS_LABEL} selection audit (generated {TODAY.isoformat()}).\n")
        fh.write("# entryId\tqid\tname\tdob\tage\tocc\thandles\treferenceUrls\twiki\tflags\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["name"], dob.isoformat(),
                str(s13.age_on(dob)), cand["occ"], handles,
                ";".join(cand["ref_urls"]) or "-", ";".join(cand["wiki_urls"]) or "-",
                ",".join(entry["flags"]) or "-",
            ]) + "\n")

    print(f"master rows           : {len(rows)}")
    print(f"promoted to entries   : {len(selected)}")
    print(f"    IG/TikTok-bearing : {sum(1 for c, _, _ in selected if {'Instagram', 'TikTok'} & set(c['handles']))}")
    print(f"sent to review queue  : {len(queued) + queued_extra_n} (master {len(queued)} + extra {queued_extra_n})")
    print(f"skipped               : {len(skipped)}")
    sc = {}
    for _, r in skipped:
        sc[r] = sc.get(r, 0) + 1
    for r, n in sorted(sc.items()):
        print(f"    {r}: {n}")
    if selected:
        print(f"entry range           : {selected[0][2]['id']} .. {selected[-1][2]['id']}")
    print(f"audit artifact        : {os.path.relpath(AUDIT, ROOT)}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return 0

    catalog["entries"].extend(e for _, _, e in selected)
    catalog["reviewQueue"] = rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(rq)
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 19 continued the fashion/fitness-model Wikidata P106 sweep at OFFSET 250–400 "
        f"and added a small influencer/Internet-celebrity P854 slice, promoting {len(selected)} "
        f"verified Instagram/TikTok profiles (female; documented DOB 1985–2008; pornographic-film "
        f"and erotic-photography occupations excluded). {len(queued) + queued_extra_n} candidates "
        f"were routed to the review queue rather than guessed. Follower counts that could not be "
        f"publicly observed are recorded as {UNKNOWN_COUNT} with range {UNKNOWN_RANGE} — never "
        f"estimated and never summed across platforms."
    )

    irr = {
        "id": "IRR-2026-09-07-024",
        "detectedAt": TODAY.isoformat(),
        "severity": "info",
        "title": "Session 19 fashion/fitness continuation: minors, host filters and DOB conflict",
        "details": (
            "Continuation of the Session 18 P106 sweep (OFFSET 250–400) plus influencer/"
            "Internet-celebrity items that carry a P854 reference. Filters: (1) babesdirectory.online, "
            "listal.com, mypmates.club, pornhub.com and playboy magazine citations were never used as "
            "age evidence; (2) Havan Flores (Q108348506, DOB 2007-11-20) and Akari Toyofuku "
            "(Q111757543, DOB 2008-12-14) are under 18 as of 2026-09-07 and were not added; "
            "(3) Wioleta Psiuk (Q108632653) carries three different P569 values and was queued "
            "AGE_CONFLICTING_VALUES rather than resolved by guesswork; (4) the fm_off120 Playboy-"
            "adjacent pool without English Wikipedia was not auto-promoted; (5) volleyball 2003–08 "
            "Instagram/TikTok remains exhausted from prior sessions. January-1 DOBs that were "
            "promoted carry DOB_JAN1_POSSIBLE_YEAR_PRECISION. No follower counts were publicly observed."
        ),
        "resolution": (
            f"{len(selected)} entries promoted with cited age and gender evidence; Wioleta Psiuk "
            "queued; audit in data/research/s19_selected.tsv; queries in "
            "data/research/urls/s18_prom_off{{250,300,350,400}}.url and s18_inf_off0.url."
        ),
    }
    catalog.setdefault("irregularities", []).append(irr)

    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, {len(rq)} review, "
          f"{len(catalog['irregularities'])} irregularities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
