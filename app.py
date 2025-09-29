import streamlit as st

# MUST be the first Streamlit call
st.set_page_config(page_title="Senior Navigator", page_icon="🧭", layout="wide")

# Import logic after page config is set
try:
    from logic import render_step
except ImportError as e:
    st.error(f"Failed to import logic module: {e}")
    st.stop()

# Sidebar controls
st.sidebar.title("Settings")
st.session_state.setdefault("show_qa", True)
st.session_state.show_qa = st.sidebar.checkbox(
    "QA View",
    value=st.session_state.show_qa,
    help="Toggle to show or hide the Answers & Flags section",
)

# App title
st.title("Senior Navigator")

# State defaults
st.session_state.setdefault("step", "intro")
st.session_state.setdefault("audiencing_step", 1)
st.session_state.setdefault("planner_step", 1)

# Router
if st.session_state.step == "intro":
    st.header("Welcome to Senior Navigator")
    st.write("This tool helps you plan care based on your needs. Click below to begin.")
    if st.button("Get Started", key="start_planning"):
        st.session_state.step = "audiencing"
        st.session_state.audiencing_step = 1
        st.rerun()
else:
    render_step(st.session_state.step)
