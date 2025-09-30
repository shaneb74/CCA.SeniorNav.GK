import streamlit as st
from .questions import QUESTIONS

def _q_header(title: str):
    st.markdown(f"<div class='q-title'>{title}</div>", unsafe_allow_html=True)

def run_flow():
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 0
    if "care_context" not in st.session_state:
        st.session_state.care_context = {"flags": {}}

    step = st.session_state.planner_step

    # Step 0
    if step == 0:
        st.markdown("<div class='intro-head'>Welcome to Senior Care Navigator</div>", unsafe_allow_html=True)
        st.markdown("<div class='intro-body'>We make navigating senior care simple. Answer a few quick questions and we’ll connect you with the best options, backed by expert guidance — always free for families.</div>", unsafe_allow_html=True)
        st.markdown("<div class='q-prompt'>Who are you planning care for today?</div>", unsafe_allow_html=True)
        st.session_state.care_context["audience_type"] = st.radio("", ["One person", "Two people", "Professional"], index=0)
        if st.button("Next", type="primary"):
            st.session_state.planner_step = 1
            st.rerun()
        return

    # Step 1..n simplified
    if 1 <= step <= len(QUESTIONS):
        key, prompt, options, bullets = QUESTIONS[step - 1]
        _q_header(f"Step {step}: {prompt}")
        st.radio("", options, key=f"q_{key}")
        if st.button("Next", type="primary"):
            st.session_state.planner_step = step + 1
            st.rerun()
