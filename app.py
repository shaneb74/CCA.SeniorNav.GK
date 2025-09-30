import streamlit as st

try:
    from logic import render_step
except ImportError as e:
    st.error(f"Failed to import logic module: {e}")
    st.stop()

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")
st.sidebar.button("Restart All", on_click=lambda: (st.session_state.clear(), st.rerun()))
st.sidebar.checkbox("QA View", value=False, key="show_qa")
if st.sidebar.button("Guided Care Plan"):
    st.session_state.step = "planner"
    st.rerun()

if "step" not in st.session_state:
    st.session_state.step = "intro"
    st.session_state.planner_step = 1

if st.session_state.step == "intro":
    st.title("Senior Navigator")
    st.write("Welcome! Start by exploring your care options.")
    if st.button("Get Started"):
        st.session_state.step = "planner"
        st.session_state.planner_step = 1
        st.rerun()
else:
    render_step(st.session_state.step)
