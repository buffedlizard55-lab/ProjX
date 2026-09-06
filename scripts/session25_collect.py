#!/usr/bin/env python3
"""Session 25 — Data Collection & Ingestion Pipeline
Harvests, verifies, and integrates 100+ verified female adult creators in the focused domains:
NCAA volleyball, beach volleyball, beachwear, bikini fashion, fitness, fitness modeling, modeling,
and European / international volleyball leagues.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.json"

TODAY = date(2026, 9, 6)

UNKNOWN_COUNT = "FOLLOWER_COUNT_UNKNOWN"
UNKNOWN_RANGE = "FOLLOWER_RANGE_UNKNOWN"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

def strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(ch))

def norm_name(name: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(name).lower()).strip()

def parse_dob(dob_str: str) -> date | None:
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", dob_str.strip())
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None

def age_on(dob: date, on_date: date = TODAY) -> int:
    return on_date.year - dob.year - ((on_date.month, on_date.day) < (dob.month, dob.day))

def human_date(d: date) -> str:
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"

def clean_handle(platform: str, handle: str) -> str:
    handle = handle.strip()
    if handle.startswith("@"):
        return handle
    if platform in ("Instagram", "TikTok", "X"):
        return f"@{handle}"
    return handle

def make_profile_url(platform: str, handle: str) -> str:
    h = handle.lstrip("@").strip()
    if platform == "Instagram":
        return f"https://www.instagram.com/{h}/"
    if platform == "TikTok":
        return f"https://www.tiktok.com/@{h}"
    if platform == "X":
        return f"https://x.com/{h}"
    if platform == "Facebook":
        return f"https://www.facebook.com/{h}"
    if platform == "YouTube":
        return f"https://www.youtube.com/@{h}"
    return f"https://www.instagram.com/{h}/"

def assign_categories(occ_label: str, raw_name: str, notes: str = "") -> list[str]:
    occ = occ_label.lower()
    text = (occ + " " + notes).lower()
    cats = []
    
    if "beach volleyball" in text:
        cats.append("Beach Volleyball")
        cats.append("Athletics")
        cats.append("Sports")
    elif "volleyball" in text:
        cats.append("Volleyball")
        cats.append("Athletics")
        cats.append("Sports")
        
    if "fitness model" in text or "bodybuilder" in text or "fitness" in text:
        if "Fitness" not in cats:
            cats.append("Fitness")
        if "Fitness Model" not in cats:
            cats.append("Fitness Model")
            
    if "fashion model" in text or "swimwear" in text or "bikini" in text or "beachwear" in text:
        if "Modeling" not in cats:
            cats.append("Modeling")
        if "Fashion" not in cats:
            cats.append("Fashion")
            
    if not cats:
        if "model" in text:
            cats = ["Modeling", "Fashion", "Creator"]
        else:
            cats = ["Creator", "Sports"]
            
    if "Creator" not in cats and len(cats) < 3:
        cats.append("Creator")
        
    return cats

print("Session 25 collection module loaded.")
