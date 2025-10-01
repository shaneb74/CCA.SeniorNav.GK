
import streamlit as st
from typing import List

try:
    from core.utils.session import get_session, save_session  # type: ignore
except Exception:
    def get_session():
        if "case" not in st.session_state:
            st.session_state["case"] = {}
        return st.session_state["case"]
    def save_session(obj):
        st.session_state["case"] = obj

st.set_page_config(page_title="Planning Hub", layout="centered")
st.title("Plan the next steps")

ss = get_session()
assessment = ss.get("assessment_snapshot", {})
recos = [v.get("recommendation") for v in assessment.values()]
reco_text = ", ".join(sorted(set([r for r in recos if r])) ) or "Not started"

def small_badge(text: str):
    st.markdown(f"**{text}**")

def primary(text: str) -> bool:
    return st.button(text, use_container_width=False)

# Card 1 — Understand the situation
with st.container(border=True):
    st.caption("Understand the situation")
    st.subheader("Guided Care Plan")
    st.caption("Recommendation")
    st.write(reco_text)
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("See responses"):
            # Try to route to your existing GCP page
            candidates = [
                "pages/01_Guided_Care_Plan.py",
                "app/pages/01_Guided_Care_Plan.py",
                "pages/Guided_Care_Plan.py",
                "app/pages/Guided_Care_Plan.py",
            ]
            for p in candidates:
                try:
                    st.switch_page(p)
                    break
                except Exception:
                    continue
    with col2:
        st.button("Start over", disabled=True)
    with col3:
        st.markdown("Completed ✅" if assessment else "Not started")

st.write("")

# Card 2 — Understand the costs
with st.container(border=True):
    st.caption("Understand the costs")
    st.subheader("Cost Estimator")
    st.caption("Assess the cost structure for various care options. The estimate updates based on your choices.")
    left, right = st.columns([1,1])
    with left:
        if st.button("Start"):
            # Navigate to the Guided module selection (next page we ship)
            try:
                st.switch_page("pages/01_Cost_Modules_Selection.py")
            except Exception:
                try:
                    st.switch_page("app/pages/01_Cost_Modules_Selection.py")
                except Exception:
                    st.warning("Could not open the module selection page. Use the sidebar to find it.")
    with right:
        st.caption("Next step ✱")

st.write("")

# Card 3 — Connect with an advisor
with st.container(border=True):
    st.caption("Connect with an advisor to plan the care")
    st.subheader("Get Connected")
    st.caption("Whenever you're ready to meet with an advisor.")
    if st.button("Get connected"):
        # Try to route to PFMA or booking page if present
        candidates = [
            "pages/04_PFMA.py",
            "app/pages/04_PFMA.py",
            "pages/PFMA.py",
            "app/pages/PFMA.py",
        ]
        for p in candidates:
            try:
                st.switch_page(p)
                break
            except Exception:
                continue

st.write("")

# Card 4 — FAQs & Answers
with st.container(border=True):
    st.caption("FAQs & Answers")
    st.subheader("AI Agent")
    st.caption("Receive instant, tailored assistance from our advanced AI chat.")
    if st.button("Open"):
        candidates = [
            "pages/05_AI_Agent.py",
            "app/pages/05_AI_Agent.py",
            "pages/AI_Agent.py",
            "app/pages/AI_Agent.py",
        ]
        for p in candidates:
            try:
                st.switch_page(p)
                break
            except Exception:
                continue
