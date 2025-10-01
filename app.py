import streamlit as st
from guided_care_plan.view import render as render_careplan

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# ======================= Global CSS =======================
st.markdown("""
<style>
:root{
  --pill-radius:14px; --pill-pad:.70rem 1rem; --pill-gap:.70rem;
  --pill-text:#111827; --pill-bg:#F3F4F6; --pill-brd:#E5E7EB; --pill-hover:#E9EBF0;
  --pill-selected:#1F2937; --pill-selected-hover:#111827; --pill-shadow:0 2px 6px rgba(17,24,39,.08);
  --pill-font:16px; --btn-primary:#2E6EFF; --btn-primary-hover:#1F5AE6;
  --btn-secondary-bg:#EAF2FF; --btn-secondary-text:#2E6EFF; --btn-secondary-brd:#D6E4FF;
  --h1-size: 2.125rem; --h1-weight: 800;
  --intro-h-size: 1.5rem; --intro-h-weight: 700;
  --intro-b-size: 1rem; --intro-b-weight: 500; --intro-max: 64ch;
  --q-title-size: 1.125rem; --q-title-weight: 700;
}

/* Title */
h1, .stApp h1 { font-size: var(--h1-size) !important; font-weight: var(--h1-weight) !important; letter-spacing:-.01em; }

/* Intro block: centered column */
.intro-wrap    { max-width: 960px; margin: 0 auto 1rem; }
.intro-head    { font-size: var(--intro-h-size); font-weight: var(--intro-h-weight); margin:.25rem 0 .5rem;
                 max-width: var(--intro-max); margin-left:auto; margin-right:auto; }
.intro-body    { font-size: var(--intro-b-size); font-weight: var(--intro-b-weight); color:#374151; max-width:var(--intro-max);
                 line-height:1.55; margin-left:auto; margin-right:auto; text-align:left; }
.align-intro   { max-width: var(--intro-max); margin-left:auto; margin-right:auto; }

/* Question titles */
.q-title, .q-prompt { font-size: var(--q-title-size); font-weight: var(--q-title-weight); color:#111827; margin:.75rem 0 1rem; }

/* --- Hard-center the welcome blurb and neutralize stray padding --- */
.intro-block{ max-width:720px; margin:0 auto 1.25rem; }
.intro-block h2{ font-size:1.5rem; font-weight:700; margin:.25rem 0 .5rem; letter-spacing:-.01em; }
.intro-block p{
  max-width:60ch; margin:0 auto; padding:0 !important;
  text-align:left; line-height:1.55; color:#374151;
}

/* In case a Streamlit wrapper adds padding to this element container */
.element-container:has(.intro-block){ padding-left:0 !important; }

/* Pill-style radios */
[data-testid="stRadio"] > div{ gap: var(--pill-gap) !important; }
[data-testid="stRadio"] div[role="radiogroup"]{
  display:grid; gap: var(--pill-gap);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  max-width: 960px; margin: 0 auto;
}
[data-testid="stRadio"] div[role="radiogroup"] > label{ margin:0 !important; padding:0 !important; display:block; position:relative; width:100%; }
[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child{ display:none !important; }
[data-testid="stRadio"] input[type="radio"]{ position:absolute !important; opacity:0 !important; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); clip-path: inset(50%); }
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child{
  display:flex; align-items:center; justify-content:center;
  background:var(--pill-bg); color:var(--pill-text);
  border:1.5px solid var(--pill-brd); border-radius:var(--pill-radius);
  padding:var(--pill-pad); box-shadow:var(--pill-shadow);
  cursor:pointer; transition:all .12s ease-in-out;
  font-size:var(--pill-font); line-height:1.3; font-weight:600; user-select:none; text-align:center; width:100%; min-height:56px;
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child:hover{ background:var(--pill-hover); }
[data-testid="stRadio"] input[type="radio"]:checked + div{ background:var(--pill-selected) !important; color:#fff !important; border-color:var(--pill-selected) !important; box-shadow:0 3px 12px rgba(31,41,55,.25); font-weight:700; }
[data-testid="stRadio"] input[type="radio"]:checked + div:hover{ background:var(--pill-selected-hover) !important; }
[data-testid="stRadio"] input[type="radio"]:focus-visible + div{ outline:3px solid rgba(46,110,255,.35); outline-offset:2px; }

/* Buttons */
.stButton > button{ padding:.7rem 1.1rem; }
button[kind="primary"]{ background:var(--btn-primary) !important; color:#fff !important; border-radius:12px !important; border:0 !important; box-shadow:0 2px 8px rgba(46,110,255,.25) !important; }
button[kind="primary"]:hover{ background:var(--btn-primary-hover) !important; }
button[kind="secondary"]{ background:var(--btn-secondary-bg) !important; color:#2E6EFF !important; border:1px solid var(--btn-secondary-brd) !important; border-radius:12px !important; }

/* Progress rail */
.progress-rail{ display:flex; gap:.5rem; margin:.25rem 0 1rem 0; }
.progress-rail .seg{ height:4px; flex:1; border-radius:999px; background:#E5E7EB; }
.progress-rail .seg.active{ background:var(--btn-primary); }

/* Keep Back/Next horizontal on mobile */
@media (max-width: 480px){
  div[data-testid="stHorizontalBlock"]{ display:flex !important; flex-wrap: nowrap !important; gap:.75rem !important; }
  div[data-testid="stHorizontalBlock"] > div[data-testid="column"]{ flex:1 1 0% !important; min-width: 0 !important; }
  .stButton > button{ width:100%; }
  .block-container{ padding-left:1rem !important; padding-right:1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# Optional dev QA
with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

st.title("Senior Care Navigator")

# Progress rail for steps 1..12
total_steps = 12
step = st.session_state.get("planner_step", 0)
if 1 <= step <= total_steps:
    rail = '<div class="progress-rail">' + ''.join(
        f'<div class="seg{" active" if i < step else ""}"></div>' for i in range(total_steps)
    ) + '</div>'
    st.markdown(rail, unsafe_allow_html=True)

# Mount the Guided Care Plan
render_careplan()

# QA drawer
if st.session_state.get("qa_mode"):
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.get("care_context", {}))
