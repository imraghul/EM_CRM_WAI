import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="CareVeda CRM Dashboard", layout="wide")

# ============================================================
# STEP 1 — Generate Synthetic CareVeda Dataset Inside App
# ============================================================

@st.cache_data
def generate_data(n=700):
    np.random.seed(42)

    df = pd.DataFrame({
        "family_id": [f"F{i:03d}" for i in range(1, n+1)],
        "family_app_logins_week": np.random.poisson(3, n),
        "months_active": np.random.randint(1, 25, n),
        "caregiver_rating_avg": np.random.normal(4, 0.6, n).clip(2.5, 5),
        "incidents_resolved_pct": np.random.uniform(50, 100, n),
        "daily_report_opens": np.random.uniform(20, 100, n),
        "upgrade_prob": np.random.uniform(0, 1, n),
        "referral_prob": np.random.uniform(0, 1, n)
    })

    # Simulate churn risk using behaviour logic
    df["churn_risk_prob"] = (
        (4 - df["caregiver_rating_avg"]) * 0.2 +
        (2 - df["family_app_logins_week"]) * 0.1 +
        (6 - df["months_active"]) * 0.05 +
        (70 - df["incidents_resolved_pct"]) * 0.01
    )

    df["churn_risk_prob"] = df["churn_risk_prob"].clip(0, 1)

    # FES formula
    df["FES_score"] = (
        (1 - df["churn_risk_prob"]) * 0.5 +
        df["upgrade_prob"] * 0.25 +
        df["referral_prob"] * 0.25
    ) * 100

    # CRM Tier logic
    df["CRM_tier"] = "AMBER"
    df.loc[(df["churn_risk_prob"] >= 0.6) | (df["FES_score"] < 45), "CRM_tier"] = "RED"
    df.loc[(df["churn_risk_prob"] < 0.3) & (df["FES_score"] >= 65), "CRM_tier"] = "GREEN"

    return df

df = generate_data()

# ============================================================
# KPI SECTION
# ============================================================

st.title("CareVeda Family Engagement Score Dashboard")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Families", len(df))
k2.metric("Avg FES", round(df["FES_score"].mean(), 1))
k3.metric("Avg Churn Risk", round(df["churn_risk_prob"].mean(), 2))
k4.metric("High Risk (RED %)", round((df["CRM_tier"]=="RED").mean()*100,1))

st.divider()

# ============================================================
# ROW 1 — Tier Distribution + Scatter
# ============================================================

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df["CRM_tier"].value_counts().reset_index(),
        x="index",
        y="CRM_tier",
        title="CRM Tier Distribution",
        labels={"index":"Tier","CRM_tier":"Families"}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(
        df,
        x="FES_score",
        y="churn_risk_prob",
        color="CRM_tier",
        title="FES Score vs Churn Risk",
        hover_data=["family_id"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ROW 2 — Upgrade & Referral Propensity by Tier
# ============================================================

st.subheader("Upgrade & Referral Propensity by CRM Tier")

grouped = df.groupby("CRM_tier")[["upgrade_prob","referral_prob"]].mean().reset_index()
grouped_melt = grouped.melt(id_vars="CRM_tier")

fig = px.bar(
    grouped_melt,
    x="CRM_tier",
    y="value",
    color="variable",
    barmode="group"
)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ACTION BOARD
# ============================================================

st.subheader("Top 20 High Churn Risk Families")

top_risk = df.sort_values("churn_risk_prob", ascending=False).head(20)
st.dataframe(
    top_risk[[
        "family_id",
        "CRM_tier",
        "FES_score",
        "churn_risk_prob",
        "upgrade_prob",
        "referral_prob"
    ]],
    use_container_width=True
)
