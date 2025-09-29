# app.py
import streamlit as st
from logic import render_step

st.set_page_config(page_title="Senior Navigator • Planner + Cost", page_icon="🧭", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("Navigation")
    if st.sidebar.button("Audiencing", use_container_width=True, key="nav_audiencing"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "audiencing"
        st.rerun()
    if st.sidebar.button("Guided Care Plan", use_container_width=True, key="nav_planner"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "planner"
        st.rerun()
    if st.sidebar.button("Cost Planner", use_container_width=True, key="nav_calculator"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "calculator"
        st.rerun()
    if st.sidebar.button("PFMA", use_container_width=True, key="nav_pfma"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "pfma"
        st.rerun()
    if st.sidebar.button("AI Agent & Tools", use_container_width=True, key="nav_tools"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "tools"
        st.rerun()

# Main content
render_step(st.session_state.get("step", "intro"))
