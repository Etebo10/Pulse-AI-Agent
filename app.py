import streamlit as st
import json
from pulse_agent import analyse

st.set_page_config(page_title="Pulse — Business Intelligence", page_icon="◆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

:root {
  --ink:      #0e0e0e;
  --ink2:     #2a2a2a;
  --ink3:     #555;
  --paper:    #f5f2eb;
  --paper2:   #ede9df;
  --paper3:   #e4dfd3;
  --emerald:  #006644;
  --em-light: #e6f2ee;
  --em-mid:   #009960;
  --amber:    #b45309;
  --red:      #991b1b;
  --grid:     rgba(14,14,14,0.07);
  --mono:     'IBM Plex Mono', monospace;
}

* { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'Lato', sans-serif;
  background: var(--paper) !important;
  color: var(--ink);
}

/* ── GRID BACKGROUND ── */
[data-testid="stAppViewContainer"] {
  background:
    linear-gradient(var(--grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid) 1px, transparent 1px),
    var(--paper) !important;
  background-size: 48px 48px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--ink) !important;
  border-right: none !important;
}
[data-testid="stSidebar"] * { color: #d4d0c8 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong { color: #f5f2eb !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: #1c1c1c !important;
  border: 1px solid #333 !important;
  color: #f5f2eb !important;
  border-radius: 4px !important;
  font-family: var(--mono) !important;
  font-size: 11px !important;
}
[data-testid="stSidebar"] .stTextArea textarea {
  background: #1c1c1c !important;
  border: 1px solid #333 !important;
  color: #d4d0c8 !important;
  border-radius: 4px !important;
  font-family: 'Lato', sans-serif !important;
  font-size: 13px !important;
  line-height: 1.6 !important;
}
[data-testid="stSidebar"] .stButton > button {
  background: var(--emerald) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 4px !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 1.1rem !important;
  letter-spacing: 0.12em !important;
  padding: 0.6rem 1.5rem !important;
  width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background: #005236 !important; }
[data-testid="stSidebar"] hr { border-color: #2a2a2a !important; }

/* ── MAIN BUTTONS ── */
.stButton > button {
  background: var(--ink) !important;
  color: var(--paper) !important;
  border: none !important;
  border-radius: 4px !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 1.1rem !important;
  letter-spacing: 0.12em !important;
  padding: 0.55rem 2rem !important;
  transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.82 !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
  background: transparent !important;
  color: var(--emerald) !important;
  border: 1.5px solid var(--emerald) !important;
  border-radius: 4px !important;
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 1rem !important;
  letter-spacing: 0.1em !important;
}

/* ── MASTHEAD ── */
.masthead {
  border-bottom: 3px solid var(--ink);
  padding: 2rem 0 1rem;
  margin-bottom: 0;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}
.masthead-left { display: flex; align-items: flex-end; gap: 16px; }
.masthead-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 5rem;
  color: var(--ink);
  letter-spacing: 0.04em;
  line-height: 0.9;
  margin: 0;
}
.masthead-rule {
  width: 3px;
  height: 64px;
  background: var(--emerald);
  margin-bottom: 4px;
}
.masthead-meta {
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--ink3);
  line-height: 1.8;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 6px;
}
.masthead-tagline {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 0.85rem;
  color: var(--ink3);
  text-align: right;
  margin-bottom: 6px;
}

