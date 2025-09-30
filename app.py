import streamlit as st
import logic  # business logic only

st.set_page_config(
    page_title="Senior Navigator",
    page_icon="🧭",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

STYLES = """
<style>
:root{
  --brand:#0B5CD8;
  --brand-ink:#ffffff;
  --ink:#0f172a;
  --muted:#475569;
  --chip:#E6EEFF;
  --chip-b:#C7D2FE;
  --chip-ink:#1E3A8A;
  --card:#ffffff;
  --radius:14px;
}
.block-container{ max-width:1360px; padding-top:1rem !important; }
header[data-testid="stHeader"] { background: transparent; }
footer {visibility: hidden;}
p, .stMarkdown { font-size: 18px !important; line-height: 1.65; color: var(--ink) !important; }
h1 { font-size: 44px; margin:0 0 .25rem 0; color: var(--ink); }
h2 { font-size: 28px; margin:.75rem 0 .35rem 0; color: var(--ink); }
h3 { font-size: 20px; margin:.5rem 0 .25rem 0; color: var(--ink); }
small, .stCaption { font-size: 15px !important; color: var(--muted); }


.section-card{ background: var(--card); border: 1px solid #eef0f6; border-radius: var(--radius);
  padding: 20px 22px; box-shadow: 0 6px 18px rgba(13, 23, 63, 0.06); margin: 12px 0 22px 0; }

.progress-bar{ display:flex; gap:8px; flex-wrap: wrap; margin: 12px 0 4px 0; }
.progress-chip{ font-size: 13px; padding: 6px 10px; border-radius: 999px;
  background: var(--chip); color: var(--chip-ink); border: 1px solid var(--chip-b); }
.progress-chip.active{ background: var(--brand); color: #ffffff; border-color: var(--brand); }

/* Buttons: enforce white text and inline layout */
.stButton > button{
  width:auto !important; display:inline-flex; align-items:center; justify-content:center; white-space:nowrap; background:var(--brand) !important; color: var(--brand-ink) !important;
  border:1px solid #CBD5E1 !important; opacity:1; box-shadow:none !important;
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# ---- Session bootstrap ----
if "care_context" not in st.session_state:
    st.session_state.care_context = {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}}
if "step" not in st.session_state:
    st.session_state.step = "audiencing"
if "audiencing_step" not in st.session_state:
    st.session_state.audiencing_step = 1
if "planner_step" not in st.session_state:
    st.session_state.planner_step = 1

# ---- Header + progress ----
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<h1>Guided Care Plan</h1>", unsafe_allow_html=True)
st.markdown("<p>Let’s walk through your care needs—one friendly step at a time.</p>", unsafe_allow_html=True)

if st.session_state.step == "planner":
    labels = ["Funding","Cognition","Caregiver","Meds","Independence","Mobility","Your World","Home Preference","Recommendation"]
    active_idx = max(1, min(st.session_state.get('planner_step', 1), len(labels))) - 1
    chips = "".join(
        f'<span class="progress-chip {"active" if i == active_idx else ""}">{i+1}. {txt}</span>'
        for i, txt in enumerate(labels)
    )
    st.markdown(f'<div class="progress-bar">{chips}</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- Step card ----
st.markdown('<div class="section-card">', unsafe_allow_html=True)
logic.render_step(st.session_state.step)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Footer ----
st.markdown("<div style='text-align:center;font-size:13px;margin-top:8px;color:#475569;'>Built with ❤️ to help you navigate care decisions.</div>", unsafe_allow_html=True)
