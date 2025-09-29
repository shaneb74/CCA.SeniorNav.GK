import streamlit as st
from logic import render_step

# Sidebar toggle for QA visibility
st.sidebar.title("Settings")
show_qa = st.sidebar.checkbox("QA View", value=True)
st.set_page_config(page_title="Senior Navigator", layout="wide")

# Main content
st.title("Senior Navigator")
if show_qa:
    render_step(st.session_state.get("step", "intro"))
else:
    if st.session_state.get("step", "intro") != "intro":
        render_step(st.session_state.get("step", "intro"))
