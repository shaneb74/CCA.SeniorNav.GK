import streamlit as st
import logic

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# ===== Global CSS (palette + pills + progress + mobile tweaks + compact popover trigger) =====
st.markdown("""
<style>
:root{
  /* Pills */
  --pill-radius:14px; --pill-pad:.6rem 1rem; --pill-gap:.6rem;
  --pill-text:#111827;
  --pill-bg:#F3F4F6;
  --pill-brd:#E5E7EB;
  --pill-hover:#E9EBF0;
  --pill-selected:#1F2937;
  --pill-selected-hover:#111827;
  --pill-shadow:0 2px 6px rgba(17,24,39,.08);
  --pill-font:14px;

  /* Buttons */
  --btn-primary:#2E6EFF;
  --btn-primary-hover:#1F5AE6;
  --btn-secondary-bg:#EAF2FF;
  --btn-secondary-text:#2E6EFF;
  --btn-secondary-brd:#D6E4FF;
}

/* Radio grid */
[data-testid="stRadio"] > div{ gap: var(--pill-gap) !important; }
[data-testid="stRadio"] div[role="radiogroup"]{
  display:grid; gap:var(--pill-gap);
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  align-items:stretch;
}

/* Hide native radio dot */
[data-testid="stRadio"] div[role="radiogroup"] > label{ margin:0 !important; padding:0 !important; display:block; position:relative; }
[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child{ display:none !important; }
[data-testid="stRadio"] input[type="radio"]{
  position:absolute !important; opacity:0 !important; width:1px; height:1px;
  overflow:hidden; clip:rect(0 0 0 0); clip-path: inset(50%);
}

/* Pill base */
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child{
  display:flex; align-items:center; justify-content:center;
  background:var(--pill-bg); color:var(--pill-text);
  border:1.5px solid var(--pill-brd); border-radius:var(--pill-radius);
  padding:var(--pill-pad); box-shadow:var(--pill-shadow);
  cursor:pointer; transition:all .12s ease-in-out;
  font-size:var(--pill-font); line-height:1.3; white-space:nowrap;
  user-select:none; text-align:center; font-weight:500;
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child:hover{
  background:var(--pill-hover);
}

/* Selected pill */
[data-testid="stRadio"] input[type="radio"]:checked + div{
  background:var(--pill-selected) !important; color:#FFFFFF !important;
  border-color:var(--pill-selected) !important;
  box-shadow:0 3px 12px rgba(31,41,55,.25);
  font-weight:600;
}
[data-testid="stRadio"] input[type="radio"]:checked + div:hover{
  background:var(--pill-selected-hover) !important; border-color:var(--pill-selected-hover) !important;
}

/* Focus ring */
[data-testid="stRadio"] input[type="radio"]:focus-visible + div{
  outline:3px solid rgba(46,110,255,.35); outline-offset:2px;
}

/* Buttons */
.stButton > button { padding:.6rem 1rem; }
button[kind="primary"]{
  background:var(--btn-primary) !important; color:#fff !important;
  border-radius:12px !important; border:0 !important;
  box-shadow:0 2px 8px rgba(46,110,255,.25) !important;
}
button[kind="primary"]:hover{ background:var(--btn-primary-hover) !important; }
button[kind="secondary"]{
  background:var(--btn-secondary-bg) !important; color:var(--btn-secondary-text) !important;
  border:1px solid var(--btn-secondary-brd) !important; border-radius:12px !important;
}

/* Progress rail */
.progress-rail{ display:flex; gap:.5rem; margin:.25rem 0 1rem 0; }
.progress-rail .seg{ height:4px; flex:1; border-radius:999px; background:#E5E7EB; }
.progress-rail .seg.active{ background:var(--btn-primary); }

/* Compact popover trigger button */
button[aria-expanded][role="button"]{
  padding:.25rem .6rem !important; border-radius:8px !important;
}

/* Mobile tweaks: keep Back/Next horizontal + full-width inside columns */
@media (max-width: 480px){
  .block-container div[data-testid="stHorizontalBlock"] { gap:.5rem !important; }
  .block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]{
    min-width:0 !important; width:50% !important; flex:1 1 50% !important;
  }
  .stButton > button{ width:100% !important; }
  .block-container{ padding-left:1rem !important; padding-right:1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ===== Session init =====
if "qa_mode" not in st.session_state:
    st.session_state.qa_mode = False
if "planner_step" not in st.session_state:
    st.session_state.planner_step = 0
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "person_a_name": None,
        "person_b_name": None,
        "flags": {},
        "chronic_conditions": [],
        "derived": {}
    }
if "chronic_conditions" not in st.session_state:
    st.session_state.chronic_conditions = []

# ===== Header =====
st.title("Senior Care Navigator")

# Sidebar QA toggle
with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

# ===== Progress rail (for steps 1..12) =====
total_steps = 12
step = st.session_state.get("planner_step", 0)
if 1 <= step <= total_steps:
    rail = '<div class="progress-rail">' + ''.join(
        f'<div class="seg{" active" if i < step else ""}"></div>' for i in range(total_steps)
    ) + '</div>'
    st.markdown(rail, unsafe_allow_html=True)

# Delegate main flow
logic.run_flow()

# QA drawer
if st.session_state.qa_mode:
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.care_context)
