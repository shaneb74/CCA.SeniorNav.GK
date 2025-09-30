import streamlit as st
import logic

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

# --- Global CSS: Horizontal "answer bar" radios ---
st.markdown("""
<style>
:root{
  --bar-radius:12px; --bar-pad:.55rem .9rem; --bar-gap:.5rem;
  --bar-bg:#fff; --bar-bg-hover:#f6f7fb; --bar-bg-active:#0B5CD8;
  --bar-fg:#0f172a; --bar-fg-active:#fff; --bar-brd:#e5e7eb;
  --bar-shadow:0 1px 4px rgba(15,23,42,.06);
  --bar-font:14px;
}

/* make radios render as horizontal, wrapping "answer bars" */
[data-testid="stRadio"] > div{ gap: var(--bar-gap) !important; }
[data-testid="stRadio"] div[role="radiogroup"]{
  display:flex; flex-wrap:wrap; align-items:stretch; gap:var(--bar-gap);
}
[data-testid="stRadio"] div[role="radiogroup"] > label{
  margin:0 !important; padding:0 !important; display:block;
}
[data-testid="stRadio"] div[role="radiogroup"] > div{
  display:flex; align-items:center; justify-content:center;
  background:var(--bar-bg); color:var(--bar-fg);
  border:1px solid var(--bar-brd); border-radius:var(--bar-radius);
  padding:var(--bar-pad); box-shadow:var(--bar-shadow);
  cursor:pointer; transition:all .12s ease-in-out;
  font-size:var(--bar-font); line-height:1.25; white-space:nowrap;
}
[data-testid="stRadio"] div[role="radiogroup"] > div:hover{
  background:var(--bar-bg-hover);
}
[data-testid="stRadio"] input[type="radio"]:checked + div{
  background:var(--bar-bg-active); color:var(--bar-fg-active);
  border-color:var(--bar-bg-active);
  box-shadow:0 2px 10px rgba(11,92,216,.25);
}
[data-testid="stRadio"] input[type="radio"]{
  position:absolute; opacity:0; width:1px; height:1px; overflow:hidden;
}

/* optional: make bars full-width instead of chips
[data-testid="stRadio"] div[role="radiogroup"] > div{ width:100% }
]*/

/* sidebar tidy */
section[data-testid="stSidebar"]{background:#f8fafc;border-left:1px solid #e5e7eb}
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
