import streamlit as st
from guided_care_plan.engine import render as render_careplan

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# ===== Global CSS =====
st.markdown("""
<style>
:root{
  --pill-radius:14px; --pill-pad:.70rem 1rem; --pill-gap:.70rem;
  --pill-text:#111827; --pill-bg:#F3F4F6; --pill-brd:#E5E7EB; --pill-hover:#E9EBF0;
  --pill-selected:#1F2937; --pill-selected-hover:#111827; --pill-shadow:0 2px 6px rgba(17,24,39,.08);
  --pill-font:16px; --btn-primary:#2E6EFF; --btn-primary-hover:#1F5AE6;
  --btn-secondary-bg:#EAF2FF; --btn-secondary-text:#2E6EFF; --btn-secondary-brd:#D6E4FF;
}

/* ---- HERO paragraph (shown only on step 0 via app.py) ---- */
.scn-hero{
  max-width: 720px;
  margin: 0 auto 2rem auto;
  text-align: center;
}
.scn-hero [data-testid="stMarkdownContainer"]{ text-align: center !important; }
.scn-hero p{
  margin: 0 auto .5rem auto !important;
  line-height: 1.55; color: #374151; font-size: 1.05rem;
}

/* ---- Radio pill grid ---- */
[data-testid="stRadio"] > div{ gap: var(--pill-gap) !important; }
[data-testid="stRadio"] div[role="radiogroup"]{
  display:grid; gap: var(--pill-gap);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  max-width: 960px; margin: 0 auto;
}
[data-testid="stRadio"] > label{
  font-size: 1.05rem !important; font-weight: 600 !important;
  color:#111827 !important; margin-bottom:.5rem !important;
}
[data-testid="stRadio"] div[role="radiogroup"] > label{ 
  margin:0 !important; padding:0 !important; display:block; position:relative; width:100%;
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child{ display:none !important; }
[data-testid="stRadio"] input[type="radio"]{
  position:absolute !important; opacity:0 !important; width:1px; height:1px;
  overflow:hidden; clip:rect(0 0 0 0); clip-path: inset(50%);
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child{
  display:flex; align-items:center; justify-content:center;
  background:var(--pill-bg); color:var(--pill-text);
  border:1.5px solid var(--pill-brd); border-radius:var(--pill-radius);
  padding:var(--pill-pad); box-shadow:var(--pill-shadow);
  cursor:pointer; transition:all .12s ease-in-out;
  font-size:var(--pill-font); line-height:1.3; font-weight:600;
  user-select:none; text-align:center; width:100%; min-height:56px;
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child:hover{ background:var(--pill-hover); }
[data-testid="stRadio"] input[type="radio"]:checked + div{
  background:var(--pill-selected) !important; color:#FFFFFF !important;
  border-color:var(--pill-selected) !important;
  box-shadow:0 3px 12px rgba(31,41,55,.25); font-weight:700;
}
[data-testid="stRadio"] input[type="radio"]:checked + div:hover{
  background:var(--pill-selected-hover) !important; border-color:var(--pill-selected-hover) !important;
}
[data-testid="stRadio"] input[type="radio"]:focus-visible + div{
  outline:3px solid rgba(46,110,255,.35); outline-offset:2px;
}

/* ---- Buttons ---- */
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

/* ---- Progress rail ---- */
.progress-rail{ display:flex; gap:.5rem; margin:.25rem 0 1rem 0; }
.progress-rail .seg{ height:4px; flex:1; border-radius:999px; background:#E5E7EB; }
.progress-rail .seg.active{ background:var(--btn-primary); }

/* ---- Nav row: keep Back/Next horizontal until really tiny ---- */
.scn-nav-row{
  display: flex !important;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: 1rem;
}
.scn-nav-row > div{ flex: 1; }
@media (max-width: 420px){
  .scn-nav-row{ flex-direction: column; }
}

/* ---- "Why we ask" expander spacing below buttons ---- */
.scn-why-wrap{ max-width:960px; margin: .75rem auto 0 auto; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

st.title("Senior Care Navigator")

# Show hero ONLY on step 0
step = st.session_state.get("planner_step", 0)
if step == 0:
    st.markdown(
        """
        <div class="scn-hero">
          <p>We make navigating senior care simple. Answer a few quick questions and we’ll connect you with the best options, backed by expert guidance — always free for families.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Progress rail for steps 1..12
total_steps = 12
if 1 <= step <= total_steps:
    rail = '<div class="progress-rail">' + ''.join(
        f'<div class="seg{" active" if i < step else ""}"></div>' for i in range(total_steps)
    ) + '</div>'
    st.markdown(rail, unsafe_allow_html=True)

# Mount Care Plan flow
render_careplan()

# QA drawer
if st.session_state.get("qa_mode"):
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.get("care_context", {}))
