import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="CareVeda CRM Dashboard", layout="wide")

@st.cache_data
def generate_data(n=700, seed=42):
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "family_id": [f"F{i:03d}" for i in range(1, n + 1)],
        "family_app_logins_week": rng.poisson(3, n).clip(0, 7),
        "months_active": rng.integers(1, 25, n),
        "caregiver_rating_avg": rng.normal(3.9, 0.6, n).clip(2.0, 5.0),
        "incidents_resolved_pct": rng.uniform(50, 100, n),
        "daily_report_opens": rng.uniform(20, 100, n),
        "upgrade_prob": rng.uniform(0, 1, n),
        "referral_prob": rng.uniform(0, 1, n),
    })

    # Behavioural churn logic (simple, interpretable)
    churn_raw = (
        (4.2 - df["caregiver_rating_avg"]) * 0.22 +
        (2.0 - df["family_app_logins_week"]) * 0.10 +
        (6.0 - df["months_active"]) * 0.05 +
        (70.0 - df["incidents_resolved_pct"]) * 0.012 +
        (50.0 - df["daily_report_opens"]) * 0.003
    )

    df["churn_risk_prob"] = churn_raw.clip(0, 1)

    # FES formula (same logic as earlier)
    df["FES_score"] = (
        (1 - df["churn_risk_prob"]) * 0.50 +
        df["upgrade_prob"] * 0.25 +
        df["referral_prob"] * 0.25
    ) * 100

    # CRM Tiering
    df["CRM_tier"] = "AMBER"
    df.loc[(df["churn_risk_prob"] >= 0.60) | (df["FES_score"] < 45), "CRM_tier"] = "RED"
    df.loc[(df["churn_risk_prob"] < 0.30) & (df["FES_score"] >= 65), "CRM_tier"] = "GREEN"

    return df

df = generate_data()

st.title("CareVeda Family Engagement Score Dashboard")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Families", f"{len(df):,}")
k2.metric("Avg FES", f"{df['FES_score'].mean():.1f}")
k3.metric("Avg Churn Risk", f"{df['churn_risk_prob'].mean():.2f}")
k4.metric("RED Tier %", f"{(df['CRM_tier'].eq('RED').mean()*100):.1f}%")

st.divider()

# Row 1
c1, c2 = st.columns(2)

with c1:
    tier_df = (
        df["CRM_tier"]
        .value_counts()
        .rename_axis("CRM_tier")
        .reset_index(name="count")
    )
    fig = px.bar(
        tier_df,
        x="CRM_tier",
        y="count",
        title="CRM Tier Distribution",
        labels={"CRM_tier": "Tier", "count": "Families"},
        text="count",
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.scatter(
        df,
        x="FES_score",
        y="churn_risk_prob",
        color="CRM_tier",
        title="FES Score vs Churn Risk",
        hover_data=["family_id", "months_active", "family_app_logins_week", "caregiver_rating_avg"],
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Row 2
st.subheader("Upgrade & Referral Propensity by CRM Tier")

grouped = df.groupby("CRM_tier", as_index=False)[["upgrade_prob", "referral_prob"]].mean()
melted = grouped.melt(id_vars="CRM_tier", var_name="metric", value_name="value")

fig = px.bar(
    melted,
    x="CRM_tier",
    y="value",
    color="metric",
    barmode="group",
    title="Average Upgrade vs Referral Probability",
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Action board
st.subheader("Top 20 High Churn Risk Families (CRM Action Board)")
top_risk = df.sort_values("churn_risk_prob", ascending=False).head(20)

st.dataframe(
    top_risk[[
        "family_id", "CRM_tier", "FES_score", "churn_risk_prob",
        "upgrade_prob", "referral_prob",
        "family_app_logins_week", "months_active", "caregiver_rating_avg",
        "incidents_resolved_pct", "daily_report_opens"
    ]],
    use_container_width=True,
    height=520
)
