import streamlit as st
from logic import render_step

# Set wide layout by default
st.set_page_config(layout="wide")

# Sidebar toggle for QA visibility
st.sidebar.title("Settings")
show_qa = st.sidebar.checkbox("QA View", value=True, help="Toggle to show or hide the Answers & Flags section")

# Main content
st.title("Senior Navigator")
if "step" not in st.session_state:
    st.session_state.step = "intro"

if show_qa or st.session_state.step == "intro":
    render_step(st.session_state.step)
else:
    if st.session_state.step != "intro":
        render_step(st.session_state.step)
