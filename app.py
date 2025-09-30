import streamlit as st
from . import logic

st.set_page_config(
    page_title="Senior Navigator",
    page_icon="🧭",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# ===== Global styles (desktop-first, no ghost wrappers) =====
STYLES = """
<style>
/* Design system tokens */
:root{--pad:16px;--gap:14px;} .card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:var(--pad);box-shadow:0 1px 2px rgba(0,0,0,.04);} .chip{display:inline-block;background:var(--chip);border:1px solid var(--chip-b);color:var(--chip-ink);padding:.25rem .5rem;border-radius:999px;font-size:12px;margin-right:6px;} .section{margin:24px 0;} .muted{color:var(--muted);} .tight>*{margin-bottom:.5rem;}
:root{
  --brand:#2563eb;        /* accessible indigo */
  --brand-ink:#ffffff;
  --ink:#0f172a;
  --muted:#475569;
  --chip:#eef2ff;
  --chip-b:#dbeafe;
  --chip-ink:#1e3a8a;
  --card:#ffffff;
  --radius:14px;
}

/* Layout: give the main column room and avoid header clipping */
.block-container{
  max-width:1360px;
  padding-top:calc(3.5rem + env(safe-area-inset-top));
}
header[data-testid="stHeader"]{ background:transparent; }
footer{ visibility:hidden; }

/* Type scale */
p,.stMarkdown{ font-size:18px!important; line-height:1.65; color:var(--ink)!important; }
h1{ font-size:44px; margin:0 0 0 .25rem; color:var(--ink); letter-spacing:-.02em; }
h2{ font-size:32px!important; line-height:1.3; margin:.75rem 0 .35rem 0; color:var(--ink); }
h3{ font-size:20px; margin:.5rem 0 .25rem 0; color:var(--ink); }
small,.stCaption{ font-size:15px!important; color:var(--muted); }

/* Card look: style any Streamlit block that contains .card-hook */
.block-container > div:has(.card-hook){
  background:var(--card);
  border:1px solid #eef0f6;
  border-radius:var(--radius);
  padding:20px 22px;
  box-shadow:0 6px 18px rgba(13,23,63,.06);
  margin:4px 0 22px 0;
}

/* Container for consistent button placement */
.card-hook-container {
  min-height: 600px;
  display: flex;
  flex-direction: column;
}
.card-hook-container > div:last-child {
  margin-top: auto;
}

/* Radio prompt + options sizing */
[data-testid="stRadio"] [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] > div,
[data-testid="stWidgetLabel"] p{
  font-size:20px!important; font-weight:600; color:#111827;
  margin:.25rem 0 .35rem 0; display:block;
}
.stRadio > div > label span,
[data-testid="stRadio"] div[role="radiogroup"] > div > label span{
  font-size:20px!important;
}
.stRadio > div > label,
[data-testid="stRadio"] div[role="radiogroup"] > div > label{
  line-height:1.5; margin:4px 0; display:flex; align-items:center;
}

/* Buttons inline, accessible contrast */
.stButton{ display:inline-block; margin-right:12px; }
.stButton > button{
  background:var(--brand)!important; color:var(--brand-ink)!important;
  border:1px solid #cbd5e1!important; border-radius:10px;
  padding:12px 18px; font-size:18px;
}
.stButton > button:hover{ filter:brightness(.95); }
.stButton > button:disabled{ opacity:.55; }

/* Progress chips (sidebar) */
.progress-bar{ display:flex; gap:6px; flex-wrap:wrap; }
.progress-chip{
  font-size:13px; padding:6px 10px; border-radius:999px;
  background:var(--chip); color:var(--chip-ink); border:1px solid var(--chip-b);
}
.progress-chip.active{ background:var(--brand); color:#fff; border-color:var(--brand); }
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# ---- Session bootstrap (lightweight safety) ----
if "care_context" not in st.session_state:
    st.session_state.care_context = {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}}
if "step" not in st.session_state:
    st.session_state.step = "audiencing"  # or "planner" depending on your flow
if "audiencing_step" not in st.session_state:
    st.session_state.audiencing_step = 1
if "planner_step" not in st.session_state:
    st.session_state.planner_step = 1

# ---- Sidebar "Navigation" chips (read-only indicator) ----
if st.session_state.step == "planner":
    labels = ["Funding", "Cognition", "Caregiver", "Meds", "Independence", "Mobility", "Your World", "Home Preference", "Recommendation"]
    active_idx = max(1, min(st.session_state.get("planner_step", 1), len(labels))) - 1
    chips_html = "".join(
        f'<span class="progress-chip {"active" if i==active_idx else ""}">{i+1}. {txt}</span>'
        for i, txt in enumerate(labels)
    )
    st.sidebar.title("Navigation")
    st.sidebar.markdown(f'<div class="progress-bar">{chips_html}</div>', unsafe_allow_html=True)

# ---- Header + content in a real container (no ghost bars) ----
with st.container():
    st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)  # lets CSS style this block as a card

    title = "Senior Care Navigator" if st.session_state.step == "audiencing" else "Guided Care Plan"
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown("<p>Let’s walk through your care needs—one friendly step at a time.</p>", unsafe_allow_html=True)

    # Render the step content
    logic.render_step(st.session_state.step)

# ---- Footer ----
st.markdown(
    "<div style='text-align:center;font-size:13px;margin-top:8px;color:#475569'>"
    "Built with ❤️ to help you navigate care decisions."
    "</div>",
    unsafe_allow_html=True,
)
