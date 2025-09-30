import streamlit as st

try:
    from logic import render_step, run_tests
except ImportError as e:
    st.error(f"Failed to import logic module: {e}")
    st.stop()

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")
st.sidebar.checkbox("QA View", value=False, key="show_qa")
if st.sidebar.button("Guided Care Plan"):
    st.session_state.step = "planner"
    st.rerun()
st.sidebar.button("Run Test Cases", key="debug_tests", on_click=lambda: run_tests())

if "step" not in st.session_state:
    st.session_state.step = "intro"
    st.session_state.planner_step = 1

if st.session_state.step == "intro":
    st.title("Senior Navigator")
    st.write("Welcome! Start by exploring your options.")
    if st.button("Get Started"):
        st.session_state.step = "planner"
        st.session_state.planner_step = 1
        st.rerun()
else:
    render_step(st.session_state.step)
