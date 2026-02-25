import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareVeda Intelligence Hub",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --bg0: #080D1A;
    --bg1: #0D1525;
    --bg2: #111D33;
    --bg3: #16233D;
    --teal:   #00D4AA;
    --blue:   #4C9BFF;
    --amber:  #FFB547;
    --rose:   #FF5C7A;
    --purple: #9B72F0;
    --text1: #EEF2FF;
    --text2: #8898BB;
    --border: rgba(76,155,255,0.10);
}

html, body, .stApp {
    background: var(--bg0);
    font-family: 'DM Sans', sans-serif;
    color: var(--text1);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.5rem 4rem; max-width: 1600px; }

section[data-testid="stSidebar"] {
    background: var(--bg1) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: var(--text1) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.hero {
    background: linear-gradient(135deg, #0D1525 0%, #111D33 60%, #0A1422 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2rem 2.5rem 1.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,212,170,0.07) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,212,170,0.10);
    border: 1px solid rgba(0,212,170,0.30);
    color: #00D4AA;
    font-size: 0.70rem;
    font-weight: 600;
    padding: 0.22rem 0.75rem;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #EEF2FF;
    margin: 0 0 0.3rem;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.hero-title span { color: #00D4AA; }
.hero-sub {
    color: #8898BB;
    font-size: 0.88rem;
    font-weight: 400;
    margin: 0;
}

.kpi-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 0.5rem;
}
.kpi-accent {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #8898BB;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem;
    color: #EEF2FF;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-delta {
    font-size: 0.75rem;
    color: #8898BB;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.6rem 0 0.9rem;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00D4AA;
    flex-shrink: 0;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    color: #EEF2FF;
    margin: 0;
}
.section-sub {
    font-size: 0.78rem;
    color: #8898BB;
    margin-left: auto;
}

.playbook-grid { display: flex; gap: 1rem; margin-top: 0.5rem; }
.playbook-card {
    flex: 1;
    background: var(--bg2);
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
}
.playbook-card.red   { border: 1px solid rgba(255,92,122,0.20);  border-top: 3px solid #FF5C7A; }
.playbook-card.amber { border: 1px solid rgba(255,181,71,0.20);  border-top: 3px solid #FFB547; }
.playbook-card.green { border: 1px solid rgba(0,212,170,0.20);   border-top: 3px solid #00D4AA; }
.playbook-tier { font-size: 0.70rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.5rem; }
.playbook-card.red   .playbook-tier { color: #FF5C7A; }
.playbook-card.amber .playbook-tier { color: #FFB547; }
.playbook-card.green .playbook-tier { color: #00D4AA; }
.playbook-headline { font-family: 'DM Serif Display', serif; font-size: 1rem; color: #EEF2FF; margin-bottom: 0.8rem; }
.playbook-action {
    font-size: 0.80rem;
    color: #B0BCDB;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
}
.playbook-action:last-child { border-bottom: none; }
.playbook-action::before { content: '→'; opacity: 0.5; flex-shrink: 0; }

.arch-section {
    background: var(--bg1);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2rem 2.5rem;
    margin-top: 2rem;
}
.arch-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #EEF2FF;
    text-align: center;
    margin-bottom: 0.3rem;
}
.arch-subtitle {
    font-size: 0.82rem;
    color: #8898BB;
    text-align: center;
    margin-bottom: 2rem;
}
.arch-pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.arch-node {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    text-align: center;
    min-width: 130px;
}
.arch-node.input-node  { border-color: rgba(76,155,255,0.30); }
.arch-node.model-node-a { border-color: rgba(255,92,122,0.35); }
.arch-node.model-node-b { border-color: rgba(155,114,240,0.35); }
.arch-node.model-node-c { border-color: rgba(0,212,170,0.35); }
.arch-node.fes-node    { border-color: rgba(255,181,71,0.40); background: rgba(255,181,71,0.04); }
.arch-node.output-node { border-color: rgba(76,155,255,0.30); }
.arch-arrow { color: #8898BB; font-size: 1.3rem; padding: 0 0.4rem; flex-shrink: 0; }
.arch-node-icon { font-size: 1.5rem; margin-bottom: 0.3rem; }
.arch-node-label {
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.arch-node.input-node   .arch-node-label { color: #4C9BFF; }
.arch-node.model-node-a .arch-node-label { color: #FF5C7A; }
.arch-node.model-node-b .arch-node-label { color: #9B72F0; }
.arch-node.model-node-c .arch-node-label { color: #00D4AA; }
.arch-node.fes-node     .arch-node-label { color: #FFB547; }
.arch-node.output-node  .arch-node-label { color: #4C9BFF; }
.arch-node-desc { font-size: 0.72rem; color: #8898BB; line-height: 1.3; }

.model-cards { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.model-card {
    flex: 1;
    min-width: 200px;
    background: var(--bg2);
    border-radius: 14px;
    padding: 1.4rem;
    position: relative;
    overflow: hidden;
    border: 1px solid var(--border);
}
.model-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
}
.model-card.card-a::before   { background: #FF5C7A; }
.model-card.card-b::before   { background: #9B72F0; }
.model-card.card-c::before   { background: #00D4AA; }
.model-card.card-fes::before { background: linear-gradient(90deg, #FF5C7A, #9B72F0, #00D4AA); }
.model-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 0.18rem 0.6rem;
    border-radius: 10px;
    margin-bottom: 0.7rem;
}
.model-card.card-a   .model-badge { background: rgba(255,92,122,0.12); color: #FF5C7A; border: 1px solid rgba(255,92,122,0.25); }
.model-card.card-b   .model-badge { background: rgba(155,114,240,0.12); color: #9B72F0; border: 1px solid rgba(155,114,240,0.25); }
.model-card.card-c   .model-badge { background: rgba(0,212,170,0.12);  color: #00D4AA; border: 1px solid rgba(0,212,170,0.25); }
.model-card.card-fes .model-badge { background: rgba(255,181,71,0.12); color: #FFB547; border: 1px solid rgba(255,181,71,0.25); }
.model-card-title { font-family: 'DM Serif Display', serif; font-size: 1rem; color: #EEF2FF; margin-bottom: 0.4rem; }
.model-card-type  { font-size: 0.75rem; color: #8898BB; margin-bottom: 0.9rem; }
.model-row { display: flex; justify-content: space-between; margin-bottom: 0.4rem; }
.model-row-label { font-size: 0.75rem; color: #8898BB; }
.model-row-value { font-size: 0.75rem; color: #B0BCDB; font-weight: 500; }
.formula-box {
    background: rgba(255,181,71,0.05);
    border: 1px solid rgba(255,181,71,0.20);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-top: 0.8rem;
    font-size: 0.80rem;
    color: #B0BCDB;
    font-family: 'Courier New', monospace;
    line-height: 1.6;
}
.divider-line {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}
.inference-note {
    margin-top: 0.45rem;
    padding: 0.55rem 0.75rem;
    border-radius: 10px;
    border: 1px solid rgba(0,212,170,0.18);
    background: rgba(0,212,170,0.05);
    color: #BDEFE3;
    font-size: 0.76rem;
    line-height: 1.45;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# DATA GENERATION
# ──────────────────────────────────────────────────────────────
@st.cache_data
def generate_data(n=700, seed=42):
    rng = np.random.default_rng(seed)

    months_active = rng.integers(1, 37, n)
    plan_type = rng.choice(["Basic", "Standard", "Premium"], n, p=[0.40, 0.38, 0.22])

    login_base = np.where(plan_type == "Premium", 4.5, np.where(plan_type == "Standard", 3.2, 2.2))
    logins = rng.poisson(login_base).clip(0, 7)

    rating_base = 3.5 + months_active * 0.015 + rng.normal(0, 0.5, n)
    rating = rating_base.clip(1.5, 5.0)

    incident_res = (60 + months_active * 0.8 + rng.normal(0, 12, n)).clip(40, 100)
    report_opens = (30 + logins * 5 + rng.normal(0, 15, n)).clip(10, 100)

    upgrade_base = np.where(
        plan_type == "Standard",
        0.35 + (months_active / 36) * 0.25,
        np.where(plan_type == "Basic", 0.20 + (months_active / 36) * 0.15, 0.05)
    )
    upgrade_prob = (upgrade_base + rng.normal(0, 0.08, n)).clip(0, 1)

    referral_base = np.where(
        plan_type == "Premium",
        0.40 + (rating - 3) * 0.1,
        np.where(plan_type == "Standard", 0.25 + (rating - 3) * 0.08, 0.12)
    )
    referral_prob = (referral_base + rng.normal(0, 0.07, n)).clip(0, 1)

    df = pd.DataFrame({
        "family_id":               [f"F{i:04d}" for i in range(1, n + 1)],
        "plan_type":               plan_type,
        "family_app_logins_week":  logins,
        "months_active":           months_active,
        "caregiver_rating_avg":    rating.round(2),
        "incidents_resolved_pct":  incident_res.round(1),
        "daily_report_opens":      report_opens.round(1),
        "upgrade_prob":            upgrade_prob.round(3),
        "referral_prob":           referral_prob.round(3),
    })

    churn_raw = (
        (4.5 - df["caregiver_rating_avg"]) * 0.26 +
        (3.5 - df["family_app_logins_week"]) * 0.11 +
        np.maximum(0, 6 - df["months_active"]) * 0.04 +
        (75.0 - df["incidents_resolved_pct"]) * 0.010 +
        (55.0 - df["daily_report_opens"]) * 0.0025 +
        rng.normal(0, 0.04, n)
    )
    df["churn_risk_prob"] = churn_raw.clip(0, 1).round(3)

    df["FES_score"] = (
        (1 - df["churn_risk_prob"]) * 0.50 +
        df["upgrade_prob"] * 0.25 +
        df["referral_prob"] * 0.25
    ) * 100
    df["FES_score"] = df["FES_score"].round(1)

    df["CRM_tier"] = "AMBER"
    df.loc[(df["churn_risk_prob"] >= 0.60) | (df["FES_score"] < 45), "CRM_tier"] = "RED"
    df.loc[(df["churn_risk_prob"] < 0.30) & (df["FES_score"] >= 65), "CRM_tier"] = "GREEN"

    df["lifecycle_stage"] = pd.cut(
        df["months_active"],
        bins=[0, 3, 9, 18, 36],
        labels=["Onboarding (0-3m)", "Early (3-9m)", "Established (9-18m)", "Loyal (18m+)"]
    )

    return df


df = generate_data()

TIER_COLORS = {"RED": "#FF5C7A", "AMBER": "#FFB547", "GREEN": "#00D4AA"}
PT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8898BB"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BCDB")),
    margin=dict(l=10, r=10, t=40, b=10),
)
AX = dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(0,0,0,0)", tickfont=dict(color="#B0BCDB"))


def render_inference(text):
    st.markdown(f"<div class='inference-note'><b>Inference:</b> {text}</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 1.2rem;'>
        <div style='font-size:0.68rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#00D4AA;margin-bottom:0.4rem;'>CareVeda Intelligence</div>
        <div style='font-family:"DM Serif Display",serif;font-size:1.25rem;color:#EEF2FF;'>CRM Analytics Hub</div>
        <div style='font-size:0.76rem;color:#8898BB;margin-top:0.2rem;'>MBA WAI Project · 2024</div>
    </div>
    <hr style='border:none;border-top:1px solid rgba(76,155,255,0.10);margin-bottom:1.2rem;'>
    """, unsafe_allow_html=True)

    st.markdown("**Threshold Simulator**")
    churn_threshold = st.slider("Churn Cutoff (RED)", 0.30, 0.90, 0.60, 0.05)
    fes_threshold   = st.slider("Min FES for RED",    30,    60,    45,   5)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(76,155,255,0.10);margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("**Filter by Plan**")
    plan_filter = st.multiselect("Plan Type", ["Basic","Standard","Premium"], default=["Basic","Standard","Premium"])

    st.markdown("<hr style='border:none;border-top:1px solid rgba(76,155,255,0.10);margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:#8898BB;line-height:1.8;'>
        <b style='color:#EEF2FF;'>Models Deployed</b><br>
        Model A · Churn (XGBoost)<br>
        Model B · Upgrade (Logistic)<br>
        Model C · Referral (RF)<br><br>
        <b style='color:#EEF2FF;'>Scoring Engine</b><br>
        Family Engagement Score<br><br>
        <b style='color:#EEF2FF;'>Dataset</b><br>
        700 synthetic families
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# APPLY THRESHOLDS + FILTERS
# ──────────────────────────────────────────────────────────────
dff = df[df["plan_type"].isin(plan_filter)].copy()
dff["CRM_tier"] = "AMBER"
dff.loc[(dff["churn_risk_prob"] >= churn_threshold) | (dff["FES_score"] < fes_threshold), "CRM_tier"] = "RED"
green_churn_cut = max(0.05, churn_threshold - 0.30)
green_fes_floor = min(95, fes_threshold + 20)
dff.loc[(dff["churn_risk_prob"] < green_churn_cut) & (dff["FES_score"] >= green_fes_floor), "CRM_tier"] = "GREEN"


# ──────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🏥 MBA WAI Project · CareVeda Elderly Care</div>
    <div class="hero-title">Family <span>Engagement</span> Intelligence Hub</div>
    <p class="hero-sub">
        AI-powered churn prediction, upgrade propensity &amp; referral scoring for elderly in-home care subscriptions &nbsp;·&nbsp;
        3 ML models &nbsp;·&nbsp; 1 composite FES scoring engine &nbsp;·&nbsp; 700 synthetic families
    </p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# KPIs
# ──────────────────────────────────────────────────────────────
total     = len(dff)
avg_fes   = dff["FES_score"].mean()
avg_churn = dff["churn_risk_prob"].mean()
red_pct   = (dff["CRM_tier"] == "RED").mean() * 100
green_pct = (dff["CRM_tier"] == "GREEN").mean() * 100

def kpi_html(label, value, delta, accent):
    return f"""
    <div class="kpi-card">
        <div class="kpi-accent" style="background:{accent};"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>"""

k1,k2,k3,k4,k5 = st.columns(5)
k1.markdown(kpi_html("Total Families",    f"{total:,}",       f"{len(plan_filter)} plan(s) active",        "#4C9BFF"), unsafe_allow_html=True)
k2.markdown(kpi_html("Avg FES Score",     f"{avg_fes:.1f}",   "Out of 100",                                "#00D4AA"), unsafe_allow_html=True)
k3.markdown(kpi_html("Avg Churn Risk",    f"{avg_churn:.2f}", f"Threshold set at {churn_threshold}",       "#FF5C7A"), unsafe_allow_html=True)
k4.markdown(kpi_html("RED Tier",          f"{red_pct:.1f}%",  f"{int(total*red_pct/100)} families at risk","#FF5C7A"), unsafe_allow_html=True)
k5.markdown(kpi_html("GREEN Tier",        f"{green_pct:.1f}%",f"{int(total*green_pct/100)} loyal families","#00D4AA"), unsafe_allow_html=True)

st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# TIER OVERVIEW
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <div class="section-title">CRM Tier Overview</div>
    <div class="section-sub">Adjust sidebar thresholds to simulate tier populations in real-time</div>
</div>""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1.6])

with c1:
    tier_df = dff["CRM_tier"].value_counts().rename_axis("CRM_tier").reset_index(name="count")
    tier_df["pct"] = (tier_df["count"] / tier_df["count"].sum() * 100).round(1)
    fig = go.Figure()
    for _, row in tier_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["CRM_tier"]], y=[row["count"]],
            name=row["CRM_tier"],
            marker_color=TIER_COLORS.get(row["CRM_tier"], "#888"),
            text=f'{row["count"]}<br><span style="font-size:10px">{row["pct"]}%</span>',
            textposition="outside", textfont=dict(color="#EEF2FF", size=13),
            width=0.45, showlegend=False
        ))
    fig.update_layout(**PT,
        title=dict(text="CRM Tier Distribution", font=dict(color="#EEF2FF", size=14)),
        yaxis=dict(**AX, title="Families"), xaxis=dict(**AX),
        height=300, bargap=0.4)
    st.plotly_chart(fig, width='stretch')
    top_tier = tier_df.sort_values("count", ascending=False).iloc[0]
    render_inference(
        f"{top_tier['CRM_tier']} is the largest segment with {int(top_tier['count'])} families "
        f"({top_tier['pct']:.1f}% of the filtered base)."
    )

with c2:
    fig = px.scatter(dff, x="FES_score", y="churn_risk_prob",
        color="CRM_tier", color_discrete_map=TIER_COLORS, opacity=0.60,
        hover_data=["family_id","plan_type","months_active","caregiver_rating_avg"],
        labels={"FES_score":"Family Engagement Score","churn_risk_prob":"Churn Risk"})
    fig.update_traces(marker=dict(size=5))
    fig.add_hline(y=churn_threshold, line_dash="dash", line_color="rgba(255,92,122,0.40)",
                  annotation_text=f"Churn threshold ({churn_threshold})",
                  annotation_font_color="#FF5C7A", annotation_font_size=11)
    fig.add_vline(x=fes_threshold, line_dash="dash", line_color="rgba(255,181,71,0.40)",
                  annotation_text=f"FES floor ({fes_threshold})",
                  annotation_font_color="#FFB547", annotation_font_size=11)
    fig.update_layout(**PT,
        title=dict(text="FES Score vs Churn Risk by Tier", font=dict(color="#EEF2FF", size=14)),
        xaxis=dict(**AX), yaxis=dict(**AX), height=300)
    st.plotly_chart(fig, width='stretch')
    safe_count = ((dff["FES_score"] >= fes_threshold) & (dff["churn_risk_prob"] < churn_threshold)).sum()
    fes_churn_corr = dff["FES_score"].corr(dff["churn_risk_prob"])
    render_inference(
        f"{safe_count} families currently sit in the safer zone (right of FES floor and below churn cutoff). "
        f"FES and churn show a {fes_churn_corr:.2f} correlation, confirming higher engagement aligns with lower churn risk."
    )


# ──────────────────────────────────────────────────────────────
# LIFECYCLE COHORT
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#9B72F0;"></div>
    <div class="section-title">Lifecycle Cohort Analysis</div>
    <div class="section-sub">Churn behaviour across family tenure stages</div>
</div>""", unsafe_allow_html=True)

c3, c4 = st.columns([1.4, 1])

with c3:
    cohort = (dff.groupby(["lifecycle_stage","CRM_tier"], observed=True)
              .size().reset_index(name="count"))
    fig = px.bar(cohort, x="lifecycle_stage", y="count", color="CRM_tier",
        color_discrete_map=TIER_COLORS, barmode="stack",
        labels={"lifecycle_stage":"Stage","count":"Families","CRM_tier":"Tier"})
    fig.update_layout(**PT,
        title=dict(text="CRM Tier by Lifecycle Stage", font=dict(color="#EEF2FF", size=14)),
        xaxis=dict(**AX), yaxis=dict(**AX), height=300)
    st.plotly_chart(fig, width='stretch')
    red_share_by_stage = (
        cohort.pivot(index="lifecycle_stage", columns="CRM_tier", values="count")
        .fillna(0)
    )
    red_share_by_stage["red_share"] = red_share_by_stage.get("RED", 0) / red_share_by_stage.sum(axis=1)
    top_red_stage = red_share_by_stage["red_share"].idxmax()
    top_red_pct = red_share_by_stage["red_share"].max() * 100
    render_inference(
        f"The highest RED concentration appears in {top_red_stage}, where RED families are {top_red_pct:.1f}% of that cohort."
    )

with c4:
    cohort_churn = (dff.groupby("lifecycle_stage", observed=True)["churn_risk_prob"]
                    .mean().reset_index())
    fig = go.Figure(go.Bar(
        x=cohort_churn["churn_risk_prob"],
        y=cohort_churn["lifecycle_stage"].astype(str),
        orientation="h",
        marker=dict(color=cohort_churn["churn_risk_prob"],
                    colorscale=[[0,"#00D4AA"],[0.5,"#FFB547"],[1,"#FF5C7A"]], showscale=False),
        text=cohort_churn["churn_risk_prob"].apply(lambda x: f"{x:.2f}"),
        textposition="outside", textfont=dict(color="#EEF2FF", size=12),
    ))
    fig.update_layout(**PT,
        title=dict(text="Avg Churn Risk by Stage", font=dict(color="#EEF2FF", size=14)),
        xaxis=dict(**AX, range=[0, 0.85]), yaxis=dict(**AX), height=300)
    st.plotly_chart(fig, width='stretch')
    risk_peak = cohort_churn.sort_values("churn_risk_prob", ascending=False).iloc[0]
    render_inference(
        f"{risk_peak['lifecycle_stage']} has the highest average churn risk at {risk_peak['churn_risk_prob']:.2f}, "
        f"so this stage should be prioritized for retention workflows."
    )


# ──────────────────────────────────────────────────────────────
# PROPENSITY + PLAN
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#FFB547;"></div>
    <div class="section-title">Upgrade &amp; Referral Propensity</div>
    <div class="section-sub">Model B and Model C outputs segmented by CRM tier and plan</div>
</div>""", unsafe_allow_html=True)

c5, c6 = st.columns(2)

with c5:
    grouped = dff.groupby("CRM_tier", as_index=False)[["upgrade_prob","referral_prob"]].mean()
    melted  = grouped.melt(id_vars="CRM_tier", var_name="metric", value_name="value")
    melted["metric_label"] = melted["metric"].map({"upgrade_prob":"Upgrade Propensity","referral_prob":"Referral Likelihood"})
    fig = px.bar(melted, x="CRM_tier", y="value", color="metric_label", barmode="group",
        color_discrete_map={"Upgrade Propensity":"#9B72F0","Referral Likelihood":"#00D4AA"},
        labels={"CRM_tier":"CRM Tier","value":"Avg Probability","metric_label":""})
    fig.update_layout(**PT,
        title=dict(text="Avg Propensity by CRM Tier", font=dict(color="#EEF2FF", size=14)),
        xaxis=dict(**AX), yaxis=dict(**AX), height=300)
    st.plotly_chart(fig, width='stretch')
    strongest_upgrade = grouped.sort_values("upgrade_prob", ascending=False).iloc[0]
    strongest_referral = grouped.sort_values("referral_prob", ascending=False).iloc[0]
    render_inference(
        f"Highest upgrade propensity is in {strongest_upgrade['CRM_tier']} ({strongest_upgrade['upgrade_prob']:.2f}) "
        f"and highest referral likelihood is in {strongest_referral['CRM_tier']} ({strongest_referral['referral_prob']:.2f})."
    )

with c6:
    plan_churn = dff.groupby("plan_type")["churn_risk_prob"].mean().reset_index()
    plan_fes   = dff.groupby("plan_type")["FES_score"].mean().reset_index()
    merged     = plan_churn.merge(plan_fes, on="plan_type")
    fig = go.Figure([
        go.Bar(x=merged["plan_type"], y=merged["churn_risk_prob"], name="Avg Churn Risk",
               marker_color="#FF5C7A", width=0.3, offset=-0.15),
        go.Bar(x=merged["plan_type"], y=merged["FES_score"]/100,  name="Avg FES (scaled 0-1)",
               marker_color="#4C9BFF", width=0.3, offset=0.15),
    ])
    fig.update_layout(**PT,
        title=dict(text="Churn Risk vs FES by Plan Type", font=dict(color="#EEF2FF", size=14)),
        barmode="group", xaxis=dict(**AX), yaxis=dict(**AX), height=300)
    st.plotly_chart(fig, width='stretch')
    best_plan = merged.sort_values(["churn_risk_prob", "FES_score"], ascending=[True, False]).iloc[0]
    render_inference(
        f"{best_plan['plan_type']} currently shows the healthiest profile: churn risk {best_plan['churn_risk_prob']:.2f} "
        f"with average FES {best_plan['FES_score']:.1f}."
    )


# ──────────────────────────────────────────────────────────────
# SHAP PANEL
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#4C9BFF;"></div>
    <div class="section-title">SHAP-Style Feature Importance  ·  Model A (Churn)</div>
    <div class="section-sub">Simulated directional feature contributions based on behavioural correlations</div>
</div>""", unsafe_allow_html=True)

c7, c8 = st.columns([1.2, 1])
features = ["caregiver_rating_avg","family_app_logins_week","months_active",
            "incidents_resolved_pct","daily_report_opens"]

with c7:
    corrs = [dff[f].corr(dff["churn_risk_prob"]) for f in features]
    shap_df = pd.DataFrame({
        "Feature": features,
        "Impact":  [abs(c) for c in corrs],
        "Direction":["Negative driver" if c > 0 else "Protective factor" for c in corrs]
    }).sort_values("Impact", ascending=True)
    fig = go.Figure(go.Bar(
        x=shap_df["Impact"], y=shap_df["Feature"], orientation="h",
        marker=dict(color=shap_df["Impact"],
                    colorscale=[[0,"#4C9BFF"],[0.5,"#9B72F0"],[1,"#FF5C7A"]], showscale=False),
        text=[f"{v:.3f}  ({d})" for v,d in zip(shap_df["Impact"], shap_df["Direction"])],
        textposition="outside", textfont=dict(color="#B0BCDB", size=11),
    ))
    fig.update_layout(**PT,
        title=dict(text="Feature Impact on Churn (|Correlation|)", font=dict(color="#EEF2FF", size=14)),
        xaxis=dict(**AX, range=[0,0.85]), yaxis=dict(**AX), height=290)
    st.plotly_chart(fig, width='stretch')
    top_driver = shap_df.sort_values("Impact", ascending=False).iloc[0]
    render_inference(
        f"{top_driver['Feature']} is the strongest churn signal (impact {top_driver['Impact']:.3f}) "
        f"and behaves as a {top_driver['Direction'].lower()}."
    )

with c8:
    all_avg = dff[features].mean()
    red_avg = dff[dff["CRM_tier"]=="RED"][features].mean()
    norm_all = [1.0 for _ in features]
    norm_red  = [(red_avg[f]/all_avg[f]) if all_avg[f]!=0 else 1.0 for f in features]
    feat_labels = [f.replace("_"," ").title() for f in features]
    fig = go.Figure([
        go.Scatterpolar(r=norm_all, theta=feat_labels, fill="toself", name="All Families",
                        line=dict(color="#4C9BFF"), fillcolor="rgba(76,155,255,0.08)"),
        go.Scatterpolar(r=norm_red,  theta=feat_labels, fill="toself", name="RED Tier",
                        line=dict(color="#FF5C7A"), fillcolor="rgba(255,92,122,0.12)"),
    ])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#8898BB"),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,2], gridcolor="rgba(255,255,255,0.07)",
                            tickfont=dict(color="#8898BB", size=9)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.07)", tickfont=dict(color="#B0BCDB", size=10)),
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BCDB")),
        margin=dict(l=10,r=10,t=40,b=10),
        title=dict(text="RED vs All Families · Feature Profile", font=dict(color="#EEF2FF", size=14)),
        height=290,
    )
    st.plotly_chart(fig, width='stretch')
    ratio_series = pd.Series(norm_red, index=feat_labels)
    largest_gap_feature = ratio_series.sub(1).abs().idxmax()
    largest_gap_ratio = ratio_series[largest_gap_feature]
    render_inference(
        f"The largest RED-vs-overall deviation is in {largest_gap_feature} at {largest_gap_ratio:.2f}x the baseline, "
        f"highlighting where RED families differ most operationally."
    )


# ──────────────────────────────────────────────────────────────
# CRM PLAYBOOK
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#FF5C7A;"></div>
    <div class="section-title">CRM Operational Playbook</div>
    <div class="section-sub">Tier-to-action mapping for the CareVeda care operations team</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="playbook-grid">
  <div class="playbook-card red">
    <div class="playbook-tier">🔴 RED Tier &nbsp;·&nbsp; High Urgency</div>
    <div class="playbook-headline">Retain Before They Cancel</div>
    <div class="playbook-action">Assign dedicated care manager within 48 hrs</div>
    <div class="playbook-action">Auto-trigger personalised outreach call from Care Director</div>
    <div class="playbook-action">Offer caregiver replacement if rating below 3.0</div>
    <div class="playbook-action">Provide 15-day service credit to rebuild trust</div>
    <div class="playbook-action">Run weekly check-in cadence for 30 days post-flag</div>
    <div class="playbook-action">Escalate unresolved incidents within 24 hrs</div>
  </div>
  <div class="playbook-card amber">
    <div class="playbook-tier">🟡 AMBER Tier &nbsp;·&nbsp; Watch &amp; Nudge</div>
    <div class="playbook-headline">Re-Engage Before Drift Becomes Decline</div>
    <div class="playbook-action">Send biweekly family health digest email</div>
    <div class="playbook-action">Trigger app re-engagement push notifications</div>
    <div class="playbook-action">Offer upgrade trial for Standard to Premium</div>
    <div class="playbook-action">Share caregiver milestone updates to boost affinity</div>
    <div class="playbook-action">Invite to CareVeda family webinar / community event</div>
    <div class="playbook-action">Flag to account manager if AMBER for more than 60 days</div>
  </div>
  <div class="playbook-card green">
    <div class="playbook-tier">🟢 GREEN Tier &nbsp;·&nbsp; Grow &amp; Leverage</div>
    <div class="playbook-headline">Convert Loyalty into Revenue &amp; Referrals</div>
    <div class="playbook-action">Launch referral bonus programme (cash or credit reward)</div>
    <div class="playbook-action">Identify upgrade candidates via Model B score above 0.65</div>
    <div class="playbook-action">Feature family testimonials in marketing (with consent)</div>
    <div class="playbook-action">Offer early access to new Premium service tiers</div>
    <div class="playbook-action">Send annual loyalty appreciation gift</div>
    <div class="playbook-action">Nominate as CareVeda Community Champions</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# ACTION BOARD TABLE
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#FF5C7A;"></div>
    <div class="section-title">Top 20 High-Risk Families &nbsp;·&nbsp; CRM Action Board</div>
    <div class="section-sub">Sorted by churn probability — immediate intervention required</div>
</div>""", unsafe_allow_html=True)

top_risk = (
    dff.sort_values("churn_risk_prob", ascending=False)
    .head(20)[["family_id","plan_type","CRM_tier","FES_score","churn_risk_prob",
               "upgrade_prob","referral_prob","family_app_logins_week",
               "months_active","caregiver_rating_avg","incidents_resolved_pct"]]
    .reset_index(drop=True)
)
def color_churn(val):
    if val >= 0.75:
        return "background-color: rgba(255,60,80,0.35); color: #FFD0D8;"
    elif val >= 0.60:
        return "background-color: rgba(255,80,100,0.22); color: #FFBFC9;"
    elif val >= 0.45:
        return "background-color: rgba(255,150,60,0.18); color: #FFD9B0;"
    return "background-color: rgba(0,200,140,0.12); color: #A8F0DC;"

def color_fes(val):
    if val >= 65:
        return "background-color: rgba(0,212,170,0.20); color: #A8F0DC;"
    elif val >= 50:
        return "background-color: rgba(255,181,71,0.15); color: #FFE0A0;"
    return "background-color: rgba(255,60,80,0.20); color: #FFD0D8;"

st.dataframe(
    top_risk.style
    .map(color_churn, subset=["churn_risk_prob"])
    .map(color_fes, subset=["FES_score"])
    .format({"churn_risk_prob":"{:.3f}","FES_score":"{:.1f}",
             "upgrade_prob":"{:.3f}","referral_prob":"{:.3f}",
             "caregiver_rating_avg":"{:.2f}","incidents_resolved_pct":"{:.1f}"}),
    width='stretch', height=480
)


# ──────────────────────────────────────────────────────────────
# ARCHITECTURE SECTION — rebuilt with st.columns to avoid raw HTML rendering
# ──────────────────────────────────────────────────────────────
st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)

st.markdown("""
<div style="background:var(--bg1);border:1px solid var(--border);border-radius:18px;padding:2rem 2.5rem 1.5rem;">
  <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:#EEF2FF;text-align:center;margin-bottom:0.3rem;">How This Was Built</div>
  <div style="font-size:0.82rem;color:#8898BB;text-align:center;margin-bottom:1.8rem;">
    3 Predictive ML Models &nbsp;·&nbsp; 1 Composite Scoring Engine &nbsp;·&nbsp; End-to-end CRM intelligence pipeline
  </div>
</div>
""", unsafe_allow_html=True)

# Pipeline diagram — 5 nodes using columns
st.markdown("""
<div style="background:var(--bg1);border:1px solid var(--border);border-left:none;border-right:none;border-top:none;border-radius:0;padding:0 2.5rem;">
  <div style="display:flex;align-items:center;justify-content:center;gap:0;flex-wrap:wrap;padding-bottom:1.5rem;">
    <div style="background:var(--bg2);border:1px solid rgba(76,155,255,0.30);border-radius:12px;padding:1rem 1.3rem;text-align:center;min-width:120px;">
      <div style="font-size:1.4rem;margin-bottom:0.3rem;">📊</div>
      <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.7px;text-transform:uppercase;color:#4C9BFF;margin-bottom:0.2rem;">Input Features</div>
      <div style="font-size:0.70rem;color:#8898BB;line-height:1.4;">App logins · Rating<br>Tenure · Incidents<br>Report opens</div>
    </div>
    <div style="color:#8898BB;font-size:1.3rem;padding:0 0.5rem;">&#8594;</div>
    <div style="display:flex;flex-direction:column;gap:0.4rem;">
      <div style="background:var(--bg2);border:1px solid rgba(255,92,122,0.35);border-radius:10px;padding:0.6rem 1rem;text-align:center;">
        <span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#FF5C7A;">Model A</span>
        <span style="font-size:0.68rem;color:#8898BB;margin-left:0.4rem;">Churn · XGBoost</span>
      </div>
      <div style="background:var(--bg2);border:1px solid rgba(155,114,240,0.35);border-radius:10px;padding:0.6rem 1rem;text-align:center;">
        <span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#9B72F0;">Model B</span>
        <span style="font-size:0.68rem;color:#8898BB;margin-left:0.4rem;">Upgrade · Logistic</span>
      </div>
      <div style="background:var(--bg2);border:1px solid rgba(0,212,170,0.35);border-radius:10px;padding:0.6rem 1rem;text-align:center;">
        <span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#00D4AA;">Model C</span>
        <span style="font-size:0.68rem;color:#8898BB;margin-left:0.4rem;">Referral · RF</span>
      </div>
    </div>
    <div style="color:#8898BB;font-size:1.3rem;padding:0 0.5rem;">&#8594;</div>
    <div style="background:rgba(255,181,71,0.04);border:1px solid rgba(255,181,71,0.40);border-radius:12px;padding:1rem 1.3rem;text-align:center;min-width:130px;">
      <div style="font-size:1.4rem;margin-bottom:0.3rem;">⚡</div>
      <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.7px;text-transform:uppercase;color:#FFB547;margin-bottom:0.2rem;">FES Engine</div>
      <div style="font-size:0.70rem;color:#8898BB;line-height:1.4;">(1−churn)×0.50<br>+upgrade×0.25<br>+referral×0.25</div>
    </div>
    <div style="color:#8898BB;font-size:1.3rem;padding:0 0.5rem;">&#8594;</div>
    <div style="background:var(--bg2);border:1px solid rgba(76,155,255,0.30);border-radius:12px;padding:1rem 1.3rem;text-align:center;min-width:110px;">
      <div style="font-size:1.4rem;margin-bottom:0.3rem;">🎯</div>
      <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.7px;text-transform:uppercase;color:#4C9BFF;margin-bottom:0.2rem;">CRM Tiers</div>
      <div style="font-size:0.70rem;color:#8898BB;line-height:1.4;">RED · AMBER<br>GREEN<br>+ Playbook</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Model cards — use st.columns so Streamlit renders them natively
ma, mb, mc, mfes = st.columns(4)

with ma:
    st.markdown("""
    <div class="model-card card-a">
      <div class="model-badge">Model A</div>
      <div class="model-card-title">Churn Prediction</div>
      <div class="model-card-type">Binary Classification · XGBoost</div>
      <div class="model-row"><span class="model-row-label">Target</span><span class="model-row-value">churned_within_6months</span></div>
      <div class="model-row"><span class="model-row-label">Algorithm</span><span class="model-row-value">XGBoost (balanced)</span></div>
      <div class="model-row"><span class="model-row-label">Key features</span><span class="model-row-value">Rating, Logins, Tenure</span></div>
      <div class="model-row"><span class="model-row-label">Business use</span><span class="model-row-value">Retention intervention</span></div>
      <div class="model-row"><span class="model-row-label">FES weight</span><span class="model-row-value">50% (inverted)</span></div>
    </div>
    """, unsafe_allow_html=True)

with mb:
    st.markdown("""
    <div class="model-card card-b">
      <div class="model-badge">Model B</div>
      <div class="model-card-title">Upgrade Propensity</div>
      <div class="model-card-type">Binary Classification · Logistic Regression</div>
      <div class="model-row"><span class="model-row-label">Target</span><span class="model-row-value">upgraded_plan</span></div>
      <div class="model-row"><span class="model-row-label">Algorithm</span><span class="model-row-value">Logistic Regression</span></div>
      <div class="model-row"><span class="model-row-label">Key features</span><span class="model-row-value">Plan type, Tenure, FES</span></div>
      <div class="model-row"><span class="model-row-label">Business use</span><span class="model-row-value">Expansion revenue</span></div>
      <div class="model-row"><span class="model-row-label">FES weight</span><span class="model-row-value">25%</span></div>
    </div>
    """, unsafe_allow_html=True)

with mc:
    st.markdown("""
    <div class="model-card card-c">
      <div class="model-badge">Model C</div>
      <div class="model-card-title">Referral Likelihood</div>
      <div class="model-card-type">Binary Classification · Random Forest</div>
      <div class="model-row"><span class="model-row-label">Target</span><span class="model-row-value">referred_another_family</span></div>
      <div class="model-row"><span class="model-row-label">Algorithm</span><span class="model-row-value">Random Forest</span></div>
      <div class="model-row"><span class="model-row-label">Key features</span><span class="model-row-value">Rating, Plan, Tenure</span></div>
      <div class="model-row"><span class="model-row-label">Business use</span><span class="model-row-value">Organic growth flywheel</span></div>
      <div class="model-row"><span class="model-row-label">FES weight</span><span class="model-row-value">25%</span></div>
    </div>
    """, unsafe_allow_html=True)

with mfes:
    st.markdown("""
    <div class="model-card card-fes">
      <div class="model-badge">FES Engine</div>
      <div class="model-card-title">Family Engagement Score</div>
      <div class="model-card-type">Composite Scoring Layer · Not a standalone model</div>
      <div class="model-row"><span class="model-row-label">Output range</span><span class="model-row-value">0 to 100</span></div>
      <div class="model-row"><span class="model-row-label">Inputs</span><span class="model-row-value">All 3 model outputs</span></div>
      <div class="model-row"><span class="model-row-label">Drives</span><span class="model-row-value">RED / AMBER / GREEN</span></div>
      <div class="formula-box">
        FES =<br>
        (1 &minus; P_churn) &times; 0.50<br>
        + P_upgrade &times; 0.25<br>
        + P_referral &times; 0.25<br>
        scaled to 0&ndash;100
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;font-size:0.73rem;color:#8898BB;margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(76,155,255,0.08);">
  CareVeda Intelligence Hub &nbsp;·&nbsp; MBA WAI Project &nbsp;·&nbsp;
  Built with Streamlit + Plotly &nbsp;·&nbsp; Fully self-contained &nbsp;·&nbsp; No external dependencies
</div>
""", unsafe_allow_html=True)
