# app.py
import streamlit as st
from logic import render_step

st.set_page_config(page_title="Senior Navigator • Planner + Cost", page_icon="🧭", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Navigation")
    if st.sidebar.button("Tools & AI Agent", use_container_width=True, key="nav_tools"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "tools"
        st.rerun()
    if st.sidebar.button("Recidivism Tool", use_container_width=True, key="nav_recidivism"):
        st.session_state.return_step = st.session_state.get("step", "intro")
        st.session_state.step = "recidivism"
        st.rerun()

# Main content
render_step(st.session_state.get("step", "intro"))
