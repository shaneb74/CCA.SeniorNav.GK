import streamlit as st
from ui.helpers import radio_from_answer_map

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
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "funding_confidence": None,
        "care_flags": {},
        "derived_flags": {}
    }

care_context = st.session_state.care_context

# ### Audiencing Functions
def render_audiencing():
    st.header("Who Are We Planning For?")
    st.write("Let’s start by understanding your planning needs.")
    # Audience selection
    audience_options = {
        "1": "Planning for one person",
        "2": "Planning for two people",
        "3": "Professional planning"
    }
    audience_type = radio_from_answer_map("Select planning type:", audience_options, key="audience_type_select", default_key="1")
    if audience_type:
        care_context["audience_type"] = audience_options[audience_type]
        if audience_type == "3":
            professional_sub_options = {
                "1": "Discharge planner",
                "2": "Making a referral"
            }
            sub_type = radio_from_answer_map("Professional role:", professional_sub_options, key="professional_sub_type", default_key="1")
            care_context["professional_role"] = professional_sub_options[sub_type]
        elif audience_type == "1":
            care_context["people"] = ["Person A"]
        else:  # Two people
            care_context["people"] = ["Person A", "Person B"]
        st.session_state.care_context = care_context
        st.write(f"Planning for: {', '.join(care_context['people'])} as {care_context.get('professional_role', 'self')}")
    # Funding confidence (first question with Medicaid off-ramp)
    funding_options = {
        "1": "Very confident (self-fund for years)",
        "2": "Somewhat confident (assets/insurance, but worried)",
        "3": "Unsure - might need help",
        "4": "Already on Medicaid"
    }
    funding_confidence = radio_from_answer_map("How confident are you that your savings and income can cover long-term care?", funding_options, key="funding_confidence_select", default_key="1")
    if funding_confidence:
        care_context["funding_confidence"] = funding_options[funding_confidence]
        st.session_state.care_context = care_context
        if funding_confidence == "4":  # Medicaid
            st.write("We can connect you to Medicaid-friendly care options-just tap here.", unsafe_allow_html=True)
            if st.button("Get Options", key="medicaid_options"):
                st.session_state.step = "tools"
                st.rerun()
        st.write(f"Funding confidence: {care_context['funding_confidence']}")
    # Proceed
    if st.button("Proceed to Guided Care Plan", key="audiencing_next"):
        st.session_state.step = "planner"
        st.rerun()

