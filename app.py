import streamlit as st
from guided_care_plan.engine import render as render_careplan

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# ---------- Global CSS ----------
STYLES = """
<style>
:root{
  --pill-radius:14px; --pill-pad:.70rem 1rem; --pill-gap:.70rem;
  --pill-text:#111827; --pill-bg:#F3F4F6; --pill-brd:#E5E7EB; --pill-hover:#E9EBF0;
  --pill-selected:#1F2937; --pill-selected-hover:#111827; --pill-shadow:0 2px 6px rgba(17,24,39,.08);
  --pill-font:16px; --btn-primary:#2E6EFF; --btn-primary-hover:#1F5AE6;
  --btn-secondary-bg:#EAF2FF; --btn-secondary-text:#2E6EFF; --btn-secondary-brd:#D6E4FF;
}

/* Title & hero */
h1 { letter-spacing:.2px; }
.scn-hero { text-align:center; max-width:820px; margin: 0 auto 1.25rem; }
.scn-hero h2 { margin:.25rem 0 .35rem; }
.scn-hero p { margin:.25rem auto 0; max-width:720px; color:#374151; }

/* Progress rail (steps) */
.progress-rail{ display:flex; gap:.5rem; margin:.25rem 0 1rem; }
.progress-rail .seg{ height:4px; flex:1; border-radius:999px; background:#E5E7EB; }
.progress-rail .seg.active{ background:var(--btn-primary); }

/* ------- RADIO -> CHIPS (robust to Streamlit DOM) ------- */
div[data-testid="stRadio"] > label {      /* question prompt if used */
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  color:#111827 !important;
  margin-bottom:.5rem !important;
}
div[data-testid="stRadio"] div[role="radiogroup"]{
  display:grid !important;
  gap: var(--pill-gap) !important;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
  max-width: 960px; margin:0 auto !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label{
  /* each option container */
  margin:0 !important; padding:0 !important; display:block !important; width:100%;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child{
  /* hide the dot column */
  display:none !important;
}
div[data-testid="stRadio"] input[type="radio"]{
  position:absolute !important; opacity:0 !important; width:1px; height:1px;
  overflow:hidden; clip:rect(0 0 0 0); clip-path: inset(50%);
}
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child{
  /* the visible pill */
  display:flex !important; align-items:center !important; justify-content:center !important;
  background:var(--pill-bg) !important; color:var(--pill-text) !important;
  border:1.5px solid var(--pill-brd) !important; border-radius:var(--pill-radius) !important;
  padding:var(--pill-pad) !important; box-shadow:var(--pill-shadow) !important;
  cursor:pointer !important; transition:all .12s ease-in-out !important;
  font-size:var(--pill-font) !important; line-height:1.3 !important;
  user-select:none !important; text-align:center !important; font-weight:600 !important;
  min-height:56px !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child:hover{
  background:var(--pill-hover) !important;
}
div[data-testid="stRadio"] input[type="radio"]:checked + div{
  background:var(--pill-selected) !important; color:#FFFFFF !important;
  border-color:var(--pill-selected) !important;
  box-shadow:0 3px 12px rgba(31,41,55,.25) !important; font-weight:700 !important;
}
div[data-testid="stRadio"] input[type="radio"]:checked + div:hover{
  background:var(--pill-selected-hover) !important;
}

/* ------- NAV: keep Back/Next horizontal even on mobile ------- */
.scn-nav-row {
  display:flex !important;
  gap: 12px !important;
  justify-content:center !important;
  align-items:center !important;
  flex-wrap: nowrap !important;          /* no wrapping on narrow screens */
  margin: .5rem 0 0.75rem !important;
}
.scn-nav-row > div {                      /* the column wrappers Streamlit inserts */
  flex: 0 0 auto !important;              /* do NOT shrink */
}
.scn-nav-row button[kind="secondary"],
.scn-nav-row button[kind="primary"]{
  min-width: 120px !important;
}

/* Buttons look & feel */
.stButton > button { padding:.7rem 1.1rem; }
button[kind="primary"]{
  background:var(--btn-primary) !important; color:#fff !important;
  border-radius:12px !important; border:0 !important;
  box-shadow:0 2px 8px rgba(46,110,255,.25) !important;
}
button[kind="primary"]:hover{ background:var(--btn-primary-hover) !important; }
button[kind="secondary"]{
  background:var(--btn-secondary-bg) !important; color:#2E6EFF !important;
  border:1px solid var(--btn-secondary-brd) !important; border-radius:12px !important;
}

/* "Why we ask" spacing under nav */
.scn-why-wrap { margin-top: .75rem !important; }

/* Mobile container padding */
@media (max-width: 480px){
  .block-container{ padding-left:1rem !important; padding-right:1rem !important; }
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# QA toggle in sidebar (kept)
with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

# App title
st.title("Senior Care Navigator")

# Simple progress rail if we’re inside the flow (1..12)
total_steps = 12
step = st.session_state.get("planner_step", 0)
if 1 <= step <= total_steps:
    rail = '<div class="progress-rail">' + ''.join(
        f'<div class="seg{" active" if i < step else ""}"></div>' for i in range(total_steps)
    ) + '</div>'
    st.markdown(rail, unsafe_allow_html=True)

# Hand off to the Guided Care Plan flow
render_careplan()

# Optional QA block
if st.session_state.get("qa_mode"):
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.get("care_context", {}))
