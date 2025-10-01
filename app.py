import streamlit as st
from guided_care_plan.engine import render as render_careplan
from pathlib import Path

st.set_page_config(page_title="Senior Care Navigator", layout="centered")

def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)
    else:
        st.warning(f"Missing CSS: {path}")

# Load external CSS
inject_css("static/style.css")

with st.sidebar:
    st.checkbox("QA view", key="qa_mode")

st.title("Senior Care Navigator")

# Progress rail
total_steps = 12
step = st.session_state.get("planner_step", 0)
if 1 <= step <= total_steps:
    segs = ''.join(
        f'<div class="seg{" active" if i < step else ""}"></div>'
        for i in range(total_steps)
    )
    rail = f'<div class="progress-rail">{segs}</div>'
    st.markdown(rail, unsafe_allow_html=True)

# Hand off to Guided Care Plan
render_careplan()

# Optional QA block
if st.session_state.get("qa_mode"):
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.get("care_context", {}))