/* ── TICKER BAR ── */
.ticker-bar {
  background: var(--ink);
  color: #f5f2eb;
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.06em;
  padding: 6px 16px;
  display: flex;
  gap: 32px;
  align-items: center;
  margin-bottom: 2rem;
  overflow: hidden;
}
.ticker-item { white-space: nowrap; }
.ticker-item .up   { color: #4ade80; }
.ticker-item .down { color: #f87171; }
.ticker-item .flat { color: #94a3b8; }

/* ── HEALTH SCORE ── */
.health-block {
  background: var(--ink);
  color: var(--paper);
  padding: 2rem 2.5rem;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
  margin-bottom: 2px;
}
.health-score-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 7rem;
  line-height: 1;
  color: var(--paper);
  letter-spacing: -0.02em;
}
.health-score-label {
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 4px;
}
.health-badge {
  display: inline-block;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.4rem;
  letter-spacing: 0.1em;
  padding: 4px 14px;
  border-radius: 2px;
  margin-top: 8px;
}
.badge-thriving  { background: #006644; color: #fff; }
.badge-healthy   { background: #059669; color: #fff; }
.badge-stable    { background: #b45309; color: #fff; }
.badge-at-risk   { background: #dc2626; color: #fff; }
.badge-critical  { background: #7f1d1d; color: #fff; }

/* ── SECTION HEADERS ── */
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 2px solid var(--ink);
  padding-top: 10px;
  margin: 2rem 0 1rem;
}
.section-header .section-num {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--ink3);
  letter-spacing: 0.1em;
}
.section-header .section-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.3rem;
  letter-spacing: 0.1em;
  color: var(--ink);
  margin: 0;
}
.section-header .section-icon {
  color: var(--emerald);
  font-size: 0.9rem;
}

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 2px; margin-bottom: 2px; }
.kpi-card {
  background: var(--paper2);
  border-top: 3px solid var(--ink);
  padding: 1rem 1.1rem 1.1rem;
  position: relative;
}
.kpi-card:hover { background: var(--paper3); }
.kpi-label { font-family: var(--mono); font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--ink3); margin-bottom: 4px; }
.kpi-value { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: var(--ink); line-height: 1; letter-spacing: 0.02em; }
.kpi-change {
  font-family: var(--mono);
  font-size: 0.72rem;
  font-weight: 500;
  margin-top: 4px;
}
.kpi-change.up   { color: var(--emerald); }
.kpi-change.down { color: var(--red); }
.kpi-change.flat { color: var(--ink3); }
.kpi-insight { font-size: 0.75rem; color: var(--ink3); margin-top: 6px; line-height: 1.4; font-style: italic; }
.kpi-trend-icon { position: absolute; top: 12px; right: 12px; font-size: 0.8rem; }

/* ── RISK & OPP CARDS ── */
.signal-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2px; }
.signal-card {
  background: var(--paper2);
  padding: 1.1rem 1.3rem;
  border-left: 4px solid transparent;
  position: relative;
}
.signal-card.high   { border-left-color: var(--red); }
.signal-card.medium { border-left-color: var(--amber); }
.signal-card.low    { border-left-color: var(--emerald); }
.signal-sev {
  font-family: var(--mono);
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  margin-bottom: 5px;
}
.signal-sev.high   { color: var(--red); }
.signal-sev.medium { color: var(--amber); }
.signal-sev.low    { color: var(--emerald); }
.signal-title { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 0.95rem; color: var(--ink); margin-bottom: 5px; }
.signal-detail { font-size: 0.8rem; color: var(--ink3); line-height: 1.5; margin-bottom: 8px; }
.signal-action {
  font-size: 0.75rem;
  color: var(--emerald);
  font-family: var(--mono);
  border-top: 1px solid var(--paper3);
  padding-top: 6px;
  margin-top: 2px;
}

/* ── ACTION ITEMS ── */
.action-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 1rem 1.2rem;
  background: var(--paper2);
  border-bottom: 1px solid var(--paper3);
  transition: background 0.12s;
}
.action-row:hover { background: var(--paper3); }
.action-row:first-child { border-top: 1px solid var(--paper3); }
.action-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2rem;
  color: var(--paper3);
  line-height: 1;
  min-width: 32px;
  text-align: right;
  padding-top: 2px;
}
.action-content { flex: 1; }
.action-task { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 0.95rem; color: var(--ink); margin-bottom: 3px; }
.action-why  { font-size: 0.78rem; color: var(--ink3); line-height: 1.5; }
.action-tf {
  font-family: var(--mono);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 3px 8px;
  border-radius: 2px;
  white-space: nowrap;
  margin-top: 6px;
  display: inline-block;
}
.tf-today     { background: #7f1d1d; color: #fecaca; }
.tf-week      { background: #78350f; color: #fde68a; }
.tf-month     { background: #14532d; color: #bbf7d0; }

/* ── SUMMARY BLOCK ── */
.summary-block {
  background: var(--paper2);
  padding: 1.5rem 1.8rem;
  border-top: 3px solid var(--emerald);
  margin-bottom: 2px;
}
.summary-eyebrow { font-family: var(--mono); font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--emerald); margin-bottom: 8px; }
.summary-text { font-family: 'Playfair Display', serif; font-size: 1.05rem; color: var(--ink); line-height: 1.75; }

/* ── FORECAST ── */
.forecast-block {
  background: var(--ink);
  color: var(--paper);
  padding: 1.5rem 1.8rem;
  border-radius: 2px;
  margin-bottom: 2rem;
}
.forecast-eyebrow { font-family: var(--mono); font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: #888; margin-bottom: 8px; }
.forecast-text { font-family: 'Playfair Display', serif; font-style: italic; font-size: 1rem; color: #d4d0c8; line-height: 1.7; }

/* ── CONTEXT ── */
.context-block {
  background: var(--em-light);
  border-left: 3px solid var(--emerald);
  padding: 1rem 1.3rem;
  margin-bottom: 2rem;
  border-radius: 0 2px 2px 0;
}
.context-text { font-size: 0.85rem; color: var(--ink2); line-height: 1.65; }

/* ── FOOTER ── */
.pulse-footer {
  border-top: 1px solid var(--paper3);
  padding: 1rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 3rem;
}
.footer-brand { font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; letter-spacing: 0.1em; color: var(--ink3); }
.footer-note  { font-family: var(--mono); font-size: 0.65rem; color: var(--ink3); letter-spacing: 0.05em; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--emerald) !important; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("result", None), ("api_key", ""), ("raw_data", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

SAMPLES = {
    "Retail store": """Monthly Sales Report — March 2024
Total Revenue: $84,200 (vs $91,400 last month, vs $72,100 same month last year)
Units Sold: 1,847
Average Order Value: $45.60
Top Products: Running Shoes $22,100 | Yoga Mats $11,800 | Water Bottles $9,400
Returns: 127 units ($5,780) — up 34% from last month
New Customers: 312 | Returning: 489
Online Sales: $31,200 (37% of total) | In-Store: $53,000
Inventory Alerts: Running Shoes — 3 days stock remaining | Yoga Mats — 8 days
Staff Hours: 940hrs | Overtime: 87hrs
Customer Complaints: 23 (sizing issues x14, delivery delays x9)
Marketing Spend: $3,200 Google Ads, $1,100 Instagram""",

    "SaaS startup": """Q1 2024 Business Metrics
MRR: $47,300 (Jan: $39,100 → Feb: $43,200 → Mar: $47,300)
ARR Run Rate: $567,600
Churn Rate: 3.8% (industry avg 5%)
New Subscriptions: 89 | Cancellations: 31
Trial-to-Paid Conversion: 22%
NPS Score: 41 (Jan: 38, Feb: 39)
Support Tickets: 312 | Avg Resolution: 18hrs | CSAT: 87%
Active Users (DAU): 2,840 | MAU: 8,920
Feature Adoption: Dashboard 94% | API 38% | Integrations 21%
Burn Rate: $31,000/month | Runway: 14 months
Top Cancellation Reasons: Too expensive 42% | Missing features 31% | Competitor 19%
Team: 11 employees, 2 open roles unfilled 60+ days""",

    "Restaurant": """Restaurant Weekly Summary — Week of March 18
Covers Served: 1,247 (Mon-Thu avg 142/day, Fri-Sat avg 218/day, Sun 87)
Total Revenue: $38,460
Food Revenue: $28,900 | Bar Revenue: $9,560
Average Spend per Cover: $30.84
Food Cost %: 34.2% (target 30%)
Labor Cost %: 38.1% (target 35%)
Waste: $1,840 (mostly seafood and produce)
Reservations Honoured: 431 | Walk-ins: 816 | No-shows: 47 (10.9%)
Online Reviews this week: Google 4.1★ (12 reviews) | TripAdvisor 3.8★ (7 reviews)
Negative feedback themes: slow service Friday night, cold food x3, portion size x4
Top sellers: Ribeye Steak $4,200 | Truffle Pasta $3,100 | Cocktail Menu $4,800
Staff Issues: 1 no-call-no-show, chef requested Friday off, 2 servers new this week"""
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem;'>
      <div style='font-family:"Bebas Neue",sans-serif;font-size:2rem;letter-spacing:0.1em;color:#f5f2eb;line-height:1;'>PULSE</div>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#666;margin-top:4px;'>Business Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**<i class='fa fa-key' style='color:#006644'></i> &nbsp;Groq API Key**", unsafe_allow_html=True)
    st.markdown('<a href="https://console.groq.com/keys" target="_blank" style="color:#009960;font-size:0.75rem;font-family:monospace;">Get free key → console.groq.com</a>', unsafe_allow_html=True)
    key = st.text_input("k", type="password", placeholder="gsk_...", label_visibility="collapsed")
    if key: st.session_state.api_key = key

    if st.session_state.api_key:
        st.markdown('<div style="font-family:monospace;font-size:0.72rem;color:#4ade80;margin-top:6px;"><i class="fa fa-circle-check"></i> Key ready</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**<i class='fa fa-database' style='color:#006644'></i> &nbsp;Your Business Data**", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem;color:#888;margin-bottom:6px;">Paste anything — sales, feedback, financials, inventory, tickets...</div>', unsafe_allow_html=True)
    data_input = st.text_area("d", placeholder="Paste your business data here...", height=200, label_visibility="collapsed")

    st.markdown("**<i class='fa fa-flask' style='color:#006644'></i> &nbsp;Try a sample**", unsafe_allow_html=True)
    for label in SAMPLES:
        if st.button(f"  {label}", use_container_width=True):
            st.session_state.raw_data = SAMPLES[label]
            st.rerun()

    if data_input: st.session_state.raw_data = data_input

    st.markdown("---")
    run = st.button("◆  ANALYSE NOW", use_container_width=True)

    if st.session_state.result:
        st.markdown("---")
        report_md = _build_markdown(st.session_state.result)
        st.download_button(
            "⬇  Download Report",
            data=report_md,
            file_name="pulse_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ── RUN ANALYSIS ─────────────────────────────────────────────────────────────
if run:
    if not st.session_state.api_key:
        st.error("Enter your Groq API key in the sidebar.")
    elif not st.session_state.raw_data.strip():
        st.warning("Paste your business data or choose a sample in the sidebar.")
    else:
        with st.spinner("Pulse is reading your data..."):
            try:
                st.session_state.result = analyse(st.session_state.raw_data, st.session_state.api_key)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.session_state.result = None

def _build_markdown(r: dict) -> str:
    lines = [f"# Pulse Report — {r.get('business_name','Business')}", f"**Period:** {r.get('period','')}", "",
             "## Executive Summary", r.get('executive_summary',''), "",
             f"**Health Score:** {r.get('health_score',0)}/100 — {r.get('health_label','')}", "",
             "## KPIs"]
    for k in r.get('kpis',[]):
        lines.append(f"- **{k['label']}:** {k['value']} ({k['change']}) — {k['insight']}")
    lines += ["", "## Risks"]
    for x in r.get('risks',[]):
        lines.append(f"- [{x['severity'].upper()}] **{x['title']}** — {x['detail']} → {x['action']}")
    lines += ["", "## Opportunities"]
    for x in r.get('opportunities',[]):
        lines.append(f"- [{x['impact'].upper()}] **{x['title']}** — {x['detail']} → {x['action']}")
    lines += ["", "## Action Items"]
    for a in r.get('action_items',[]):
        lines.append(f"{a['priority']}. **{a['task']}** ({a['timeframe']}) — {a['why']}")
    lines += ["", "## Market Context", r.get('market_context',''), "", "## Forecast", r.get('forecast','')]
    return "\n".join(lines)

# ── RENDER ────────────────────────────────────────────────────────────────────
r = st.session_state.result

# MASTHEAD
import datetime
now = datetime.datetime.now()
st.markdown(f"""
<div class="masthead">
  <div class="masthead-left">
    <div class="masthead-title">PULSE</div>
    <div class="masthead-rule"></div>
    <div class="masthead-meta">
      Business Intelligence Engine<br>
      {now.strftime('%A, %B %d %Y')}<br>
      AI-Powered Analysis
    </div>
  </div>
  <div class="masthead-tagline">
    "Clarity for every decision."<br>
    <span style="font-size:0.72rem;font-family:'IBM Plex Mono',monospace;font-style:normal;color:#aaa;letter-spacing:0.06em;">POWERED BY GROQ LLM</span>
  </div>
</div>
""", unsafe_allow_html=True)

if not r:
    # ── LANDING STATE ──
    st.markdown("""
    <div class="ticker-bar">
      <span class="ticker-item"><i class="fa fa-chart-line" style="color:#4ade80"></i> &nbsp;PULSE READY</span>
      <span class="ticker-item" style="color:#888">◆ Paste your data in the sidebar → click Analyse Now</span>
      <span class="ticker-item" style="color:#888">◆ Works with: sales reports, financials, CRM exports, feedback, inventory</span>
      <span class="ticker-item" style="color:#888">◆ Get a boardroom-quality brief in seconds</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("fa-gauge-high",    "Health Score",      "Instant 0-100 business vitality score with label — Critical to Thriving."),
        ("fa-chart-bar",     "KPI Extraction",    "Auto-detects your key metrics, calculates trends, and explains what they mean."),
        ("fa-triangle-exclamation", "Risk Radar", "Surfaces hidden risks before they become crises — ranked by severity."),
        ("fa-lightbulb",     "Opportunities",     "Spots revenue and efficiency opportunities buried in your data."),
        ("fa-list-check",    "Action Items",      "Prioritised, specific tasks — not generic advice — with timeframes."),
        ("fa-newspaper",     "Boardroom Brief",   "Download a clean executive report ready to share with your team or investors."),
    ]
    cols = [col1, col2, col3, col1, col2, col3]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div style="background:var(--paper2);border-top:3px solid var(--ink);padding:1.2rem 1.3rem;margin-bottom:2px;">
              <div style="color:var(--emerald);font-size:1.3rem;margin-bottom:8px;"><i class="fa {icon}"></i></div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:0.08em;color:var(--ink);margin-bottom:6px;">{title}</div>
              <div style="font-size:0.8rem;color:var(--ink3);line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pulse-footer">
      <div class="footer-brand">PULSE ◆ BUSINESS INTELLIGENCE</div>
      <div class="footer-note">Free · Powered by Groq LLaMA · No data stored · Open source</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── RESULTS STATE ──
    biz  = r.get('business_name', 'Your Business')
    per  = r.get('period', '')
    score = r.get('health_score', 0)
    label = r.get('health_label', 'Stable')
    badge_cls = {"Thriving":"thriving","Healthy":"healthy","Stable":"stable","At Risk":"at-risk","Critical":"critical"}.get(label, "stable")

    # Ticker
    kpis = r.get('kpis', [])
    ticker_items = " &nbsp;◆&nbsp; ".join(
        f"<span class='ticker-item'>{k['label']}: <span class='{k['trend']}'>{k['value']}</span> {k['change']}</span>"
        for k in kpis[:5]
    )
    st.markdown(f'<div class="ticker-bar">{ticker_items}</div>', unsafe_allow_html=True)

    # Top row — health + summary
    col_h, col_s = st.columns([1, 2])
    with col_h:
        bar_color = {"Thriving":"#006644","Healthy":"#059669","Stable":"#b45309","At Risk":"#dc2626","Critical":"#7f1d1d"}.get(label,"#b45309")
        st.markdown(f"""
        <div class="health-block">
          <div class="health-score-label"><i class="fa fa-heart-pulse"></i> &nbsp;Business Health</div>
          <div class="health-score-num">{score}</div>
          <div style="background:#1c1c1c;border-radius:2px;height:6px;margin:8px 0;">
            <div style="background:{bar_color};height:6px;width:{score}%;border-radius:2px;"></div>
          </div>
          <div class="health-badge badge-{badge_cls}">{label.upper()}</div>
          <div style="font-family:var(--mono);font-size:0.65rem;color:#666;margin-top:12px;text-transform:uppercase;letter-spacing:0.08em;">{biz} &nbsp;·&nbsp; {per}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s:
        st.markdown(f"""
        <div class="summary-block" style="height:100%;">
          <div class="summary-eyebrow"><i class="fa fa-file-lines"></i> &nbsp;Executive Summary</div>
          <div class="summary-text">{r.get('executive_summary','')}</div>
        </div>
        """, unsafe_allow_html=True)

    # KPIs
    st.markdown("""<div class="section-header">
      <span class="section-num">01</span>
      <span class="section-icon"><i class="fa fa-chart-bar"></i></span>
      <h2 class="section-title">Key Performance Indicators</h2>
    </div>""", unsafe_allow_html=True)

    kpi_html = '<div class="kpi-grid">'
    trend_icons = {"up": "fa-arrow-trend-up", "down": "fa-arrow-trend-down", "flat": "fa-minus"}
    trend_colors = {"up": "#006644", "down": "#991b1b", "flat": "#888"}
    for k in kpis:
        trend = k.get('trend','flat')
        icon  = trend_icons.get(trend, 'fa-minus')
        color = trend_colors.get(trend, '#888')
        kpi_html += f"""
        <div class="kpi-card">
          <div class="kpi-trend-icon" style="color:{color}"><i class="fa {icon}"></i></div>
          <div class="kpi-label">{k['label']}</div>
          <div class="kpi-value">{k['value']}</div>
          <div class="kpi-change {trend}"><i class="fa fa-caret-{'up' if trend=='up' else 'down' if trend=='down' else 'right'}"></i> {k['change']}</div>
          <div class="kpi-insight">{k['insight']}</div>
        </div>"""
    kpi_html += '</div>'
    st.markdown(kpi_html, unsafe_allow_html=True)

    # Risks & Opportunities side by side
    col_r, col_o = st.columns(2)

    with col_r:
        st.markdown("""<div class="section-header">
          <span class="section-num">02</span>
          <span class="section-icon"><i class="fa fa-triangle-exclamation"></i></span>
          <h2 class="section-title">Risk Signals</h2>
        </div>""", unsafe_allow_html=True)
        for x in r.get('risks', []):
            sev = x.get('severity','medium')
            sev_icon = {"high":"fa-circle-xmark","medium":"fa-circle-exclamation","low":"fa-circle-info"}.get(sev,"fa-circle")
            st.markdown(f"""
            <div class="signal-card {sev}" style="margin-bottom:2px;">
              <div class="signal-sev {sev}"><i class="fa {sev_icon}"></i> &nbsp;{sev.upper()} RISK</div>
              <div class="signal-title">{x['title']}</div>
              <div class="signal-detail">{x['detail']}</div>
              <div class="signal-action"><i class="fa fa-arrow-right"></i> &nbsp;{x['action']}</div>
            </div>""", unsafe_allow_html=True)

    with col_o:
        st.markdown("""<div class="section-header">
          <span class="section-num">03</span>
          <span class="section-icon"><i class="fa fa-lightbulb"></i></span>
          <h2 class="section-title">Opportunities</h2>
        </div>""", unsafe_allow_html=True)
        for x in r.get('opportunities', []):
            imp = x.get('impact','medium')
            imp_icon = {"high":"fa-rocket","medium":"fa-star","low":"fa-seedling"}.get(imp,"fa-star")
            st.markdown(f"""
            <div class="signal-card {imp}" style="margin-bottom:2px;">
              <div class="signal-sev {imp}"><i class="fa {imp_icon}"></i> &nbsp;{imp.upper()} IMPACT</div>
              <div class="signal-title">{x['title']}</div>
              <div class="signal-detail">{x['detail']}</div>
              <div class="signal-action"><i class="fa fa-arrow-right"></i> &nbsp;{x['action']}</div>
            </div>""", unsafe_allow_html=True)

    # Action items
    st.markdown("""<div class="section-header">
      <span class="section-num">04</span>
      <span class="section-icon"><i class="fa fa-list-check"></i></span>
      <h2 class="section-title">Priority Action Items</h2>
    </div>""", unsafe_allow_html=True)

    for a in r.get('action_items', []):
        tf = a.get('timeframe','This Week')
        tf_cls = {"Today":"today","This Week":"week","This Month":"month"}.get(tf,"week")
        tf_icon = {"Today":"fa-bolt","This Week":"fa-calendar-week","This Month":"fa-calendar"}.get(tf,"fa-calendar-week")
        st.markdown(f"""
        <div class="action-row">
          <div class="action-num">{a['priority']:02d}</div>
          <div class="action-content">
            <div class="action-task">{a['task']}</div>
            <div class="action-why">{a['why']}</div>
            <div class="action-tf tf-{tf_cls}"><i class="fa {tf_icon}"></i> &nbsp;{tf}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Market context + forecast
    st.markdown("""<div class="section-header">
      <span class="section-num">05</span>
      <span class="section-icon"><i class="fa fa-globe"></i></span>
      <h2 class="section-title">Market Context & Forecast</h2>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="context-block">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--emerald);margin-bottom:6px;"><i class="fa fa-globe"></i> &nbsp;Market Context</div>
      <div class="context-text">{r.get('market_context','')}</div>
    </div>
    <div class="forecast-block">
      <div class="forecast-eyebrow"><i class="fa fa-binoculars"></i> &nbsp;Forward Outlook</div>
      <div class="forecast-text">{r.get('forecast','')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pulse-footer">
      <div class="footer-brand">PULSE ◆ BUSINESS INTELLIGENCE</div>
      <div class="footer-note">AI analysis · Not financial advice · <i class="fa fa-lock"></i> Your data is never stored</div>
    </div>
    """, unsafe_allow_html=True)