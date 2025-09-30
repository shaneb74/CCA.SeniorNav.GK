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
:root {
  --brand:#0B5CD8;
  --brand-ink:#ffffff;
  --ink:#0f172a;
  --muted:#475569;
  --border:#e6e8f0;
  --card:#ffffff;
  --chip:#E6EEFF;
  --chip-b:#C7D2FE;
  --chip-ink:#1E3A8A;
  --radius:14px;
  --pad:18px;
  --gap:14px;
}

html, body, [data-testid="stAppViewContainer"] * { box-sizing:border-box; }

.block-container{max-width:1100px;padding-top:8px;}
header[data-testid="stHeader"] { background:transparent; }
footer { visibility:hidden; }

/* Sidebar polish */
section[data-testid="stSidebar"]>div{padding:12px;}
section[data-testid="stSidebar"]{background:#f8fafc;border-right:1px solid var(--border);}

/* Typography */
p, .stMarkdown { font-size:18px!important; line-height:1.6; color:var(--ink)!important; }
h1{font-size:42px;letter-spacing:-.02em;margin:.25rem 0 .25rem 0;color:var(--ink);}
h2 { font-size:28px!important; line-height:1.25; margin:.75rem 0 .35rem 0; color:var(--ink); }
h3 { font-size:20px; margin:.5rem 0 .25rem 0; color:var(--ink); }
small, .stCaption { font-size:14px!important; color:var(--muted); }

/* Cards */
.card-hook-container{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px;box-shadow:0 2px 8px rgba(13,23,63,.04);margin:8px 0 16px 0;}
.card-hook { display:none; }

/* Chips */
.chip {
  display:inline-block; background:var(--chip);
  border:1px solid var(--chip-b); color:var(--chip-ink);
  padding:.25rem .6rem; border-radius:999px; font-size:12px; margin-right:6px;
}

/* Progress chips in sidebar */
.progress-bar{display:flex;flex-direction:column;gap:8px;}
.progress-chip{border:1px solid var(--border);border-radius:10px;padding:.4rem .6rem;font-size:13px;color:#1f2937;background:#fff;}
.progress-chip.active{background:var(--brand);color:var(--brand-ink);border-color:var(--brand);font-weight:600;}

/* Inputs */
/* Radio polish */
[data-testid="stRadio"] div[role="radiogroup"] > div{padding:.25rem .25rem;border-radius:10px;}
[data-testid="stRadio"] div[role="radiogroup"] > div:hover{background:#f8fafc;}
[data-testid="stRadio"] [data-testid="stWidgetLabel"], .stSelectbox label, .stTextInput label {
  font-size:18px!important; font-weight:600; color:#111827; margin:.25rem 0 .35rem 0; display:block;
}
.stRadio > div > label span, [data-testid="stRadio"] div[role="radiogroup"] > div > label span {
  font-size:18px!important;
}
.stRadio > div > label, [data-testid="stRadio"] div[role="radiogroup"] > div > label { line-height:1.5; margin:4px 0; display:block; }

.stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input {
  border:1px solid var(--border); border-radius:12px; padding:.6rem .75rem; font-size:16px;
}
.stMultiSelect [data-baseweb="select"] { border-radius:12px; }

/* Buttons */
[data-testid="baseButton-secondary"], [data-testid="baseButton-primary"], .stButton > button {
  border-radius:12px; padding:.6rem 1rem; border:1px solid var(--border);
  box-shadow:0 1px 2px rgba(16,24,40,.05);
}
.stButton > button{background:#fff;color:#111827;}
.stButton > button:hover { border-color:#d0d5dd; }
/* Primary look when we mark as 'primary' */
button[kind="primary"] { background:var(--brand)!important; color:var(--brand-ink)!important; border-color:var(--brand)!important; }

/* Nav row layout */
.nav-row{display:flex;justify-content:space-between;gap:12px;margin-top:12px;}
.nav-row .left, .nav-row .right { display:flex; gap:8px; }

/* Make default Streamlit elements breathe */
[data-testid="stVerticalBlock"] > div { margin-bottom:12px; }
.content-max{max-width:820px;margin-left:auto;margin-right:auto;}
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
