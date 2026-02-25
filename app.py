# app.py
# Streamlit dashboard for CareVeda FES Scoring Output
# Expects: careveda_fes_scored.csv in the same folder

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="CareVeda CRM Dashboard", layout="wide")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Defensive type casting
    for c in ["FES_score", "churn_risk_prob", "upgrade_prob", "referral_prob"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

st.title("CareVeda Family Engagement Score (FES) Dashboard")

# ---------------------------
# Data load
# ---------------------------
csv_path = st.sidebar.text_input("CSV path", "careveda_fes_scored.csv")
df = load_data(csv_path)

required_cols = {
    "family_id",
    "CRM_tier",
    "FES_score",
    "churn_risk_prob",
    "upgrade_prob",
    "referral_prob",
    "recommended_action",
}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"Missing required columns in CSV: {sorted(missing)}")
    st.stop()

# Optional fields (if present, we will use them)
optional_cols = [
    "acquisition_channel",
    "plan_tier",
    "city",
    "senior_dependency_level",
    "months_active",
    "family_app_logins_week",
    "daily_report_opens",
    "caregiver_rating_avg",
    "incidents_resolved_pct",
]

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("Filters")

tier_order = ["RED", "AMBER", "GREEN"]
tiers = st.sidebar.multiselect(
    "CRM Tier",
    options=tier_order,
    default=tier_order,
)

df_f = df[df["CRM_tier"].isin(tiers)].copy()

# If encoded categories exist, allow filtering anyway
for col in ["acquisition_channel", "plan_tier", "city", "senior_dependency_level"]:
    if col in df_f.columns:
        vals = sorted(df_f[col].dropna().unique().tolist())
        sel = st.sidebar.multiselect(f"{col}", options=vals, default=vals)
        df_f = df_f[df_f[col].isin(sel)]

# Numeric filters
fes_min, fes_max = float(np.nanmin(df["FES_score"])), float(np.nanmax(df["FES_score"]))
fes_range = st.sidebar.slider("FES score range", min_value=0.0, max_value=100.0, value=(max(0.0, fes_min), min(100.0, fes_max)))
df_f = df_f[(df_f["FES_score"] >= fes_range[0]) & (df_f["FES_score"] <= fes_range[1])]

cr_min, cr_max = float(np.nanmin(df["churn_risk_prob"])), float(np.nanmax(df["churn_risk_prob"]))
cr_range = st.sidebar.slider("Churn risk probability range", min_value=0.0, max_value=1.0, value=(max(0.0, cr_min), min(1.0, cr_max)))
df_f = df_f[(df_f["churn_risk_prob"] >= cr_range[0]) & (df_f["churn_risk_prob"] <= cr_range[1])]

top_n = st.sidebar.number_input("Top N for tables", min_value=5, max_value=200, value=20, step=5)

# ---------------------------
# KPI row
# ---------------------------
total = len(df_f)
avg_fes = float(df_f["FES_score"].mean()) if total else 0.0
avg_churn_risk = float(df_f["churn_risk_prob"].mean()) if total else 0.0
avg_upgrade = float(df_f["upgrade_prob"].mean()) if total else 0.0
avg_ref = float(df_f["referral_prob"].mean()) if total else 0.0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Families", f"{total:,}")
k2.metric("Avg FES", f"{avg_fes:.1f}")
k3.metric("Avg Churn Risk", f"{avg_churn_risk:.2f}")
k4.metric("Avg Upgrade Prob", f"{avg_upgrade:.2f}")
k5.metric("Avg Referral Prob", f"{avg_ref:.2f}")

st.divider()

# ---------------------------
# Layout: Charts
# ---------------------------
c1, c2 = st.columns(2)

with c1:
    # Tier distribution
    tier_counts = df_f["CRM_tier"].value_counts().reindex(tier_order).fillna(0).astype(int).reset_index()
    tier_counts.columns = ["CRM_tier", "count"]
    fig_tier = px.bar(
        tier_counts,
        x="CRM_tier",
        y="count",
        title="CRM Tier Distribution",
        text="count",
    )
    fig_tier.update_layout(xaxis_title="", yaxis_title="Families")
    st.plotly_chart(fig_tier, use_container_width=True)

with c2:
    # Scatter FES vs churn risk
    fig_scatter = px.scatter(
        df_f,
        x="FES_score",
        y="churn_risk_prob",
        color="CRM_tier",
        hover_data=["family_id", "upgrade_prob", "referral_prob"],
        title="FES Score vs Churn Risk",
    )
    fig_scatter.update_layout(xaxis_title="FES (0-100)", yaxis_title="Churn Risk Probability")
    st.plotly_chart(fig_scatter, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    # Churn risk by acquisition channel or fallback to tier
    group_col = "acquisition_channel" if "acquisition_channel" in df_f.columns else "CRM_tier"
    g = df_f.groupby(group_col, dropna=False)["churn_risk_prob"].mean().reset_index().sort_values("churn_risk_prob", ascending=False)
    fig_churn = px.bar(
        g,
        x=group_col,
        y="churn_risk_prob",
        title=f"Average Churn Risk by {group_col}",
        text=g["churn_risk_prob"].round(2),
    )
    fig_churn.update_layout(xaxis_title="", yaxis_title="Avg Churn Risk")
    st.plotly_chart(fig_churn, use_container_width=True)

with c4:
    # Upgrade and referral propensity by tier
    g2 = df_f.groupby("CRM_tier")[["upgrade_prob", "referral_prob"]].mean().reindex(tier_order).reset_index()
    g2_m = g2.melt(id_vars="CRM_tier", var_name="metric", value_name="value")
    fig_ur = px.bar(
        g2_m,
        x="CRM_tier",
        y="value",
        color="metric",
        barmode="group",
        title="Upgrade and Referral Propensity by CRM Tier",
        text=g2_m["value"].round(2),
    )
    fig_ur.update_layout(xaxis_title="", yaxis_title="Average Probability")
    st.plotly_chart(fig_ur, use_container_width=True)

st.divider()

# ---------------------------
# Action board tables
# ---------------------------
t1, t2 = st.columns(2)

with t1:
    st.subheader(f"Top {int(top_n)} Highest Churn Risk Families")
    cols = [
        "family_id",
        "CRM_tier",
        "FES_score",
        "churn_risk_prob",
        "upgrade_prob",
        "referral_prob",
        "recommended_action",
    ] + [c for c in optional_cols if c in df_f.columns]
    top_risk = df_f.sort_values("churn_risk_prob", ascending=False).head(int(top_n))[cols]
    st.dataframe(top_risk, use_container_width=True, height=420)

with t2:
    st.subheader(f"Top {int(top_n)} Best Growth Candidates (High FES)")
    top_growth = df_f.sort_values(["FES_score", "referral_prob", "upgrade_prob"], ascending=False).head(int(top_n))[cols]
    st.dataframe(top_growth, use_container_width=True, height=420)

# ---------------------------
# Download filtered data
# ---------------------------
st.divider()
st.subheader("Export")
csv_bytes = df_f.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered dataset (CSV)",
    data=csv_bytes,
    file_name="careveda_fes_scored_filtered.csv",
    mime="text/csv",
)

st.caption("Tip: run with  streamlit run app.py")
