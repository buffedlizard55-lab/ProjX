#!/usr/bin/env python3
"""Session 12 batch W (2026-09-06): 1 verified add (W-2026-201).
Katie Taylor: DOB 1986-07-02 x5 (theirishinsider, playundisputed official
game-roster bio, imdb, thecityceleb structured, surprisesports); women's
boxing career (2012 Olympic lightweight gold, 2-weight undisputed champion).
"""
import json
from pathlib import Path

CHECKED = "2026-09-06"
CATALOG = Path("data/catalog.json")

def ev(s, l, u): return {"summary": s, "sourceLabel": l, "sourceUrl": u, "checkedAt": CHECKED}
def src(l, p, u, r): return {"label": l, "platform": p, "url": u, "relationship": r}

NEW = [dict(
    id="W-2026-201", displayName="Katie Taylor",
    categories=["Athlete", "Boxing", "Creator"],
    legalAdultEvidence=ev(
        "Born July 2, 1986 in Bray, County Wicklow, Ireland — age 40 in 2026 — per the Irish Insider (Birth Date 2 July 1986), the official Undisputed game roster bio (born 2 July 1986), IMDb (born 2 July 1986) and thecityceleb structured record (birthDate 1986-07-02).",
        "Irish Insider — Katie Taylor biography (Birth Date 2 July 1986)", "https://theirishinsider.ie/the-local-lens/locals-that-are-making-impact/katie-taylor/"),
    genderEvidence=ev(
        "Identified as a woman via women's boxing career — 2012 Olympic gold in the women's lightweight division ('Gold medal winner in women's lightweight boxing (60kg) at the 2012 London Olympics'), undisputed women's lightweight and light-welterweight champion (IMDb/Undisputed roster).",
        "IMDb — Katie Taylor bio (women's lightweight Olympic gold)", "https://www.imdb.com/name/nm2513572/"),
    sources=[
        src("Irish Insider — Katie Taylor biography (Birth Date 2 July 1986; career)", "Website", "https://theirishinsider.ie/the-local-lens/locals-that-are-making-impact/katie-taylor/", "other-trusted"),
        src("Undisputed (official game roster) — Katie Taylor bio (born 2 July 1986; undisputed record)", "Website", "https://playundisputed.com/roster/katie-taylor", "official"),
        src("IMDb — Katie Taylor (born 2 July 1986; women's boxing career)", "Website", "https://www.imdb.com/name/nm2513572/", "other-trusted"),
        src("TheCityCeleb — Katie Taylor biography (structured birthDate 1986-07-02)", "Website", "https://www.thecityceleb.com/biography/public-figure/sportsperson/katie-taylor-biography-awards-nationality-age-record-height-parents-boxing-career-net-worth/", "other-trusted")],
    verificationStatus="verified", lastReviewed=CHECKED, flags=[],
    notes=("2012 Olympic women's lightweight gold medalist and two-weight undisputed professional world champion — widely regarded among the greatest female boxers of all time — objective athlete category; verified 40 years old. No social handle captured this pass — follower range UNKNOWN."),
    socialAccounts=[],
    largestPublicFollowing={"platform": None, "username": None, "display": None,
                            "numeric": None, "sizeRange": "FOLLOWER_RANGE_UNKNOWN",
                            "checkedAt": CHECKED},
    overallFollowerSizeRange="FOLLOWER_RANGE_UNKNOWN")]


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
