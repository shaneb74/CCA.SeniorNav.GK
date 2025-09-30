import streamlit as st
import logic  # business logic only

st.set_page_config(
    page_title="Senior Navigator",
    page_icon="🧭",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# ===== Design System (one source of truth) =====

STYLES = """
<style>
:root{
  --brand:#0B5CD8; --brand-ink:#fff;
  --ink:#0f172a; --muted:#475569;
  --bg:#f6f7fb; --card:#fff; --border:#e5e7eb;
  --radius:14px; --pad:18px; --gap:14px;
  --shadow:0 6px 18px rgba(17,24,39,.06);
}

/* Base */
html,body,[data-testid="stAppViewContainer"] *{box-sizing:border-box}
[data-testid="stAppViewContainer"]{background:var(--bg);}
.block-container{max-width:980px;padding-top:12px}
header[data-testid="stHeader"]{background:transparent}
footer{visibility:hidden}

/* Typography */
body, .stMarkdown, p{font:16px/1.6 ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, Apple Color Emoji, Segoe UI Emoji; color:var(--ink)!important}
h1{font-size:34px;margin:.25rem 0 .25rem 0;letter-spacing:-.01em}
h2{font-size:24px!important;margin:.5rem 0 .35rem 0}
h3{font-size:18px;margin:.5rem 0 .25rem 0}
small,.stCaption{font-size:13px!important;color:var(--muted)}

/* Card */
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 22px;box-shadow:var(--shadow);margin:8px 0 18px}
.card > *:last-child{margin-bottom:0}

/* Inputs */
label[data-testid="stWidgetLabel"]{font-size:16px!important;font-weight:600;margin:.25rem 0 .25rem 0;color:#111827;display:block}
[data-testid="stRadio"] div[role="radiogroup"] > div{padding:.3rem .35rem;border-radius:10px}
[data-testid="stRadio"] div[role="radiogroup"] > div:hover{background:#f1f5f9}
.stTextInput input,.stNumberInput input,.stSelectbox select{border:1px solid var(--border);border-radius:12px;padding:.55rem .7rem;font-size:16px}
/* Radio bullet color */
input[type="radio"] + div:before{accent-color:var(--brand)!important}

/* Buttons */
.stButton > button{border-radius:12px;padding:.6rem 1rem;border:1px solid var(--border);box-shadow:0 1px 2px rgba(16,24,40,.05);font-weight:600}
.stButton > button[kind="primary"], .stButton > button[data-baseweb="buttonPrimary"], .stButton > button:has(+ [data-testid="baseButton-primary"]) {background:var(--brand)!important;color:var(--brand-ink)!important;border-color:var(--brand)!important}
/* Align nav buttons */
.nav-row{display:flex;justify-content:space-between;gap:12px;margin-top:12px}

/* Sidebar */
section[data-testid="stSidebar"]{background:#f8fafc;border-right:1px solid var(--border)}
section[data-testid="stSidebar"] > div{padding:12px}
.progress-bar{display:flex;flex-direction:column;gap:8px}
.progress-chip{border:1px solid var(--border);border-radius:10px;padding:.4rem .6rem;font-size:13px;color:#1f2937;background:#fff}
.progress-chip.active{background:var(--brand);color:var(--brand-ink);border-color:var(--brand);font-weight:600}

/* Content width */
.content{max-width:760px;margin:0 auto}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)


# ---- Session bootstrap ----
if "care_context" not in st.session_state:
    st.session_state.care_context = {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}}
if "step" not in st.session_state:
    st.session_state.step = "audiencing"  # or "planner"
if "audiencing_step" not in st.session_state:
    st.session_state.audiencing_step = 1
if "planner_step" not in st.session_state:
    st.session_state.planner_step = 1

# ---- Sidebar progress ----
if st.session_state.step == "planner":
    labels = ["Funding", "Cognition", "Caregiver", "Meds", "Independence", "Mobility", "Your World", "Home Preference", "Recommendation"]
    active_idx = max(1, min(st.session_state.get("planner_step", 1), len(labels))) - 1
    chips_html = "".join(
        f'<span class="progress-chip {"active" if i==active_idx else ""}">{i+1}. {txt}</span>'
        for i, txt in enumerate(labels)
    )
    st.sidebar.title("Navigation")
    st.sidebar.markdown(f'<div class="progress-bar">{chips_html}</div>', unsafe_allow_html=True)

# ---- Header + content ----
with st.container():
    st.markdown("<div class='content-max'>", unsafe_allow_html=True)
    st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-hook-container'>", unsafe_allow_html=True)

    title = "Senior Care Navigator" if st.session_state.step == "audiencing" else "Guided Care Plan"
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown("<p class='muted'>We’ll ask only what’s needed and save your answers as we go.</p>", unsafe_allow_html=True)

    # Delegate the actual step UI to logic.py
    logic.render_step(st.session_state.step)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Footer ----
st.markdown(
    "<div style='text-align:center;font-size:13px;margin-top:8px;color:#475569'>"
    "Built to reduce guesswork and noise. If it doesn’t, we fix it."
    "</div>",
    unsafe_allow_html=True,
)
