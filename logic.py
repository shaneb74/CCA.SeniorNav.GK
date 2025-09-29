# logic.py
import streamlit as st
from ui.helpers import order_answer_map, radio_from_answer_map

# Helpers
def _to_int(v, default=0):
    try:
        if v is None or v == "":
            return default
        if isinstance(v, (int, float)):
            return int(v)
        s = str(v).replace("$", "").replace(",", "").strip()
        if s == "":
            return default
        return int(float(s))
    except Exception:
        return default

def _g(s, *names, default=0):
    for n in names:
        if n in s and s.get(n) not in (None, ""):
            return s.get(n)
    return default

def _m(n):
    try:
        return f"${int(n):,}"
    except Exception:
        try:
            return f"${float(n):,.0f}"
        except Exception:
            return str(n)

# Shared Context (central data for all components)
care_context = st.session_state.get("care_context", {
    "audience_type": None,  # e.g., "Senior", "Caregiver", "Planner"
    "chronic_conditions": [],
    "care_needs": {},
    "cost_estimates": {},
    "pfma_details": {},
    "tools_exports": []
})

# ### Audiencing Functions (Onboarding/Audience Selection)
def render_audiencing():
    st.header("Audience Selection")
    st.write("Tell us who you are to tailor the experience.")
    audience_type = st.selectbox("I am a:", ["Senior", "Caregiver", "Discharge Planner", "Other"], key="audience_type")
    if audience_type:
        care_context["audience_type"] = audience_type
        st.session_state.care_context = care_context
        st.write(f"Selected: {audience_type}. The app will personalize based on this.")

# ### Guided Care Plan Functions
def render_planner():
    st.header("Guided Care Plan")
    st.write("Assess care needs and conditions.")
    conditions = st.multiselect("Chronic Conditions", ["Diabetes", "Hypertension"], key="planner_conditions")
    care_context["chronic_conditions"] = conditions
    st.session_state.care_context = care_context

# ### Cost Planner Functions
def render_calculator():
    st.header("Cost Planner")
    st.write("Estimate care costs based on needs.")
    # Integrate cost logic (e.g., from pricing_config.json)
    # Example placeholder
    location = st.selectbox("Location", ["National", "Washington"], key="cost_location")
    base_cost = 5500  # From config
    st.write(f"Estimated Cost: {_m(base_cost)}")

# ### PFMA Functions
def render_pfma():
    st.header("Plan for My Advisor")
    st.write("Prepare data for advisor consultation.")
    # Example placeholder
    advisor_notes = st.text_area("Notes for Advisor", key="pfma_notes")
    if advisor_notes:
        care_context["pfma_details"]["notes"] = advisor_notes
        st.session_state.care_context = care_context

# ### AI Agent & Tools Functions
def render_tools():
    st.subheader("AI Agent & Tools")
    st.write("Export data and interact with AI agent.")
    # Tools (exports)
    if st.button("Export CSV"):
        # Placeholder export logic
        st.download_button("Download CSV", "example data", "export.csv")
    # AI Agent Mock
    preset = st.selectbox("AI Preset", ["Close Funding Gap", "Maximize Benefits"], key="ai_preset")
    if st.button("Send to AI Agent"):
        st.success("Mock handoff: " + preset + " processed with care data.")

# Dispatcher
STEP_MAP = {
    "intro": lambda: st.header("Welcome to Senior Navigator"),
    "audiencing": render_audiencing,
    "planner": render_planner,
    "calculator": render_calculator,
    "pfma": render_pfma,
    "tools": render_tools
}

def render_step(step: str):
    """Dispatch to the appropriate step function."""
    func = STEP_MAP.get(step, lambda: st.error(f"Unknown step: {step}"))
    func()
