import streamlit as st

try:
    from logic import render_step
except ImportError as e:
    st.error(f"Failed to import logic module: {e}")
    st.stop()

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")
if st.sidebar.button("QA View"):
    st.session_state.step = "qa"
    st.rerun()
if st.sidebar.button("Guided Care Plan"):
    st.session_state.step = "planner"
    st.rerun()
if st.sidebar.button("Cost Planner"):
    st.session_state.step = "cost_planner"
    st.rerun()
if st.sidebar.button("Plan for My Advisor"):
    st.session_state.step = "advisor"
    st.rerun()

if "step" not in st.session_state:
    st.session_state.step = "intro"
    st.session_state.audiencing_step = 1
    st.session_state.planner_step = 1

if st.session_state.step == "intro":
    st.title("Senior Navigator")
    st.write("Welcome! Start by exploring your options.")
    if st.button("Get Started"):
        st.session_state.step = "audiencing"
        st.session_state.audiencing_step = 1
        st.rerun()
else:
    render_step(st.session_state.step)
