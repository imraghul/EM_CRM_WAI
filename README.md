# CareVeda Intelligence Hub
### MBA WAI Project — Family Engagement CRM Dashboard

A fully self-contained Streamlit dashboard for **CareVeda**, an elderly in-home care subscription service. No external files, no uploads, no cloud storage — dataset is generated entirely inside the app.

---

## What It Does

Demonstrates a complete AI-powered CRM pipeline:

| Layer | Component | Purpose |
|---|---|---|
| Model A | Churn Prediction (XGBoost) | Identify families likely to cancel within 6 months |
| Model B | Upgrade Propensity (Logistic Regression) | Predict plan upgrade likelihood |
| Model C | Referral Likelihood (Random Forest) | Find families ready to refer others |
| Scoring | Family Engagement Score (FES) | Composite 0–100 score from all 3 models |
| Output | CRM Tiers (RED / AMBER / GREEN) | Operational segmentation + playbook actions |

---

## Dashboard Sections

1. **KPI Row** — Total families, Avg FES, Avg Churn Risk, RED%, GREEN%
2. **CRM Tier Distribution** — Bar chart of tier populations
3. **FES vs Churn Risk Scatter** — With dynamic threshold lines
4. **Lifecycle Cohort Analysis** — Tier breakdown by tenure stage
5. **Upgrade and Referral Propensity** — Model B and C outputs by tier
6. **SHAP-Style Feature Importance** — Radar + bar chart for Model A
7. **CRM Operational Playbook** — RED / AMBER / GREEN action cards
8. **Top 20 Action Board** — Sorted by churn risk with heat-mapped table
9. **Model Architecture Panel** — Visual pipeline + 4-card model breakdown

---

## Interactive Controls (Sidebar)

- **Churn Threshold Slider** — Move the RED tier boundary and see population shift live
- **Min FES Slider** — Adjust the FES floor for RED classification
- **Plan Filter** — Filter by Basic / Standard / Premium

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the entry point
4. Deploy — no secrets or environment variables needed

---

## Tech Stack

- **Streamlit** — Dashboard framework
- **Plotly** — All charts and visualisations
- **NumPy / Pandas** — Synthetic data generation and manipulation
- Fully self-contained, runs on Streamlit Cloud free tier
