import streamlit as st
import logic  # visual shell only; keeps all business logic in logic.py

# ---------- Page meta ----------
st.set_page_config(
    page_title="Senior Navigator",
    page_icon="🧭",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# ---------- Global CSS (visual-only) ----------
STYLES = """
<style>
:root{
  --card:#ffffff;
  --ink:#1b2430;
  --muted:#5b6678;
  --brand:#1f6feb;
  --brand-ink:#ffffff;
  --chip:#eef3ff;
  --chip-b:#dbe5ff;
  --chip-ink:#2a3a6b;
  --radius:14px;
}

.block-container{
  max-width: 980px;
  padding-top: 1rem !important;
}
header[data-testid="stHeader"] { background: transparent; }
footer {visibility: hidden;}

html, body {
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial;
}
:root { --body: 18px; --muted: 15px; --h1: 44px; --h2: 28px; --h3: 20px; }
p, .stMarkdown { font-size: var(--body) !important; line-height: 1.65; color: var(--ink); }
h1 { font-size: var(--h1); letter-spacing: -0.02em; margin: 0 0 .25rem 0; }
h2 { font-size: var(--h2); margin: .75rem 0 .35rem 0; color: var(--ink); }
h3 { font-size: var(--h3); margin: .5rem 0 .25rem 0; color: var(--ink); }
small, .stCaption { font-size: var(--muted) !important; color: var(--muted); }

.app-hero{
  border-radius: 24px;
  padding: 22px 22px 16px 22px;
  border: 1px solid rgba(0,0,0,.06);
}
.section-card{
  background: var(--card);
  border: 1px solid #eef0f6;
  border-radius: var(--radius);
  padding: 20px 22px;
  box-shadow: 0 6px 18px rgba(13, 23, 63, 0.06);
  margin: 12px 0 22px 0;
}

.progress-bar{ display:flex; gap:8px; flex-wrap: wrap; margin: 12px 0 4px 0; }
.progress-chip{
  font-size: 13px; padding: 6px 10px; border-radius: 999px;
  background: var(--chip); color: var(--chip-ink); border: 1px solid var(--chip-b);
}
.progress-chip.active{ background: var(--brand); color: var(--brand-ink); border-color: var(--brand); }

[data-testid="stWidgetLabel"], [data-testid="stRadio"] [data-testid="stWidgetLabel"]{
  font-size: 20px !important; font-weight: 600; color: var(--ink); margin: 2px 0 8px 0; display:block;
}
.stRadio > div > label, [data-testid="stRadio"] div[role="radiogroup"] > div > label{
  line-height: 1.5; margin: 6px 0; display:flex; align-items:center; gap:.5rem;
}
.stRadio > div > label span, [data-testid="stRadio"] div[role="radiogroup"] > div > label span{ font-size: 18px !important; }

.stButton > button{
  background-color: var(--brand); color: var(--brand-ink);
  border: none; border-radius: 10px; padding: 12px 18px; font-size: 18px; font-weight: 600;
  box-shadow: 0 6px 12px rgba(31,111,235,.18);
}
.stButton > button:hover { filter: brightness(1.05); }
.stButton > button:disabled{ opacity:.55; box-shadow: none; }

.stButton > button:focus-visible,
input[type="radio"]:focus-visible + div,
label:has(input[type="radio"]:focus-visible){
  outline: 3px solid rgba(31,111,235,.45);
  outline-offset: 2px;
  border-radius: 10px;
}

.sidebar-card{
  background: var(--card); border: 1px solid #eef0f6; border-radius: var(--radius);
  padding: 14px; box-shadow: 0 3px 12px rgba(13,23,63,.05);
}
.summary-badge{ display:inline-block; font-size:12px; padding:4px 8px; margin:3px 3px 0 0;
  border-radius:999px; background:#f6f8fb; border:1px solid #e6eaf2; color:#334155; }

.app-footer{ text-align:center; font-size:13px; margin-top: 8px; }
</style>
"""

st.markdown(STYLES, unsafe_allow_html=True)

if "care_context" not in st.session_state:
    st.session_state.care_context = {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}}
if "step" not in st.session_state:
    st.session_state.step = "planner"
if "planner_step" not in st.session_state:
    st.session_state.planner_step = 1

with st.sidebar:
    st.markdown("<h3 style='margin:0 0 8px 0;'>🧭 Senior Navigator</h3>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("**Your answers so far**")
    cc = st.session_state.care_context
    if cc.get("care_flags"):
        for k, v in cc["care_flags"].items():
            st.markdown(f"<span class='summary-badge'>{k.replace('_',' ').title()}: {v}</span>", unsafe_allow_html=True)
    if cc.get("derived_flags"):
        st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)
        st.caption("Derived insights")
        for k, v in cc["derived_flags"].items():
            st.markdown(f"<span class='summary-badge'>{k.replace('_',' ').title()}: {v}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

col = st.container()
with col:
    st.markdown("<div class='app-hero'>", unsafe_allow_html=True)
    st.markdown("<h1>Guided Care Plan</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-sub'>Let’s walk through your care needs—one friendly step at a time.</p>", unsafe_allow_html=True)

    labels = ["Funding","Cognition","Caregiver","Meds","Independence","Mobility","Your World","Home Preference","Recommendation"]
    active_idx = max(1, min(st.session_state.get("planner_step", 1), len(labels))) - 1
    chips = "".join(f'<span class="progress-chip {"active" if i == active_idx else ""}">{i+1}. {txt}</span>' for i, txt in enumerate(labels))
    st.markdown(f'<div class="progress-bar">{chips}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
logic.render_step(st.session_state.step)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='app-footer'>Built with ❤️ to help you navigate care decisions.</div>", unsafe_allow_html=True)
