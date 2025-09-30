import streamlit as st
import logic

st.set_page_config(
    page_title="Senior Care Navigator",
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

# Header (always app-level)
st.title("Senior Care Navigator")

# QA toggle
st.checkbox("QA view", key="qa_mode")

# Delegate flow
logic.run_flow()

# QA drawer at bottom if enabled
if st.session_state.qa_mode:
    st.markdown("---")
    st.subheader("QA Data")
    st.json(st.session_state.care_context)
