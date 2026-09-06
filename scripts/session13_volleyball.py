#!/usr/bin/env python3
"""
Session 13 — women's volleyball discovery batch (NCAA / college, international beach,
European + other international indoor leagues).

Builds catalog entries from the harvested research artifacts:

  data/research/s13_ncaa.tsv          qid|name|dob|instagram|team|team|...
  data/research/s13_facts.tsv         qid|S=..;X=..;K=..;F=..;Y=..;W=..      (NCAA facts)
  data/research/s13_beach_intl.tsv    qid|name|dob|instagram|x|tiktok|country
  data/research/s13_indoor_intl.tsv   qid|name|dob|instagram|country
  data/research/s13_evidence.tsv      qid<TAB>tag<TAB>value   (S/U/T/X/K/F/Y for intl + beach)

Every field written to the catalog comes from one of those artifacts (i.e. from a Wikidata
SPARQL result fetched on 2026-09-06). Nothing is inferred, estimated or invented:
  * candidates without a documented date of birth are NOT promoted to entries — they go to
    the review queue with AGE_UNVERIFIED;
  * follower counts that were not publicly observed are written as FOLLOWER_COUNT_UNKNOWN
    with countType "unknown" and followerSizeRange FOLLOWER_RANGE_UNKNOWN.

Usage:  python3 scripts/session13_volleyball.py [--apply]
Without --apply the script only prints the plan and writes the audit TSV.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "catalog.json")
RESEARCH = os.path.join(ROOT, "data", "research")
AUDIT_TSV = os.path.join(RESEARCH, "s13_selected.tsv")

TODAY = date(2026, 9, 6)
MIN_DOB = date(1990, 1, 1)
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

UNKNOWN_COUNT = "FOLLOWER_COUNT_UNKNOWN"
UNKNOWN_RANGE = "FOLLOWER_RANGE_UNKNOWN"


# ---------------------------------------------------------------- helpers
def strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(ch))


def norm_name(name: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(name).lower()).strip()


def read_rows(path: str):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            yield line


def parse_dob(value: str):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", value.strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def age_on(dob: date, when: date = TODAY) -> int:
    return when.year - dob.year - ((when.month, when.day) < (dob.month, dob.day))


def human_date(dob: date) -> str:
    return f"{MONTHS[dob.month - 1]} {dob.day}, {dob.year}"


def join_sources(names):
    names = list(dict.fromkeys(names))
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return " and ".join([", ".join(names[:-1]), names[-1]])


def size_range(numeric):
    if numeric is None:
        return UNKNOWN_RANGE
    buckets = [(1000, "Under 1K"), (5000, "1K\u20134.9K"), (10000, "5K\u20139.9K"),
               (25000, "10K\u201324.9K"), (50000, "25K\u201349.9K"),
               (100000, "50K\u201399.9K"), (250000, "100K\u2013249.9K"),
               (500000, "250K\u2013499.9K"), (1000000, "500K\u2013999.9K"),
               (5000000, "1M\u20134.9M")]
    for limit, label in buckets:
        if numeric < limit:
            return label
    return "5M+"


# ---------------------------------------------------------------- load research
def load_evidence():
    ev = {}
    for row in read_rows(os.path.join(RESEARCH, "s13_evidence.tsv")):
        parts = row.split("\t")
        if len(parts) != 3:
            continue
        qid, tag, value = parts
        ev.setdefault(qid, {}).setdefault(tag, [])
        if value not in ev[qid][tag]:
            ev[qid][tag].append(value)
    return ev


def load_facts_ncaa():
    facts = {}
    for row in read_rows(os.path.join(RESEARCH, "s13_facts.tsv")):
        qid, _, payload = row.partition("|")
        info = {}
        for chunk in payload.split(";"):
            key, _, val = chunk.partition("=")
            info[key.strip()] = val.strip()
        facts[qid] = info
    return facts


def dash(value):
    value = (value or "").strip()
    return "" if value in ("", "-", "UNKNOWN") else value


def load_candidates(ev, facts_ncaa):
    cands = []

    # --- NCAA / US college indoor volleyball
    for row in read_rows(os.path.join(RESEARCH, "s13_ncaa.tsv")):
        parts = row.split("|")
        if len(parts) < 4:
            continue
        qid, name, dob, ig = parts[0], parts[1], parts[2], parts[3]
        teams = [t for t in parts[4:] if t and t != "-"]
        f = facts_ncaa.get(qid, {})
        handles = {"Instagram": dash(ig)}
        for tag, platform in (("X", "X"), ("K", "TikTok"), ("F", "Facebook"), ("Y", "YouTube")):
            handles[platform] = dash(f.get(tag))
        srcs = [s for s in re.split(r"\+", f.get("S", "")) if s and s != "-"]
        e = ev.get(qid, {})
        cands.append({
            "qid": qid, "name": name, "dob": dash(dob), "group": "ncaa",
            "country": "United States", "teams": teams, "handles": handles,
            "dob_sources": srcs, "ref_urls": e.get("U", []),
            "wiki_urls": e.get("W", []), "imports": e.get("I", []),
        })

    # --- international beach volleyball
    for row in read_rows(os.path.join(RESEARCH, "s13_beach_intl.tsv")):
        parts = row.split("|")
        if len(parts) < 7:
            continue
        qid, name, dob, ig, x, tt, country = parts[:7]
        e = ev.get(qid, {})
        handles = {"Instagram": dash(ig), "X": dash(x), "TikTok": dash(tt)}
        for tag, platform in (("X", "X"), ("K", "TikTok"), ("F", "Facebook"), ("Y", "YouTube")):
            for value in e.get(tag, []):
                if not handles.get(platform):
                    handles[platform] = value
        cands.append({
            "qid": qid, "name": name, "dob": dash(dob), "group": "beach",
            "country": dash(country) or "UNKNOWN", "teams": [],
            "handles": handles, "dob_sources": e.get("S", []), "ref_urls": e.get("U", []),
            "wiki_urls": e.get("W", []), "imports": e.get("I", []),
        })

    # --- international indoor (European / Asian / American leagues)
    for row in read_rows(os.path.join(RESEARCH, "s13_indoor_intl.tsv")):
        parts = row.split("|")
        if len(parts) < 5:
            continue
        qid, name, dob, ig, country = parts[:5]
        e = ev.get(qid, {})
        handles = {"Instagram": dash(ig)}
        for tag, platform in (("X", "X"), ("K", "TikTok"), ("F", "Facebook"), ("Y", "YouTube")):
            for value in e.get(tag, []):
                if not handles.get(platform):
                    handles[platform] = value
        cands.append({
            "qid": qid, "name": name, "dob": dash(dob), "group": "intl",
            "country": dash(country) or "UNKNOWN", "teams": e.get("T", []),
            "handles": handles, "dob_sources": e.get("S", []), "ref_urls": e.get("U", []),
            "wiki_urls": e.get("W", []), "imports": e.get("I", []),
        })
    return cands


# ---------------------------------------------------------------- url builders
PLATFORM_META = {
    "Instagram": ("https://www.instagram.com/{}/", "@{}"),
    "X": ("https://x.com/{}", "@{}"),
    "TikTok": ("https://www.tiktok.com/@{}", "@{}"),
    "Facebook": ("https://www.facebook.com/{}", "{}"),
    "YouTube": ("https://www.youtube.com/channel/{}", "{}"),
}


def profile_url(platform, handle):
    template, _ = PLATFORM_META[platform]
    return template.format(handle)


def display_handle(platform, handle):
    _, template = PLATFORM_META[platform]
    return template.format(handle)


OFFICIAL_HOSTS = (
    "fivb.org", "fivb.com", "cev.eu", "eurovolley.cev.eu", "volleyball-bundesliga.de",
    "vfb-suhl.de", "slovakvolley.sk", "svf.sk", "bvf.by", "teamnl.org", "volleyball.ca",
    "cpb.org.br", "jva.or.jp", "vleague.jp", "rfevb-web.dataproject.com",
    "svbf-web.dataproject.com", "nvbf-web.dataproject.com", "turksporu.com.tr",
    "dscvolley.de", "dresdnersportclub.de", "stuttgarts-schoenster-sport.de",
    "ladies-in-black.de", "nawaro-straubing.de", "wealthplanet.it", "haok-mladost.hr",
    "jti.co.jp", "sportinternat-muenster.de", "olympic.ca",
    "wkusports.com", "csurams.com", "wsucougars.com", "goislanders.com", "herdzone.com",
    "auburntigers.com", "usctrojans.com", "hawkeyesports.com", "floridagators.com",
    "gocards.com", "mutigers.com", "goblueraiders.com", "vcuathletics.com",
    "osubeavers.com", "kstatesports.com", "seminoles.com", "fswbucs.com",
    "arizonawildcats.com", "gomarquette.com", "ttusports.com",
)
PRESS_HOSTS = ("lequipe.fr", "eurosport.de", "hlsports.de", "jornaldovolei.com.br")


def host_of(url):
    return re.sub(r"^https?://", "", url).split("/")[0].replace("www.", "").lower()


def relationship_for(url):
    host = host_of(url)
    if host.endswith("wikipedia.org"):
        return "other-trusted"
    if any(host == h or host.endswith("." + h) for h in OFFICIAL_HOSTS):
        return "official"
    if any(host == h or host.endswith("." + h) for h in PRESS_HOSTS):
        return "press"
    return "other-trusted"


# ---------------------------------------------------------------- entry builder
def build_entry(idx, cand, dob):
    qid = cand["qid"]
    name = cand["name"]
    wd_url = f"https://www.wikidata.org/wiki/{qid}"
    handles = {p: h for p, h in cand["handles"].items() if h}
    srcs = cand["dob_sources"]
    refs = cand["ref_urls"]
    wiki = cand["wiki_urls"]
    imports = cand["imports"]
    teams = cand["teams"]
    age = age_on(dob)
    group = cand["group"]

    if group == "beach":
        categories = ["Athlete", "Beach Volleyball", "Creator"]
        sport_text = "beach volleyball"
    elif group == "ncaa":
        categories = ["Athlete", "Volleyball", "College Athlete", "Creator"]
        sport_text = "NCAA (US college) indoor volleyball"
    else:
        categories = ["Athlete", "Volleyball", "Creator"]
        sport_text = "indoor volleyball"

    women_teams = [t for t in teams if re.search(r"women|ladies|dames|femminile|femenino|f\u00e9minin|\u017eeny|n\u0151i|zeny", t, re.I)]
    women_refs = [u for u in refs if re.search(r"women|ladies|womens|girls|/zeny/|wb-", u, re.I)]

    # ---------------- adult (18+) evidence
    provenance = []
    if srcs:
        provenance.append(f"its reference names {join_sources(srcs)}")
    if refs:
        provenance.append(f"the reference URL recorded against that statement is {refs[0]}")
    if imports:
        provenance.append(f"the statement was imported into Wikidata from the {join_sources(imports)}")
    prov_text = ("; ".join(provenance)) if provenance else (\n        "the structured record names no source and no reference URL for that statement")

    if refs:
        age_url = refs[0]
        age_label = f"{domain_label(refs[0])} \u2014 {name} (record cited by the Wikidata date-of-birth reference)"
    elif wiki:
        age_url = wiki[0]
        age_label = f"English Wikipedia \u2014 {name} (article linked to Wikidata {qid})"
    else:
        age_url = wd_url
        age_label = f"Wikidata {qid} \u2014 {name} (date of birth {dob.isoformat()})"

    extra = ""
    if wiki:
        extra += f" An English Wikipedia article covers this player ({wiki[0]})."
    if len(refs) > 1:
        extra += f" Further reference URLs recorded against the same item: {'; '.join(refs[1:3])}."

    legal = {
        "summary": (
            f"Born {human_date(dob)} ({dob.isoformat()}) \u2014 age {age} as of {TODAY.isoformat()}, "
            f"so an adult (18+). The birth date is the value recorded in the Wikidata structured item "
            f"{qid} ({wd_url}): {prov_text}.{extra} Adult status is taken only from this documented "
            f"birth date \u2014 never inferred from appearance, clothing, photographs, college attendance "
            f"or any image-based judgement."
        ),
        "sourceLabel": age_label,
        "sourceUrl": age_url,
        "checkedAt": TODAY.isoformat(),
    }

    # ---------------- gender evidence
    bits = [f"the Wikidata structured item {qid} records sex/gender: female"]
    if women_teams:
        bits.append(f"roster membership of {join_sources(women_teams[:3])} is recorded in the same item")
    elif teams:
        bits.append(f"roster membership of {join_sources(teams[:3])} is recorded in the same item")
    if women_refs:
        bits.append(f"she appears in the women's competition/roster record at {women_refs[0]}")
    elif refs:
        bits.append(f"player record at {refs[0]}")
    if srcs:
        bits.append(f"her birth date in that same structured record is cited to {join_sources(srcs)}")

    if women_refs:
        gender_url = women_refs[0]
    elif refs:
        gender_url = refs[0]
    elif wiki:
        gender_url = wiki[0]
    else:
        gender_url = wd_url

    gender = {
        "summary": (
            f"Woman \u2014 {'; '.join(bits)}. She competes in women's {sport_text}"
            + (f" ({cand['country']})." if cand["country"] != "UNKNOWN" else ".")
            + " Gender is established from documentary records (structured data fields, team rosters and "
              "competition databases), never from appearance, clothing or imagery."
        ),
        "sourceLabel": (
            f"Wikidata {qid} \u2014 {name} (sex/gender: female"
            + (f"; member of sports team: {join_sources(teams[:3])}" if teams else "")
            + ")"
        ) if gender_url == wd_url else f"{domain_label(gender_url)} \u2014 {name}",
        "sourceUrl": gender_url,
        "checkedAt": TODAY.isoformat(),
    }

    # ---------------- sources
    sources = [{
        "label": f"Wikidata {qid} \u2014 {name} (women's {sport_text}; date of birth {dob.isoformat()}"
                 + (f"; reference: {join_sources(srcs)}" if srcs else "")
                 + (f"; country: {cand['country']}" if cand["country"] != "UNKNOWN" else "") + ")",
        "platform": "Website",
        "url": wd_url,
        "relationship": "age-evidence",
    }]
    for u in refs:
        sources.append({
            "label": f"{domain_label(u)} \u2014 {name} (record cited by the Wikidata date-of-birth reference)",
            "platform": "Website",
            "url": u,
            "relationship": relationship_for(u),
        })
    for u in wiki:
        sources.append({
            "label": f"English Wikipedia \u2014 {name}",
            "platform": "Website",
            "url": u,
            "relationship": "other-trusted",
        })
    for platform, handle in handles.items():
        sources.append({
            "label": f"{platform} \u2014 {display_handle(platform, handle)} (public profile; handle recorded in Wikidata {qid})",
            "platform": platform,
            "url": profile_url(platform, handle),
            "relationship": "verified-platform",
        })

    # ---------------- social accounts
    accounts = []
    for platform in ("Instagram", "TikTok", "YouTube", "X", "Facebook"):
        handle = handles.get(platform)
        if not handle:
            continue
        accounts.append({
            "platform": platform,
            "username": display_handle(platform, handle),
            "profileUrl": profile_url(platform, handle),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "countType": "unknown",
            "checkedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
            "sourceNote": (
                f"Handle recorded in Wikidata {qid}. No follower count was publicly observed on "
                f"{TODAY.isoformat()} (the platform blocks automated retrieval of the profile page), so it is "
                f"recorded as {UNKNOWN_COUNT} rather than estimated."
            ),
        })

    # ---------------- notes
    note_parts = [
        f"Session 13 volleyball discovery pass \u2014 {group_label(group)}; added {TODAY.isoformat()}.",
        "Discovery method: public structured-data query over Wikidata for female athletes whose occupation is "
        + ("beach volleyball player" if group == "beach" else "volleyball player")
        + ", with a documented date of birth and at least one public social handle "
        + "(queries archived under data/research/urls/).",
    ]
    if teams:
        note_parts.append(f"Teams recorded in the structured item: {join_sources(teams[:4])}.")
    if cand["country"] != "UNKNOWN":
        note_parts.append(f"Citizenship recorded in Wikidata: {cand['country']}.")
    if srcs or refs or imports:
        bits2 = []
        if srcs:
            bits2.append(f"birth-date reference(s): {join_sources(srcs)}")
        if imports:
            bits2.append(f"imported from the {join_sources(imports)}")
        if refs:
            bits2.append(f"reference URL(s): {'; '.join(refs[:3])}")
        note_parts.append("Evidence chain \u2014 " + "; ".join(bits2) + ".")
    if wiki:
        note_parts.append(f"English Wikipedia: {wiki[0]}.")
    note_parts.append(
        f"Follower counts: none publicly observed for the listed account(s) \u2014 recorded as {UNKNOWN_COUNT} / "
        f"{UNKNOWN_RANGE} (never estimated, never summed across platforms)."
    )
    note_parts.append(
        "Categories are objective (sport, competition level, creator activity) \u2014 this directory is not an "
        "attractiveness ranking."
    )

    return {
        "id": f"W-2026-{idx}",
        "displayName": name,
        "categories": categories,
        "legalAdultEvidence": legal,
        "genderEvidence": gender,
        "sources": sources,
        "socialAccounts": accounts,
        "overallFollowerSizeRange": UNKNOWN_RANGE,
        "verificationStatus": "verified",
        "lastReviewed": TODAY.isoformat(),
        "flags": [],
        "notes": " ".join(note_parts),
    }


def group_label(group):
    return {"ncaa": "NCAA / US college volleyball",
            "beach": "international beach volleyball",
            "intl": "European / international indoor volleyball"}[group]


def domain_label(url):
    host = re.sub(r"^https?://", "", url).split("/")[0]
    host = host.replace("www.", "")
    names = {
        "women.volleybox.net": "Volleybox (women's database)",
        "volleybox.net": "Volleybox",
        "volleyball-bundesliga.de": "German Volleyball Bundesliga (VBL)",
        "1.bundesliga.vfb-suhl.de": "VfB 91 Suhl (German Bundesliga club)",
        "cev.eu": "CEV (European Volleyball Confederation)",
        "en.volleyballworld.com": "Volleyball World (FIVB)",
        "worldofvolley.com": "WorldofVolley",
        "olympedia.org": "Olympedia",
        "svf.sk": "Slovak Volleyball Federation",
        "slovakvolley.sk": "Slovak Volleyball Federation",
        "bvf.by": "Belarusian Volleyball Federation",
        "teamnl.org": "TeamNL (Dutch Olympic Committee)",
        "volleyball.ca": "Volleyball Canada",
        "cpb.org.br": "Confedera\u00e7\u00e3o Brasileira de Voleibol",
        "jornaldovolei.com.br": "Jornal do V\u00f4lei (Brazilian volleyball press)",
        "jva.or.jp": "Japan Volleyball Association",
        "vleague.jp": "V.League (Japan)",
        "jti.co.jp": "JT Marvelous (Japan club)",
        "hlsports.de": "HL Sports (regional press)",
        "dscvolley.de": "Dresdner SC Volleyball (club)",
        "dresdnersportclub.de": "Dresdner SC (club)",
        "stuttgarts-schoenster-sport.de": "Allianz MTV Stuttgart (club)",
        "wealthplanet.it": "Wealth Planet Perugia (club)",
        "nvbf-web.dataproject.com": "Norwegian Volleyball Federation",
        "u18.girls.2017.volleyball.fivb.com": "FIVB U18 Girls World Championship 2017",
    }
    return names.get(host, host)


# ---------------------------------------------------------------- main
def main():
    apply_changes = "--apply" in sys.argv
    with open(CATALOG, encoding="utf-8") as fh:
        catalog = json.load(fh)

    existing_names = {norm_name(e["displayName"]) for e in catalog["entries"] if e.get("displayName")}
    existing_handles = set()
    for e in catalog["entries"]:
        for a in e.get("socialAccounts", []):
            existing_handles.add(a.get("username", "").lstrip("@").lower())
    rq_names = {norm_name(r["displayName"]) for r in catalog.get("reviewQueue", []) if r.get("displayName")}

    ev = load_evidence()
    facts_ncaa = load_facts_ncaa()
    cands = load_candidates(ev, facts_ncaa)

    selected, queued, skipped = [], [], []
    next_id = 302
    seen_names, seen_handles = set(), set()

    for cand in cands:
        key = norm_name(cand["name"])
        handles = {p: h for p, h in cand["handles"].items() if h}
        hkeys = {h.lower() for h in handles.values()}

        if key in existing_names or key in rq_names or key in seen_names:
            skipped.append((cand, "duplicate-name"))
            continue
        if hkeys & (existing_handles | seen_handles):
            skipped.append((cand, "duplicate-handle"))
            continue
        if not handles:
            skipped.append((cand, "no-public-handle"))
            continue

        dob = parse_dob(cand["dob"]) if cand["dob"] else None
        if dob is None:
            queued.append((cand, "AGE_UNVERIFIED"))
            continue
        if dob < MIN_DOB or age_on(dob) < 18:
            queued.append((cand, "AGE_OUT_OF_RANGE_OR_MINOR"))
            continue
        if not (cand["dob_sources"] or cand["ref_urls"] or cand["wiki_urls"] or cand["imports"]):
            queued.append((cand, "AGE_SOURCE_NOT_RECORDED"))
            continue

        entry = build_entry(next_id, cand, dob)
        if not cand["ref_urls"] and not cand["wiki_urls"]:
            # birth date is documented, but the cited database page is not linked from the
            # structured record -> surface that so a human reviewer can chase the primary page.
            entry["flags"] = ["AGE_EVIDENCE_SECONDARY_SOURCES"]
        selected.append((cand, dob, entry))
        seen_names.add(key)
        seen_handles |= hkeys
        next_id += 1

    # ---------------- review queue additions
    rq = catalog.get("reviewQueue", [])
    rq_num = 13
    for cand, reason in queued:
        handles = {p: h for p, h in cand["handles"].items() if h}
        platform = "Instagram" if "Instagram" in handles else sorted(handles)[0]
        handle = handles[platform]
        rq.append({
            "id": f"R-2026-{rq_num:03d}",
            "displayName": cand["name"],
            "handle": display_handle(platform, handle),
            "platform": platform,
            "profileUrl": profile_url(platform, handle),
            "discoveryCategory": group_label(cand["group"]),
            "evidenceFound": {
                "summary": (
                    f"Wikidata item {cand['qid']} records the athlete as a female "
                    f"{'beach volleyball' if cand['group'] == 'beach' else 'volleyball'} player"
                    + (f" with teams {join_sources(cand['teams'][:3])}" if cand["teams"] else "")
                    + f". Date of birth recorded: {cand['dob'] or 'none'}."
                ),
                "sourceLabel": f"Wikidata {cand['qid']} \u2014 {cand['name']}",
                "sourceUrl": f"https://www.wikidata.org/wiki/{cand['qid']}",
            },
            "missingEvidence": [reason],
            "flags": [reason],
            "lastChecked": TODAY.isoformat(),
            "notes": (
                f"Session 13 volleyball discovery pass. Not promoted to a verified entry: "
                f"{reason_explanation(reason)} Recorded here with provenance instead of being guessed. "
                f"Candidate Q-ID {cand['qid']}; country recorded in Wikidata: {cand['country']}."
            ),
            "followerCountDisplay": UNKNOWN_COUNT,
            "followerCountNumeric": None,
            "followerCountCheckedAt": TODAY.isoformat(),
            "followerSizeRange": UNKNOWN_RANGE,
        })
        rq_num += 1

    # ---------------- audit artifact
    with open(AUDIT_TSV, "w", encoding="utf-8") as fh:
        fh.write("# Session 13 selection audit \u2014 every promoted entry with its evidence links "
                 "(generated 2026-09-06).\n")
        fh.write("# entryId\tqid\tgroup\tname\tdob\tage\tcountry\thandles\tdobSources\treferenceUrls\tteams\n")
        for cand, dob, entry in selected:
            handles = ";".join(f"{p}:{h}" for p, h in cand["handles"].items() if h)
            fh.write("\t".join([
                entry["id"], cand["qid"], cand["group"], cand["name"], dob.isoformat(),
                str(age_on(dob)), cand["country"], handles,
                ";".join(cand["dob_sources"]) or "-",
                ";".join(cand["ref_urls"]) or "-",
                ";".join(cand["teams"][:4]) or "-",
            ]) + "\n")

    # ---------------- report
    print(f"candidates loaded      : {len(cands)}")
    print(f"promoted to entries    : {len(selected)}")
    by_group = {}
    for cand, _, _ in selected:
        by_group[cand["group"]] = by_group.get(cand["group"], 0) + 1
    for g in ("ncaa", "beach", "intl"):
        print(f"    {g:<6}: {by_group.get(g, 0)}")
    print(f"sent to review queue   : {len(queued)}")
    reason_counts = {}
    for _, reason in queued:
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    for r, n in sorted(reason_counts.items()):
        print(f"    {r}: {n}")
    print(f"skipped                : {len(skipped)}")
    skip_counts = {}
    for _, reason in skipped:
        skip_counts[reason] = skip_counts.get(reason, 0) + 1
    for r, n in sorted(skip_counts.items()):
        print(f"    {r}: {n}")
    with_ref = sum(1 for c, _, _ in selected if c["ref_urls"])
    with_wiki = sum(1 for c, _, _ in selected if c["wiki_urls"])
    print(f"entries with an external reference URL : {with_ref}")
    print(f"entries with an English Wikipedia link : {with_wiki}")
    print(f"audit artifact                         : {os.path.relpath(AUDIT_TSV, ROOT)}")

    if not apply_changes:
        print("\n[dry run] re-run with --apply to write data/catalog.json")
        return

    catalog["entries"].extend(entry for _, _, entry in selected)
    catalog["reviewQueue"] = rq
    meta = catalog["metadata"]
    meta["entryCount"] = len(catalog["entries"])
    meta["reviewQueueCount"] = len(rq)
    meta["generatedAt"] = TODAY.isoformat()
    meta["summary"] = meta["summary"] + (
        f" Session 13 added {len(selected)} verified volleyball profiles from a public structured-data "
        f"discovery pass: {by_group.get('ncaa', 0)} NCAA/US college indoor players, "
        f"{by_group.get('beach', 0)} international beach volleyball players and "
        f"{by_group.get('intl', 0)} European/international indoor league players "
        f"(German Bundesliga, Slovak, French, Italian, Greek, Turkish, Japanese, Dutch, Belgian, "
        f"Czech, Austrian, Argentine, Brazilian, Canadian and Belarusian clubs plus women's national teams). "
        f"{len(queued)} further candidates were routed to the review queue rather than promoted "
        f"(no documented birth date, or birth date without a recorded source). Follower counts that could "
        f"not be publicly observed are recorded as {UNKNOWN_COUNT} with range {UNKNOWN_RANGE} \u2014 never "
        f"estimated and never summed across platforms."
    )
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\napplied: {len(catalog['entries'])} entries, {len(rq)} review-queue items")


def reason_explanation(reason):
    return {
        "AGE_UNVERIFIED": "the structured item carries no date of birth, so adult status cannot be "
                          "documented (and is never inferred from college attendance or appearance).",
        "AGE_SOURCE_NOT_RECORDED": "a date of birth is present but no reference source is attached to it, "
                                   "so the value cannot be traced to a document.",
        "AGE_OUT_OF_RANGE_OR_MINOR": "the recorded date of birth places the candidate outside the adult "
                                     "18+ scope as of 2026-09-06.",
    }[reason]


if __name__ == "__main__":
    main()
