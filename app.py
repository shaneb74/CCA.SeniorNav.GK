import streamlit as st
import logic

st.set_page_config(
    page_title="Senior Navigator – Guided Care Plan",
    layout="centered"
)

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
        "chronic_conditions": []
    }

care_context = st.session_state.care_context

# Header
st.title("Guided Care Plan")

# QA toggle
st.checkbox("QA view", key="qa_mode")

# Navigation flow
logic.run_flow()

# QA drawer at bottom if enabled
if st.session_state.qa_mode:
    st.markdown("---")
    st.subheader("QA Data")
    st.json(care_context)
