"""Plotly charts."""
import numpy as np
import plotly.express as px


def ladder(d, score):
    """One course across colleges: 2025 R1, 2026 R1, R2 and Spot, with your score as a red line."""
    d = d.sort_values("r1")
    fig = px.scatter()
    xs, ys = [], []
    for r in d.dropna(subset=["r2"]).itertuples():  # grey bar from R1 to R2
        xs += [r.r2, r.r1, None]
        ys += [r.college, r.college, None]
    fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color="rgba(150,150,150,.5)", width=3), hoverinfo="skip", showlegend=False)
    for col, name, color, symbol in [("r1_25", "2025 R1", "#9ca3af", "circle-open"), ("r1", "2026 R1", "#2563eb", "circle"),
                                     ("r2", "2026 R2", "#d97706", "diamond"), ("spot", "2026 Spot", "#7c3aed", "x")]:
        fig.add_scatter(x=d[col], y=d["college"], mode="markers", name=name, marker=dict(color=color, symbol=symbol, size=10))
    fig.add_vline(x=score, line_dash="dash", line_color="#dc2626", annotation_text="Your score")
    fig.update_layout(height=max(380, 26 * len(d) + 140), legend=dict(orientation="h", y=1.06), xaxis_title="Cutoff score",
                      yaxis=dict(categoryorder="array", categoryarray=list(d["college"]), title=""), margin=dict(l=0, r=10, t=40, b=10))
    return fig


def subject_bars(d, col, title):
    """Median change per subject (only subjects with 6+ courses)."""
    g = d.dropna(subset=["subject", col]).groupby("subject")[col].agg(["count", "median"]).query("count >= 6").sort_values("median")
    fig = px.bar(g.reset_index(), x="median", y="subject", orientation="h", title=title, color="median",
                 color_continuous_scale=["#16a34a", "#e5e7eb", "#ea580c"], color_continuous_midpoint=0,
                 labels={"median": "Median change (points)", "subject": ""})
    return fig.update_layout(coloraxis_showscale=False, height=max(360, 24 * len(g) + 120))


def year_scatter(d):
    """Every course: 2025 vs 2026 Round 1 cutoff. Above the dashed line = cutoff rose."""
    fig = px.scatter(d, x="r1_25", y="r1", color="stream", hover_data=["college", "course"], opacity=0.7,
                     labels={"r1_25": "2025 Round 1 cutoff", "r1": "2026 Round 1 cutoff"}, title="Every programme: 2025 vs 2026 (above the line = cutoff rose)")
    lo, hi = d[["r1_25", "r1"]].min().min(), d[["r1_25", "r1"]].max().max()
    fig.add_scatter(x=[lo, hi], y=[lo, hi], mode="lines", line=dict(dash="dash", color="gray"), showlegend=False, hoverinfo="skip")
    return fig.update_layout(height=520)


def change_hist(d, col, title):
    fig = px.histogram(d, x=col, nbins=40, title=title, labels={col: "Change (points)"})
    fig.add_vline(x=float(np.nanmedian(d[col])), line_dash="dash", annotation_text="median")
    return fig.update_layout(height=340, yaxis_title="Programmes")
