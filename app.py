import streamlit as st
import logic


st.set_page_config(page_title="Senior Navigator", page_icon="🧭", layout="wide")

st.markdown('''
<style>
/* ----- Layout ----- */
.block-container { max-width: 900px; padding-top: 0.5rem; }

/* Typographic scale */
:root { --body: 18px; --muted: 15px; --h1: 44px; --h2: 30px; --h3: 22px; }
p, .stMarkdown { font-size: var(--body) !important; line-height: 1.65; color: #222; }
h1 { font-size: var(--h1); letter-spacing: -0.02em; margin: 0 0 .25rem 0; }
h2 { font-size: var(--h2); letter-spacing: -0.01em; margin: .75rem 0 .35rem 0; }
h3 { font-size: var(--h3); margin: .5rem 0 .25rem 0; }
small, .stCaption, .st-emotion-cache-1wbqy5l { font-size: var(--muted) !important; color: #666; }

/* Cards (for section grouping, subtle) */
.section-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 1px 1px rgba(0,0,0,0.02);
  margin: 8px 0 18px 0;
}

/* Radio: prompt/label */
[data-testid="stRadio"] [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] {
  font-size: 20px !important;
  font-weight: 600;
  color: #222;
  margin: 0.25rem 0 0.35rem 0;
  display: block;
}
/* In some Streamlit builds the text is wrapped */
[data-testid="stWidgetLabel"] > div,
[data-testid="stWidgetLabel"] p { font-size: 20px !important; margin: 0; }

/* Radio: options */
.stRadio > div > label span,
[data-testid="stRadio"] div[role="radiogroup"] > div > label span {
  font-size: 20px !important;
}
.stRadio > div > label,
[data-testid="stRadio"] div[role="radiogroup"] > div > label {
  line-height: 1.5;
  margin: 4px 0;
  display: flex; align-items: center;
}

/* Buttons */
.stButton > button {
  background-color: #1f6feb; color: #fff;
  border: none; border-radius: 10px;
  padding: 12px 18px; font-size: 18px;
}
.stButton > button:disabled { opacity: 0.5; }

/* Progress chips */
.progress-bar { display: flex; gap: 6px; flex-wrap: wrap; margin: 6px 0 10px 0; }
.progress-chip {
  font-size: 13px; padding: 6px 10px; border-radius: 999px;
  background: #f3f6ff; color: #2a3a6b; border: 1px solid #dbe5ff;
}
.progress-chip.active { background: #1f6feb; color: #fff; border-color: #1f6feb; }

</style>
''', unsafe_allow_html=True)

# Session state bootstrap used by logic
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {}
    }

if "step" not in st.session_state:
    st.session_state.step = "planner"

if "planner_step" not in st.session_state:
    st.session_state.planner_step = 1

# Top heading (kept outside cards for hierarchy)
st.header("Guided Care Plan")
st.write("Let’s walk through your care needs.")

# Lightweight progress chips driven by current step
labels = [
    "Funding", "Cognition", "Caregiver", "Meds",
    "Independence", "Mobility", "Your World",
    "Home Preference", "Recommendation"
]
active_idx = max(1, min(st.session_state.get("planner_step", 1), len(labels))) - 1
chips = "".join(
    f'<span class="progress-chip {"active" if i==active_idx else ""}">{i+1}. {txt}</span>'
    for i, txt in enumerate(labels)
)
st.markdown(f'<div class="progress-bar">{chips}</div>', unsafe_allow_html=True)

# Main card wrapper for form sections
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    # Delegate to the app logic
    logic.render_step(st.session_state.step)
    st.markdown('</div>', unsafe_allow_html=True)
