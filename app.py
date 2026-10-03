import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DU College Predictor", page_icon="🎓", layout="wide")

# ---------- Load data ----------
# Build the path relative to this script's own location, not the current working
# directory (the server may launch the app from a different folder than expected).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "du_cutoffs_2025.csv")

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(
            f"Data file not found at: {DATA_PATH}\n\n"
            "This means the 'data' folder was not pushed to GitHub, or the CSV "
            "inside it is missing. Check your repo on github.com and confirm "
            "data/du_cutoffs_2025.csv is actually there."
        )
        st.stop()
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()

st.title("🎓 DU College & Course Predictor")
st.caption(
    "Based on Delhi University's 2025 CUET UG cutoff data (Round 1, ~50 college-course combinations). "
    "Enter your CUET score and category to see which colleges/courses you'd likely have qualified for."
)

# ---------- Sidebar inputs ----------
st.sidebar.header("Your Details")
score = st.sidebar.number_input("Your CUET Score (out of ~1000)", min_value=0.0, max_value=1000.0, value=850.0, step=1.0)
category = st.sidebar.selectbox("Category", sorted(df["category"].unique()))
course_filter = st.sidebar.multiselect("Filter by Course (optional)", sorted(df["course"].unique()))

# ---------- Filter logic ----------
filtered = df[df["category"] == category].copy()
if course_filter:
    filtered = filtered[filtered["course"].isin(course_filter)]

eligible = filtered[filtered["cutoff_score"] <= score].sort_values("cutoff_score", ascending=False)
close_miss = filtered[
    (filtered["cutoff_score"] > score) & (filtered["cutoff_score"] <= score + 30)
].sort_values("cutoff_score")

# ---------- Results ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"✅ You qualify for ({len(eligible)})")
    if eligible.empty:
        st.info("No matches at this score for the selected category/course filter.")
    else:
        st.dataframe(
            eligible[["college", "course", "cutoff_score"]].rename(
                columns={"college": "College", "course": "Course", "cutoff_score": "Cutoff"}
            ),
            use_container_width=True,
            hide_index=True,
        )

with col2:
    st.subheader(f"🔶 Close misses — within 30 marks ({len(close_miss)})")
    if close_miss.empty:
        st.info("None nearby.")
    else:
        st.dataframe(
            close_miss[["college", "course", "cutoff_score"]].rename(
                columns={"college": "College", "course": "Course", "cutoff_score": "Cutoff"}
            ),
            use_container_width=True,
            hide_index=True,
        )

st.divider()

# ---------- Visualization ----------
st.subheader("📊 Where your score lands")
plot_df = filtered.sort_values("cutoff_score", ascending=False).head(25).copy()
plot_df["label"] = plot_df["college"] + " — " + plot_df["course"]
plot_df["status"] = plot_df["cutoff_score"].apply(lambda c: "Eligible" if c <= score else "Not eligible")

fig = px.bar(
    plot_df,
    x="cutoff_score",
    y="label",
    color="status",
    orientation="h",
    color_discrete_map={"Eligible": "#2ecc71", "Not eligible": "#e74c3c"},
    labels={"cutoff_score": "Cutoff Score", "label": ""},
    title=f"Top 25 cutoffs for {category} category" + (f" ({', '.join(course_filter)})" if course_filter else ""),
)
fig.add_vline(x=score, line_dash="dash", line_color="blue", annotation_text="Your score")
fig.update_layout(height=700, yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

st.divider()


st.subheader("📈 Category-wise cutoff gap (General vs Reserved categories)")
pivot = df.pivot_table(index=["college", "course"], columns="category", values="cutoff_score").dropna()
if "UR" in pivot.columns and "SC" in pivot.columns:
    pivot["UR_minus_SC_gap"] = pivot["UR"] - pivot["SC"]
    avg_gap = pivot["UR_minus_SC_gap"].mean()
    st.metric("Average UR vs SC cutoff gap across all course combinations", f"{avg_gap:.1f} points")
    st.caption(
        "This reflects the structural gap in cutoffs between General and SC category across the sampled "
        "college-course combinations — a genuine pattern worth noting, not a judgment on any policy."
    )

st.divider()
st.caption(
    "⚠️ Disclaimer: This tool uses Round 1, 2025 CUET cutoff data for a sample of ~25 popular DU colleges "
    "and is for exploratory/educational purposes only. Actual cutoffs vary by year, round, and seat "
    "availability. Always confirm with official DU CSAS portal (ugadmission.uod.ac.in) before making decisions."
)
