import streamlit as st
try:
    from logic import render_step
except ImportError as e:
    st.error(f"Failed to import logic module: {e}")
    st.stop()

# Set wide layout by default
st.set_page_config(layout="wide")

# Sidebar toggle for QA visibility
st.sidebar.title("Settings")
show_qa = st.sidebar.checkbox("QA View", value=True, help="Toggle to show or hide the Answers & Flags section")

# Main content
st.title("Senior Navigator")
if "step" not in st.session_state:
    st.session_state.step = "intro"
    st.session_state.audiencing_step = 1
    st.session_state.planner_step = 1

if st.session_state.step == "intro":
    st.header("Welcome to Senior Navigator")
    st.write("This tool helps you plan care based on your needs. Click below to begin.")
    if st.button("Get Started", key="start_planning"):
        st.session_state.step = "audiencing"
        st.session_state.audiencing_step = 1
        st.rerun()
else:
    render_step(st.session_state.step)
