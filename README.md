# DU College & Course Predictor

An interactive tool that predicts which Delhi University colleges and courses a student
would qualify for, based on their CUET UG score and category — built from real, published
2025 cutoff data.

**Live demo:** _(add your Streamlit Cloud link here after deployment)_

## Problem

Every year, thousands of DU aspirants manually scroll through dozens of separate college PDFs
and news articles to figure out where their score stands. This tool consolidates that into one
searchable, visual, interactive interface.

## Data

- Source: Delhi University 2025 CUET UG Round 1 cutoffs, compiled from publicly published
  college-wise cutoff tables.
- Coverage: 16 colleges, 19 courses, 4 categories (UR/OBC/SC/ST) — 207 records.
- File: `data/du_cutoffs_2025.csv`
- Columns: `college, course, category, cutoff_score` (CUET score out of ~1000)

**Limitation:** This is a single-year (2025), single-round snapshot for a sample of ~16
well-known DU colleges — not the full 60+ college list, and not a multi-year trend. It's
built to demonstrate the pipeline and be genuinely useful for the covered colleges; expanding
to more colleges/years is the natural next step (see below).

## Approach

1. Compiled and cleaned cutoff data into a flat CSV (`college, course, category, cutoff_score`).
2. Built an interactive Streamlit app: user enters their score + category, the app filters and
   ranks eligible college-course combinations, and flags "close miss" options within 30 marks.
3. Added a category-gap analysis showing the average cutoff difference between General (UR) and
   SC category across all sampled course combinations — a genuine, data-backed pattern.

## Key insight

Across the sampled colleges and courses, the average gap between the General (UR) cutoff and
SC category cutoff is visible directly in the app's metric panel — this kind of category-wise
disparity is a recurring, data-verifiable feature of the DU admission system worth highlighting
in any writeup.

## Tech stack

- Python, Pandas (data handling)
- Streamlit (app/UI)
- Plotly (interactive charts)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations & next steps

- Expand to all ~60 DU colleges and multiple years for real trend analysis (year-over-year
  cutoff drift).
- Add pre-CUET (2018–2021) percentage-based cutoffs as a separate, clearly labeled historical
  view — different scoring system, so not directly comparable to CUET-era marks.
- Layer a simple regression model to predict next year's likely cutoff range.

## Disclaimer

For educational/exploratory purposes only. Always verify with the official DU CSAS admission
portal before making decisions.
