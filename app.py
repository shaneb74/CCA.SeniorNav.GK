import streamlit as st
import logic

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# --- Global CSS: Outline pill radios (match designer mock) ---
st.markdown("""
<style>
:root{
  --pill-radius:14px; --pill-pad:.55rem 1rem; --pill-gap:.6rem;
  --pill-bg:#fff; --pill-brd:#e5e7eb; --pill-fg:#0f172a;
  --pill-brd-hover:#cbd5e1; --pill-brd-active:#0B5CD8; --pill-fg-active:#0B5CD8;
  --pill-shadow:0 1px 3px rgba(15,23,42,.06);
  --pill-font:14px;
}

/* radio group -> responsive grid of pills */
[data-testid="stRadio"] > div{ gap: var(--pill-gap) !important; }
[data-testid="stRadio"] div[role="radiogroup"]{
  display:grid; gap:var(--pill-gap);
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  align-items:stretch;
}

/* each option is a label; hide the native dot wrapper entirely */
[data-testid="stRadio"] div[role="radiogroup"] > label{
  margin:0 !important; padding:0 !important; display:block; position:relative;
}
/* Streamlit renders: label > div(dot wrapper) + div(text wrapper). Kill the dot wrapper. */
[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child{
  display:none !important;
}

/* visually hide the input but keep it focusable */
[data-testid="stRadio"] input[type="radio"]{
  position:absolute !important; opacity:0 !important; width:1px; height:1px;
  overflow:hidden; clip:rect(0 0 0 0); clip-path: inset(50%);
}

/* make the text wrapper look like a pill bar */
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child{
  display:flex; align-items:center; justify-content:center;
  background:var(--pill-bg); color:var(--pill-fg);
  border:1.5px solid var(--pill-brd); border-radius:var(--pill-radius);
  padding:var(--pill-pad); box-shadow:var(--pill-shadow);
  cursor:pointer; transition:all .12s ease-in-out;
  font-size:var(--pill-font); line-height:1.25; white-space:nowrap;
  user-select:none;
}
[data-testid="stRadio"] div[role="radiogroup"] > label > div:last-child:hover{
  border-color:var(--pill-brd-hover);
}

/* selected state = outline emphasis + brand text color */
[data-testid="stRadio"] input[type="radio"]:checked + div{
  border-color:var(--pill-brd-active) !important; color:var(--pill-fg-active) !important;
  box-shadow:0 1px 6px rgba(11,92,216,.18);
  background:var(--pill-bg);
  font-weight:600;
}

/* keyboard focus-visible ring on the pill */
[data-testid="stRadio"] input[type="radio"]:focus-visible + div{
  outline:3px solid rgba(11,92,216,.25); outline-offset:2px;
}

/* remove accidental blue text selection look */
[data-testid="stRadio"] div[role="radiogroup"] > label::selection,
[data-testid="stRadio"] div[role="radiogroup"] > label *::selection{
  background:transparent; color:inherit;
}

/* Sidebar polish */
section[data-testid="stSidebar"]{background:#f8fafc;border-left:1px solid #e5e7eb}

/* OPTIONAL: switch to filled pills (brand background). Uncomment to use.
[data-testid="stRadio"] input[type="radio"]:checked + div{
  background:#0B5CD8 !important; color:#fff !important; border-color:#0B5CD8 !important;
  box-shadow:0 2px 10px rgba(11,92,216,.25);
  font-weight:600;
}
]*/
</style>
""", unsafe_allow_html=True)

# Initialize session state
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
# Ensure chronic_conditions widget state exists (fixes multiselect flicker)
if "chronic_conditions" not in st.session_state:
    st.session_state.chronic_conditions = []

# Header (always app-level)
st.title("Senior Care Navigator")

# Sidebar QA toggle to keep UI clean
with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

# Delegate flow
logic.run_flow()

# QA drawer at bottom if enabled
if st.session_state.qa_mode:
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.care_context)
