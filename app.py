import streamlit as st
import logic  # presentation-only wrapper; business logic lives in logic.py

# Desktop-friendly canvas
st.set_page_config(page_title="Senior Navigator", page_icon="🧭", layout="wide")

# ===== Global visual treatment (no logic) =====
st.markdown(
    """
<style>
/* ----- Layout: responsive desktop-first ----- */
.block-container {
  max-width: 1280px;                       /* wide for desktop */
  padding-top: calc(3.5rem + env(safe-area-inset-top));  /* avoid toolbar clip */
}
@media (min-width: 1500px) { .block-container { max-width: 1400px; } }

/* Typography */
:root { --body: 18px; --muted: 15px; --h1: 44px; --h2: 30px; --h3: 22px; }
p, .stMarkdown { font-size: var(--body) !important; line-height: 1.65; color: #1f2937; }
h1 { font-size: var(--h1); letter-spacing: -0.02em; margin: 0 0 .25rem 0; }
h2 { font-size: var(--h2); letter-spacing: -0.01em; margin: .75rem 0 .35rem 0; }
h3 { font-size: var(--h3); margin: .5rem 0 .25rem 0; }
small, .stCaption { font-size: var(--muted) !important; color: #6b7280; }

/* Cards for the form sections */
.section-card {
  background: #fff; border: 1px solid #e5e7eb; border-radius: 14px;
  padding: 18px 20px; box-shadow: 0 1px 1px rgba(0,0,0,0.02);
  margin: 8px 0 18px 0;
}

/* Softer accessible palette */
:root {
  --primary: #2563eb;       /* indigo-600: accessible blue */
  --primary-100: #eef2ff;   /* chip bg */
  --primary-700: #1d4ed8;   /* hover */
  --primary-900: #1e3a8a;   /* chip text */
}

/* Radio prompt (the question line) */
[data-testid="stRadio"] [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] > div,
[data-testid="stWidgetLabel"] p {
  font-size: 20px !important; font-weight: 600; color: #111827;
  margin: .25rem 0 .35rem 0; display: block;
}

/* Radio options */
.stRadio > div > label span,
[data-testid="stRadio"] div[role="radiogroup"] > div > label span {
  font-size: 20px !important;
}
.stRadio > div > label,
[data-testid="stRadio"] div[role="radiogroup"] > div > label {
  line-height: 1.5; margin: 4px 0; display: flex; align-items: center;
}

/* Buttons: inline, softer blue, white text */
.stButton { display: inline-block; margin-right: 12px; }
.stButton > button {
  background-color: var(--primary); color: #fff;
  border: none; border-radius: 10px; padding: 12px 18px; font-size: 18px;
}
.stButton > button:hover { background-color: var(--primary-700); }
.stButton > button:disabled { opacity: 0.55; }

/* Progress chips */
.progress-bar { display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0 10px 0; }
.progress-chip {
  font-size: 13px; padding: 6px 10px; border-radius: 999px;
  background: var(--primary-100); color: var(--primary-900); border: 1px solid #dbeafe;
}
.progress-chip.active { background: var(--primary); color: #fff; border-color: var(--primary); }
</style>
""",
    unsafe_allow_html=True,
)

# ===== Header (main column) =====
st.header("Guided Care Plan")
st.write("Let’s walk through your care needs.")

# ===== Left navigation: progress chips in sidebar (no step-jumping logic) =====
labels = [
    "Funding", "Cognition", "Caregiver", "Meds",
    "Independence", "Mobility", "Your World",
    "Home Preference", "Recommendation",
]
active_idx = max(1, min(st.session_state.get("planner_step", 1), len(labels))) - 1
chips_html = "".join(
    f'<span class="progress-chip {"active" if i == active_idx else ""}">{i+1}. {txt}</span>'
    for i, txt in enumerate(labels)
)
st.sidebar.title("Navigation")
st.sidebar.markdown(f'<div class="progress-bar">{chips_html}</div>', unsafe_allow_html=True)

# ===== Content card =====
st.markdown('<div class="section-card">', unsafe_allow_html=True)
logic.render_step(st.session_state.get("step", "planner"))
st.markdown("</div>", unsafe_allow_html=True)
