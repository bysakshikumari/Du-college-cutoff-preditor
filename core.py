"""Data loading and prediction logic."""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

CATEGORIES = {"UR": "UR (General)", "OBC": "OBC-NCL", "SC": "SC", "ST": "ST", "EWS": "EWS", "PwBD": "PwBD",
              "SGC": "SGC (Single Girl Child)", "KM": "KM (Kashmiri Migrant)", "SIKH": "Sikh minority",
              "OF": "Orphan (Female)", "OM": "Orphan (Male)"}
STREAMS = ["Science", "Commerce", "Arts (Hons)", "BA Programme", "Other"]
TIERS = ["Round 1 likely", "Round 2 likely", "Spot possible", "Stretch", "Out of reach"]
SHORT = ["Round 1", "Round 2", "Spot", "Stretch"]
ICONS = ["🟢", "🟡", "🔵", "🟠", "⚪"]
HELP = ["Your score is at or above the 2026 Round 1 cutoff.",
        "Below the Round 1 cutoff but at or above the 2026 Round 2 cutoff.",
        "Only if seats remain: at or above the 2026 Spot Round cutoff.",
        "Within the stretch band below the Round 2 cutoff. Possible if cutoffs dip next year."]
STRETCH = 30      # marks below the Round 2 cutoff that still count as a "Stretch"
SAFE_MARGIN = 15  # marks above the Round 1 cutoff needed to call a course "Safe"
COLUMNS = {"2025_R1": "r1_25", "2026_R1": "r1", "2026_R2": "r2", "2026_Spot": "spot"}


def stream(course):
    for prefix, name in [("B.Sc", "Science"), ("B.Com", "Commerce"), ("B.A. (Hons", "Arts (Hons)"), ("B.A. Program", "BA Programme")]:
        if course.startswith(prefix):
            return name
    return "Other"


def subject(course):
    """Comparable subject name for Honours-style courses (None for combinations)."""
    m = re.match(r"^B\.(?:A|Sc)\. \(Hons\.\) (.+)$", course)
    if m:
        return m.group(1)
    if course.startswith("B.Com. (Hons"):
        return "B.Com (Hons.)"
    if course == "B.Com.":
        return "B.Com (Pass)"
    return "BMS" if course.startswith("Bachelor of Management Studies") else None


@st.cache_data
def load():
    """One row per college x course x category, with columns r1_25, r1, r2, spot."""
    df = pd.read_csv(Path(__file__).parent / "data" / "du_cutoffs.csv")
    df["key"] = df["year"].astype(str) + "_" + df["round"]
    df = df[df["key"].isin(COLUMNS)]
    w = df.pivot_table(index=["college", "course", "category"], columns="key", values="cutoff_score").rename(columns=COLUMNS).reset_index()
    w = w.reindex(columns=["college", "course", "category", "r1_25", "r1", "r2", "spot"])
    w = w[w[["r1", "r2", "spot"]].notna().any(axis=1)]  # keep only courses that ran in 2026
    w["stream"] = w["course"].map(stream)
    w["subject"] = w["course"].map(subject)
    w["yoy"] = w["r1"] - w["r1_25"]      # 2026 R1 vs 2025 R1
    w["r1_to_r2"] = w["r2"] - w["r1"]    # how far the cutoff falls in Round 2
    return w


def classify(d, score):
    """Give every row a tier (0-4) and your margin over the Round 1 cutoff."""
    ref = d["r2"].fillna(d["r1"]).fillna(d["spot"])
    tier = np.select([score >= d["r1"], score >= d["r2"], score >= d["spot"], score >= ref - STRETCH], [0, 1, 2, 3], default=4)
    return d.assign(tier=tier, margin=score - d["r1"],
                    verdict=[f"{ICONS[t]} {TIERS[t]}" for t in tier])


def ordered(d):
    """Best (highest-cutoff) college first."""
    return d.sort_values("r1", ascending=False, na_position="last")


def shortlist(d, k=5):
    """Picks in priority order, one course per college in each bucket."""
    top = lambda x: ordered(x).drop_duplicates("college").head(k)
    r1 = d[d["tier"] == 0]
    return {"🟢 Safe in Round 1": top(r1[r1["margin"] >= SAFE_MARGIN]),
            "🎯 Round 1, close call": top(r1[r1["margin"] < SAFE_MARGIN]),
            "🟡 Round 2 plays": top(d[d["tier"] == 1]),
            "🟠 Reach": top(d[d["tier"] == 3])}