# ### Guided Care Plan Functions
def render_planner():
    st.header("Guided Care Plan")
    st.write("Answer these questions to assess care needs and set recommendations.")
    # Initialize flags for the session
    if "care_flags" not in care_context:
        care_context["care_flags"] = {}
    if "derived_flags" not in care_context:
        care_context["derived_flags"] = {}

    # Question 1: Living Situation
    living_options = {"1": "Alone", "2": "With spouse", "3": "With family", "4": "In a facility"}
    living_sit = radio_from_answer_map("Where do you currently live?", living_options, key="living_sit")
    if living_sit:
        care_context["care_flags"]["living_situation"] = living_options[living_sit]
        prior_facility = st.radio("Have you lived in assisted living, memory care, or skilled nursing before?", ["Yes", "No", "Not applicable"], key="prior_facility")
        if prior_facility == "Yes":
            care_context["derived_flags"]["prior_facility_experience"] = True
        st.session_state.care_context = care_context

    # Question 2: Chronic Conditions
    conditions = st.multiselect("Which chronic conditions do you have? (Select all that apply)", ["Diabetes", "Hypertension", "Dementia"], key="chronic_conditions")
    if conditions:
        care_context["care_flags"]["chronic_conditions"] = conditions
        st.session_state.care_context = care_context

    # Question 3: Daily Activities (ADLs)
    adl_options = ["Bathing", "Dressing", "Eating", "Toileting"]
    adls = st.multiselect("Which daily activities require assistance? (Select all that apply)", adl_options, key="adls")
    if adls:
        care_context["care_flags"]["adl_support_needed"] = len(adls) > 0
        if len(adls) >= 2:
            care_context["derived_flags"]["adl_support"] = "high"
        st.session_state.care_context = care_context

    # Question 4: Mobility
    mobility_options = {"1": "None", "2": "Cane", "3": "Walker", "4": "Wheelchair"}
    mobility = radio_from_answer_map("What mobility aid do you use, if any?", mobility_options, key="mobility_select")
    if mobility:
        care_context["care_flags"]["mobility_issue"] = mobility_options[mobility] != "None"
        if mobility_options[mobility] != "None":
            care_context["derived_flags"]["inferred_mobility_aid"] = mobility_options[mobility]
        fall_history = st.radio("Have you fallen in the past 6 months?", ["Yes", "No", "Unsure"], key="fall_history")
        if fall_history == "Yes":
            care_context["derived_flags"]["recent_fall"] = True
        st.session_state.care_context = care_context

    # Question 5: Safety
    safety_options = {"1": "Safe", "2": "Some concerns", "3": "Unsafe"}
    safety = radio_from_answer_map("How safe do you feel at home (stairs, hazards)?", safety_options, key="safety_select")
    if safety:
        care_context["care_flags"]["falls_risk"] = safety_options[safety] in ["Some concerns", "Unsafe"]
        st.session_state.care_context = care_context

    # Question 6: Support Network
    support_options = {"1": "Daily", "2": "Weekly", "3": "Rarely", "4": "None"}
    support = radio_from_answer_map("How often do you get help from family or friends?", support_options, key="support_select")
    if support:
        care_context["care_flags"]["support_network_weak"] = support_options[support] in ["Rarely", "None"]
        if care_context["care_flags"]["living_situation"] == "Alone" and support_options[support] == "None":
            care_context["derived_flags"]["no_support"] = True
        st.session_state.care_context = care_context

    # Question 7: Goals
    goal_options = {"1": "Stay home", "2": "Assisted living", "3": "Memory care", "4": "Unsure"}
    goal = radio_from_answer_map("What is your preferred living arrangement?", goal_options, key="goal_select")
    if goal:
        care_context["care_flags"]["living_goal"] = goal_options[goal]
        st.session_state.care_context = care_context

    # Question 8: Tech Comfort
    tech_options = {"1": "Comfortable", "2": "Basic", "3": "Uncomfortable"}
    tech = radio_from_answer_map("How comfortable are you with technology (phone, video)?", tech_options, key="tech_select")
    if tech:
        care_context["care_flags"]["tech_comfort"] = tech_options[tech]
        st.session_state.care_context = care_context

    # Question 9: Finances Confidence (re-asked for context)
    funding_options = {
        "1": "Very confident (self-fund for years)",
        "2": "Somewhat confident (assets/insurance, but worried)",
        "3": "Unsure - might need help",
        "4": "Already on Medicaid"
    }
    funding_confidence = radio_from_answer_map("How confident are you that your savings and income can cover long-term care?", funding_options, key="funding_confidence_plan")
    if funding_confidence:
        care_context["care_flags"]["funding_confidence"] = funding_options[funding_confidence]
        if funding_confidence == "4":  # Medicaid
            st.write("We can connect you to Medicaid-friendly care options-just tap here.", unsafe_allow_html=True)
            if st.button("Get Options", key="medicaid_options_plan"):
                st.session_state.step = "tools"
                st.rerun()
        st.session_state.care_context = care_context

    # Recommendation Engine Hook (placeholder - assumes existing engine function)
    if all(key in care_context["care_flags"] for key in ["living_situation", "chronic_conditions", "adl_support_needed", "mobility_issue", "falls_risk", "support_network_weak", "living_goal", "tech_comfort", "funding_confidence"]):
        care_flags = {k: v for k, v in care_context["care_flags"].items() if k in ["living_situation", "chronic_conditions", "adl_support_needed", "mobility_issue", "falls_risk", "support_network_weak", "living_goal", "tech_comfort", "funding_confidence"]}
        # Placeholder for recommendation engine call (replace with actual function)
        # from engines import PlannerEngine
        # engine = PlannerEngine("config/question_answer_logic.json", "config/recommendation_logic.json")
        # rec = engine.run(care_flags)
        st.write("Recommendation engine would process here with flags:", care_flags)

# Dispatcher
STEP_MAP = {
    "intro": lambda: st.header("Welcome to Senior Navigator"),
    "audiencing": render_audiencing,
    "planner": render_planner
}

def render_step(step: str):
    """Dispatch to the appropriate step function."""
    func = STEP_MAP.get(step, lambda: st.error(f"Unknown step: {step}"))
    func()
