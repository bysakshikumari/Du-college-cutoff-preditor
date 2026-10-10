# DU College & Course Predictor

Streamlit app that shows which Delhi University courses a CUET score can realistically get, based on the official
**2026** Round 1, Round 2 and Spot Round cutoffs (2025 Round 1 is used for trends only).

**Live demo:** - https://du-college-cutoff-predictor.streamlit.app/


## Problem

Every year, thousands of DU aspirants manually scroll through dozens of separate college PDFs
and news articles to figure out where their score stands. This tool consolidates that into one
searchable, visual, interactive interface.


## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```


## Files
```
app.py                  screen layout: sidebar filters + 5 tabs
core.py                 load the data, work out verdicts, build the shortlist
charts.py               the plotly charts
data/du_cutoffs.csv     year, round, college, course, category, cutoff_score
scripts/build_data.py   rebuild the CSV from the official PDFs
```


## How a verdict is chosen (all against 2026)
Round 1 likely: score >= Round 1 cutoff · Round 2 likely: score >= Round 2 cutoff · Spot possible: score >= Spot cutoff ·
Stretch: within 30 marks below the Round 2 cutoff · otherwise out of reach. "Safe" = 15+ marks above the Round 1 cutoff.
The 30 and 15 are constants at the top of `core.py`.


## Disclaimer

Verify with the official DU CSAS admission
portal before making decisions.
