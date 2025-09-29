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

# Shared Context
care_context = st.session_state.get("care_context", {
    "chronic_conditions": [],
    "care_needs": {},
    "discharge_date": None,
    "follow_up_schedule": {},
    "follow_up_services": []
})

# ### Guided Care Plan Functions
def render_planner():
    st.header("Guided Care Plan")
    st.write("Assess care needs and conditions.")
    # Placeholder - will use question_answer_logic.json
    conditions = st.multiselect("Chronic Conditions", ["Diabetes", "Hypertension"], key="planner_conditions")
    care_context["chronic_conditions"] = conditions
    st.session_state.care_context = care_context

# ### Cost Estimator Functions
def render_calculator():
    st.header("Cost Estimator")
    st.write("Estimate care costs based on needs.")
    # Placeholder - will integrate cost_controls.py

# ### PFMA Functions
def render_pfma():
    st.header("Plan for My Advisor")
    st.write("Prepare data for advisor consultation.")
    # Placeholder - will integrate pfma_controls.py

# ### Tools Functions
def render_tools():
    st.subheader("Tools & Export Options")
    s = st.session_state
    income_total = _to_int(_g(s, "income_total")) or (_to_int(_g(s, "inc_A")) + _to_int(_g(s, "inc_B")) + _to_int(_g(s, "inc_house")))
    care_total = _to_int(_g(s, "care_total", "care_monthly_total"))
    gap = care_total - income_total
    st.write(f"Income: {_m(income_total)}, Costs: {_m(care_total)}, Gap: {_m(gap)}")
    # Add exports and AI mock later

# ### Recidivism Tool Functions
def render_recidivism():
    st.header("Recidivism Support Tool")
    st.write("Coordinate post-discharge care to reduce readmissions.")
    # Access shared data
    conditions = care_context.get("chronic_conditions", [])
    st.write(f"Chronic Conditions: {conditions}")
    # Discharge and follow-up inputs
    discharge_date = st.date_input("Discharge Date", value=None, key="recidivism_discharge")
    follow_up_date = st.date_input("Next Follow-Up Date", value=None, key="recidivism_followup")
    care_context["discharge_date"] = discharge_date
    care_context["follow_up_schedule"]["next"] = follow_up_date
    st.session_state.care_context = care_context
    # Risk assessment
    if conditions and not follow_up_date:
        st.warning("No follow-up scheduled—risk of recidivism may increase.")
    # Service coordination
    services = st.session_state.get("recidivism_services", ["Home Health", "Transportation", "Meal Delivery"])
    selected_services = st.multiselect("Select Follow-Up Services", services, key="recidivism_services_select")
    if selected_services:
        care_context["follow_up_services"] = selected_services
        st.session_state.care_context = care_context
        st.write(f"Selected Services: {selected_services}")

# Dispatcher
STEP_MAP = {
    "intro": lambda: st.header("Welcome to Senior Navigator"),
    "planner": render_planner,
    "calculator": render_calculator,
    "pfma": render_pfma,
    "tools": render_tools,
    "recidivism": render_recidivism
}

def render_step(step: str):
    """Dispatch to the appropriate step function."""
    func = STEP_MAP.get(step, lambda: st.error(f"Unknown step: {step}"))
    func()
