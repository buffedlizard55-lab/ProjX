#!/usr/bin/env python3
"""Session 12 batch G (2026-09-06): 6 verified adds (W-2026-153..158).
WNBA roster run: basketball-reference structured pages (birthDate JSON-LD +
Instagram handle in one view) corroborated by Wikipedia/usbasket/proballers/
briefly.co.za. Dup-guard: all 6 names grep-checked before authoring.
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

def acct(p, u, url, note):
    return {"platform": p, "username": u, "profileUrl": url,
            "followerCountDisplay": "FOLLOWER_COUNT_UNKNOWN", "followerCountNumeric": None,
            "countType": "unknown", "checkedAt": CHECKED,
            "followerSizeRange": "FOLLOWER_RANGE_UNKNOWN", "sourceNote": note}

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

def ent(i, n, a, g, s, flags, notes, accts):
    return {"id": i, "displayName": n, "categories": ["Athlete", "Basketball", "Creator"],
            "legalAdultEvidence": a, "genderEvidence": g, "sources": s,
            "verificationStatus": "verified", "lastReviewed": CHECKED, "flags": flags,
            "notes": notes, "socialAccounts": accts,
            "largestPublicFollowing": {"platform": None, "username": None, "display": None,
                                       "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                                       "checkedAt": CHECKED},
            "overallFollowerSizeRange": "FOLLOWER_RANGE_UNKNOWN"}

NEW = []

NEW.append(ent("W-2026-153", "Napheesa Collier",
    ev("Born September 23, 1996 in Jefferson City, Missouri — age 29 in 2026 — per basketball-reference structured record (birthDate 1996-09-23), Wikipedia (born September 23, 1996), proballers (born September 23, 1996) and wnba.miraheze wiki.",
       "Basketball-Reference — Napheesa Collier (born September 23, 1996)", "https://www.basketball-reference.com/wnba/players/c/collina01w.html"),
    ev("Identified as a woman via WNBA women's basketball career (Minnesota Lynx star forward; Unrivaled league co-founder) and be-basketball structured data ('gender: https://schema.org/Female').",
       "Be-basketball — Napheesa Collier (gender schema.org/Female structured)", "https://www.be-basketball.com/player/napheesa-collier"),
    [src("Basketball-Reference — Napheesa Collier (DOB 1996-09-23; Instagram: napheesa24)", "Website", "https://www.basketball-reference.com/wnba/players/c/collina01w.html", "age-evidence"),
     src("Wikipedia — Napheesa Collier (DOB 1996-09-23; UConn/Unrivaled founder)", "Website", "https://en.wikipedia.org/wiki/Napheesa_Collier", "other-trusted"),
     src("Proballers — Napheesa Collier (DOB Sep 23, 1996)", "Website", "https://www.proballers.com/basketball/player/184783/collier-napheesa", "other-trusted"),
     src("Instagram — @napheesa24 (basketball-reference displayed handle)", "Instagram", "https://www.instagram.com/napheesa24/", "verified-platform")],
    [], "2019 WNBA Rookie of the Year and Unrivaled league co-founder — objective athlete category. IG handle via basketball-reference; count not captured — UNKNOWN.",
    [acct("Instagram", "@napheesa24", "https://www.instagram.com/napheesa24/", "Handle via basketball-reference player page; count not captured.")]))

NEW.append(ent("W-2026-154", "Breanna Stewart",
    ev("Born August 27, 1994 in North Syracuse, New York — age 32 in 2026 — per basketball-reference structured record (birthDate 1994-08-27), Wikipedia (born August 27, 1994), wnba.com official player page (Birthdate Aug 27, 1994) and usbasket (born Aug.27, 1994).",
       "Basketball-Reference — Breanna Stewart (born August 27, 1994)", "https://www.basketball-reference.com/wnba/players/s/stewabr01w.html"),
    ev("Identified as a woman via WNBA women's basketball career — New York Liberty forward, multiple WNBA MVP awards, Unrivaled co-founder (Wikipedia/wnba.com).",
       "WNBA.com — Breanna Stewart official player page", "https://www.wnba.com/player/1627668/breanna-stewart"),
    [src("Basketball-Reference — Breanna Stewart (DOB 1994-08-27; Instagram: breannastewart30)", "Website", "https://www.basketball-reference.com/wnba/players/s/stewabr01w.html", "age-evidence"),
     src("WNBA.com — Breanna Stewart official player page (Birthdate Aug 27, 1994)", "Website", "https://www.wnba.com/player/1627668/breanna-stewart", "official"),
     src("Wikipedia — Breanna Stewart (DOB 1994-08-27)", "Website", "https://en.wikipedia.org/wiki/Breanna_Stewart", "other-trusted"),
     src("Instagram — @breannastewart30 (basketball-reference displayed handle)", "Instagram", "https://www.instagram.com/breannastewart30/", "verified-platform")],
    [], "2x WNBA MVP, 4x NCAA champion (UConn) and Unrivaled league co-founder — objective athlete category. IG handle via basketball-reference; count not captured — UNKNOWN.",
    [acct("Instagram", "@breannastewart30", "https://www.instagram.com/breannastewart30/", "Handle via basketball-reference player page; count not captured.")]))

NEW.append(ent("W-2026-155", "Kelsey Plum",
    ev("Born August 24, 1994 in Poway, California — age 32 in 2026 — per basketball-reference structured record (birthDate 1994-08-24) and briefly.co.za profile (Date of birth: 24th August 1994).",
       "Basketball-Reference — Kelsey Plum (born August 24, 1994)", "https://www.basketball-reference.com/wnba/players/p/plumke01w.html"),
    ev("Identified as a woman via WNBA women's basketball career — 2x WNBA champion, 2022 All-Star MVP, five-time All-Star with Las Vegas Aces (basketball-reference honors list).",
       "Basketball-Reference — Kelsey Plum (2x WNBA Champ, 5x All Star)", "https://www.basketball-reference.com/wnba/players/p/plumke01w.html"),
    [src("Basketball-Reference — Kelsey Plum (DOB 1994-08-24; Instagram: kelseyplum10)", "Website", "https://www.basketball-reference.com/wnba/players/p/plumke01w.html", "age-evidence"),
     src("Briefly — Kelsey Plum bio (DOB 24 August 1994; IG/Twitter @kelseyplum10)", "Website", "https://briefly.co.za/facts-lifehacks/celebrities-biographies/118202-kelsey-plum-bio-age-husband-ethnicity-stats-salary-wnba-team-net-worth/", "other-trusted"),
     src("Instagram — @kelseyplum10 (basketball-reference + briefly displayed handle)", "Instagram", "https://www.instagram.com/kelseyplum10/", "verified-platform"),
     src("X — @Kelseyplum10 (briefly.co.za displayed handle)", "X", "https://x.com/Kelseyplum10", "verified-platform")],
    [], "2x WNBA champion and 2022 All-Star MVP (Washington Huskies all-time scorer) — objective athlete category. Handles via basketball-reference + briefly; counts not captured — UNKNOWN.",
    [acct("Instagram", "@kelseyplum10", "https://www.instagram.com/kelseyplum10/", "Handle via basketball-reference + briefly.co.za bio; count not captured."),
     acct("X", "@Kelseyplum10", "https://x.com/Kelseyplum10", "Handle via briefly.co.za bio; count not captured.")]))

NEW.append(ent("W-2026-156", "Jackie Young",
    ev("Born September 16, 1997 in Princeton, Indiana — age 28 in 2026 — per proballers (born September 16, 1997), wnba.miraheze wiki (born September 16, 1997) and grokipedia (born September 16, 1997).",
       "Proballers — Jackie Young (born September 16, 1997)", "https://www.proballers.com/basketball/player/184773/young-jackie"),
    ev("Identified as a woman via WNBA women's basketball career — 2019 first overall pick, 2022 Most Improved Player, 3x WNBA champion with Las Vegas Aces, 2x Olympic gold (proballers/wnba.miraheze).",
       "WNBA Wiki (Miraheze) — Jackie Young (2019 1st overall; Olympic golds)", "https://wnba.miraheze.org/wiki/Jackie_Young"),
    [src("Proballers — Jackie Young (DOB Sep 16, 1997)", "Website", "https://www.proballers.com/basketball/player/184773/young-jackie", "age-evidence"),
     src("WNBA Wiki (Miraheze) — Jackie Young (DOB 1997-09-16; career honors)", "Website", "https://wnba.miraheze.org/wiki/Jackie_Young", "other-trusted"),
     src("Grokipedia — Jackie Young (DOB 1997-09-16; Notre Dame career)", "Website", "https://grokipedia.com/page/jackie_young", "other-trusted")],
    [], "2019 WNBA first overall pick and 2022 Most Improved Player; 2020 Tokyo 3x3 + 2024 Paris 5x5 Olympic golds — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))

NEW.append(ent("W-2026-157", "Sabrina Ionescu",
    ev("Born December 6, 1997 in Walnut Creek, California — age 28 in 2026 — per basketball-reference structured record (birthDate 1997-12-06) and usbasket (born Dec.6, 1997 in Walnut Creek, CA).",
       "Basketball-Reference — Sabrina Ionescu (born December 6, 1997)", "https://www.basketball-reference.com/wnba/players/i/ionessa01w.html"),
    ev("Identified as a woman via WNBA women's basketball career — New York Liberty guard, 2024 WNBA champion, four-time All-Star (basketball-reference honors list; Oregon Ducks women's record).",
       "Basketball-Reference — Sabrina Ionescu (2024 WNBA Champ, 4x All Star)", "https://www.basketball-reference.com/wnba/players/i/ionessa01w.html"),
    [src("Basketball-Reference — Sabrina Ionescu (DOB 1997-12-06; Instagram: sabrina_i)", "Website", "https://www.basketball-reference.com/wnba/players/i/ionessa01w.html", "age-evidence"),
     src("USbasket — Sabrina Ionescu profile (born Dec.6, 1997)", "Website", "https://basketball.usbasket.com/player/Sabrina-Ionescu/297966", "other-trusted"),
     src("Instagram — @sabrina_i (basketball-reference displayed handle)", "Instagram", "https://www.instagram.com/sabrina_i/", "verified-platform")],
    [], "2020 first overall pick, 2024 WNBA champion and NCAA all-time triple-double leader (Oregon) — objective athlete category. IG handle via basketball-reference; count not captured — UNKNOWN.",
    [acct("Instagram", "@sabrina_i", "https://www.instagram.com/sabrina_i/", "Handle via basketball-reference player page; count not captured.")]))

NEW.append(ent("W-2026-158", "Jewell Loyd",
    ev("Born October 5, 1993 in Lincolnwood, Illinois — age 32 in 2026 — per eurobasket player profile (born October 5 1993), usbasket (Born: Oct.5, 1993), Wikiwand/Wikipedia (born October 5, 1993).",
       "Eurobasket — Jewell Loyd player profile (born October 5, 1993)", "https://basketball.eurobasket.com/player/Jewell-Loyd/WNBA/Seattle-Storm/203237"),
    ev("Identified as a woman via WNBA women's basketball career — 2015 Rookie of the Year, 2x WNBA champion, 2x Olympic gold medalist (thendalliance.org ambassador bio; Wikipedia).",
       "ND Alliance — Jewell Loyd ambassador bio (WNBA/Olympic honors)", "https://thendalliance.org/celebrity-ambassador/jewell-loyd/"),
    [src("Eurobasket — Jewell Loyd (DOB Oct 5, 1993)", "Website", "https://basketball.eurobasket.com/player/Jewell-Loyd/WNBA/Seattle-Storm/203237", "age-evidence"),
     src("Wikipedia — Jewell Loyd (DOB 1993-10-05; career medal record)", "Website", "https://en.wikipedia.org/wiki/Jewell_Loyd", "other-trusted"),
     src("ND Alliance — Jewell Loyd ambassador bio (2x Olympic gold; 2x WNBA champion)", "Website", "https://thendalliance.org/celebrity-ambassador/jewell-loyd/", "other-trusted")],
    [], "2015 WNBA first overall pick and Rookie of the Year; 2x Olympic gold medalist ('Gold Mamba') — objective athlete category. No handle captured this pass — follower range UNKNOWN.", []))


def build():
    data = json.loads(CATALOG.read_text())
    entries = data["entries"]
    ids = {e["id"] for e in entries}
    names = {e["displayName"].lower() for e in entries}
    urls = {s["url"] for e in entries for s in e["sources"]}
    for r in NEW:
        assert r["id"] not in ids, r["id"]
        assert r["displayName"].lower() not in names, r["displayName"]
        assert not ({s["url"] for s in r["sources"]} & urls), r["displayName"]
    entries.extend(NEW)
    data["metadata"]["entryCount"] = len(entries)
    data["metadata"]["generatedAt"] = CHECKED
    CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"entries={len(entries)} (+{len(NEW)})")

if __name__ == "__main__":
    build()
