import streamlit as st
from GuidedCarePlan.view import render as render_careplan

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# ===== Global CSS with unified typography =====
st.markdown("""
<style>
:root{
  --pill-radius:14px; --pill-pad:.70rem 1rem; --pill-gap:.70rem;
  --pill-text:#111827; --pill-bg:#F3F4F6; --pill-brd:#E5E7EB; --pill-hover:#E9EBF0;
  --pill-selected:#1F2937; --pill-selected-hover:#111827; --pill-shadow:0 2px 6px rgba(17,24,39,.08);
  --pill-font:16px; --btn-primary:#2E6EFF; --btn-primary-hover:#1F5AE6;
  --btn-secondary-bg:#EAF2FF; --btn-secondary-text:#2E6EFF; --btn-secondary-brd:#D6E4FF;

  --h1-size: 2.125rem;     /* 34px */
  --h1-weight: 800;
  --intro-h-size: 1.5rem;  /* 24px */
  --intro-h-weight: 700;
  --intro-b-size: 1rem;    /* 16px */
  --intro-b-weight: 500;
  --intro-max: 64ch;
  --q-title-size: 1.125rem; /* 18px */
  --q-title-weight: 600;
  --small-size: .875rem;   /* 14px */
}

/* App title */
h1, .stMarkdown h1, .stApp h1 {
  font-size: var(--h1-size) !important;
  font-weight: var(--h1-weight) !important;
  letter-spacing: -0.01em;
}

/* Intro block */
.intro-head {
  font-size: var(--intro-h-size);
  font-weight: var(--intro-h-weight);
  margin: .25rem 0 .5rem;
}
.intro-body {
  font-size: var(--intro-b-size);
  font-weight: var(--intro-b-weight);
  color: #374151;
  max-width: var(--intro-max);
  line-height: 1.55;
  margin-bottom: 1.25rem;
}

/* Question titles */
.q-title, .q-prompt {
  font-size: var(--q-title-size);
  font-weight: var(--q-title-weight);
  color: #111827;
  margin: .5rem 0 .75rem;
}

/* Pills */
[data-testid="stRadio"] > div{ gap: var(--pill-gap) !important; }
[data-testid="stRadio"] div[role="radiogroup"]{
  display:grid;
  gap: var(--pill-gap);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  max-width: 960px;
  margin: 0 auto;
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child{
  font-size: var(--pill-font);
  font-weight: 600;
}

/* Popover */
button[aria-expanded][role="button"]{
  background: transparent !important; color: #2563eb !important;
  font-size: var(--small-size) !important;
  font-weight: 500 !important;
  border: none !important; box-shadow: none !important;
  text-decoration: underline; padding: .25rem 0 !important;
  margin: 0 auto !important; display: block;
}

/* Buttons */
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

/* Progress rail */
.progress-rail{ display:flex; gap:.5rem; margin:.25rem 0 1rem 0; }
.progress-rail .seg{ height:4px; flex:1; border-radius:999px; background:#E5E7EB; }
.progress-rail .seg.active{ background:var(--btn-primary); }

/* Mobile */
@media (max-width: 480px){
  :root{
    --h1-size: 1.875rem;    /* 30px */
    --intro-h-size: 1.375rem;
    --q-title-size: 1.0625rem; /* 17px */
  }
  .block-container{ padding-left:1rem !important; padding-right:1rem !important; }
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

st.title("Senior Care Navigator")

# Progress rail
total_steps = 12
step = st.session_state.get("planner_step", 0)
if 1 <= step <= total_steps:
    rail = '<div class="progress-rail">' + ''.join(
        f'<div class="seg{" active" if i < step else ""}"></div>' for i in range(total_steps)
    ) + '</div>'
    st.markdown(rail, unsafe_allow_html=True)

# Guided Care Plan
render_careplan()

# QA drawer
if st.session_state.get("qa_mode"):
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.get("care_context", {}))
