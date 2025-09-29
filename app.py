import streamlit as st
from logic import render_step

st.set_page_config(page_title="Senior Navigator", layout="wide")

# Sidebar navigation
with st.sidebar:
    st.title("Steps")
    if st.sidebar.button("Audiencing", use_container_width=True, key="nav_audiencing"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "audiencing"
        st.rerun()
    if st.sidebar.button("Guided Care Plan", use_container_width=True, key="nav_planner"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "planner"
        st.rerun()

# Main content
render_step(st.session_state.get("step", "intro"))
