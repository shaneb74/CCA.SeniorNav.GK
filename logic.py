import streamlit as st

# Shared Context
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {}
    }

care_context = st.session_state.care_context

# ### Audiencing Functions
def render_audiencing():
    st.header("Who Are We Planning For?")
    st.write("Let’s start by understanding your planning needs.")
    if "audiencing_step" not in st.session_state:
        st.session_state.audiencing_step = 1

    if st.session_state.audiencing_step == 1:
        st.subheader("Step 1: Select Planning Context")
        audience_options = {
            "1": "Planning for one person",
            "2": "Planning for two people",
            "3": "Professional planning"
        }
        audience_type = st.radio("Select planning type:", [audience_options["1"], audience_options["2"], audience_options["3"]], key="audience_type_select", index=0)
        if audience_type:
            care_context["audience_type"] = audience_type
            care_context["professional_role"] = None
            if audience_type == "Professional planning":
                professional_sub_options = {
                    "1": "Discharge planner",
                    "2": "Making a referral"
                }
                sub_type = st.radio("Professional role:", [professional_sub_options["1"], professional_sub_options["2"]], key="professional_sub_type", index=0)
                care_context["professional_role"] = sub_type
            elif audience_type == "Planning for one person":
                care_context["people"] = ["Person A"]
            else:  # Two people
                care_context["people"] = ["Person A", "Person B"]
            st.session_state.care_context = care_context
            st.write(f"Planning for: {', '.join(care_context['people'])} as {care_context.get('professional_role', 'self')}")
        if st.button("Next", key="audiencing_next_1"):
            st.session_state.audiencing_step = 2
            st.rerun()

    if st.session_state.audiencing_step == 2:
        st.subheader("Step 2: Confirm and Proceed")
        st.write(f"Confirmed: Planning for {', '.join(care_context['people'])} as {care_context.get('professional_role', 'self')}.")
        if st.button("Proceed to Guided Care Plan", key="audiencing_proceed"):
            st.session_state.step = "planner"
            st.session_state.audiencing_step = 1  # Reset for next use
            st.rerun()

# ### Guided Care Plan Functions
def render_planner():
    st.header("Guided Care Plan")
    st.write("Let’s walk through these questions to understand your care needs.")
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1

    if st.session_state.planner_step == 1:
        st.subheader("Step 1: Financial Confidence")
        funding_options = {
            "1": "Very confident",
            "2": "Somewhat confident",
            "3": "Unsure",
            "4": "Already on Medicaid"
        }
        funding_confidence = st.radio("How confident are you that your savings will cover long-term care?", [funding_options["1"], funding_options["2"], funding_options["3"], funding_options["4"]], key="funding_confidence_select", index=0)
        if funding_confidence:
            care_context["care_flags"]["funding_confidence"] = funding_confidence
            st.session_state.care_context = care_context
            if funding_confidence == "Already on Medicaid":
                st.write("We can connect you to Medicaid-friendly care options-just tap here.", unsafe_allow_html=True)
                if st.button("Get Options", key="medicaid_options"):
                    st.session_state.step = "tools"
                    st.rerun()
            st.write(f"Funding confidence: {care_context['care_flags']['funding_confidence']}")
        if st.button("Next", key="planner_next_1"):
            st.session_state.planner_step = 2
            st.rerun()

    elif st.session_state.planner_step == 2:
        st.subheader("Step 2: Living Situation")
        living_options = {
            "1": "Alone",
            "2": "With spouse",
            "3": "With family",
            "4": "In a facility"
        }
        living_sit = st.radio("Where do you currently live?", [living_options["1"], living_options["2"], living_options["3"], living_options["4"]], key="living_sit")
        if living_sit:
            care_context["care_flags"]["living_situation"] = living_sit
            prior_facility = st.radio("Have you been in assisted living, memory care, or skilled nursing before?", ["Yes", "No", "Not applicable"], key="prior_facility")
            if prior_facility == "Yes":
                care_context["derived_flags"]["prior_facility_experience"] = True
            st.session_state.care_context = care_context
        if st.button("Next", key="planner_next_2"):
            st.session_state.planner_step = 3
            st.rerun()

    elif st.session_state.planner_step == 3:
        st.subheader("Step 3: Support Network")
        support_options = {
            "1": "Daily",
            "2": "Weekly",
            "3": "Rarely",
            "4": "None"
        }
        support = st.radio("How often do you get help from family or friends?", [support_options["1"], support_options["2"], support_options["3"], support_options["4"]], key="support_select")
        if support:
            care_context["care_flags"]["support_network_weak"] = support in ["Rarely", "None"]
            st.session_state.care_context = care_context
        if st.button("Next", key="planner_next_3"):
            st.session_state.planner_step = 4
            st.rerun()

    elif st.session_state.planner_step == 4:
        st.subheader("Step 4: Mobility")
        mobility_options = {
            "1": "None",
            "2": "Cane",
            "3": "Walker",
            "4": "Wheelchair"
        }
        mobility = st.radio("What kind of mobility support do you use?", [mobility_options["1"], mobility_options["2"], mobility_options["3"], mobility_options["4"]], key="mobility_select")
        if mobility:
            care_context["care_flags"]["mobility_issue"] = mobility != "None"
            if mobility != "None":
                care_context["derived_flags"]["inferred_mobility_aid"] = mobility
            fall_history = st.radio("Have you had a fall in the past six months?", ["Yes", "No", "Unsure"], key="fall_history")
            if fall_history == "Yes":
                care_context["derived_flags"]["recent_fall"] = True
            st.session_state.care_context = care_context
        if st.button("Next", key="planner_next_4"):
            st.session_state.planner_step = 5
            st.rerun()

    elif st.session_state.planner_step == 5:
        st.subheader("Step 5: Home Safety")
        safety_options = {
            "1": "Safe",
            "2": "Some concerns",
            "3": "Unsafe"
        }
        safety = st.radio("How safe is your home?", [safety_options["1"], safety_options["2"], safety_options["3"]], key="safety_select")
        if safety:
            care_context["care_flags"]["falls_risk"] = safety in ["Some concerns", "Unsafe"]
            st.session_state.care_context = care_context
        if st.button("Next", key="planner_next_5"):
            st.session_state.planner_step = 6
            st.rerun()

    elif st.session_state.planner_step == 6:
        st.subheader("Step 6: Chronic Conditions")
        conditions = st.multiselect("Which chronic conditions do you have?", ["Diabetes", "Hypertension", "Dementia"], key="chronic_conditions")
        if conditions:
            care_context["care_flags"]["chronic_conditions"] = conditions
            st.session_state.care_context = care_context
        if st.button("Next", key="planner_next_6"):
            st.session_state.planner_step = 7
            st.rerun()

    elif st.session_state.planner_step == 7:
        st.subheader("Step 7: Goals")
        goal_options = {
            "1": "Stay home",
            "2": "Assisted living",
            "3": "Memory care",
            "4": "Unsure"
        }
        goal = st.radio("What is your preferred living arrangement?", [goal_options["1"], goal_options["2"], goal_options["3"], goal_options["4"]], key="goal_select")
        if goal:
            care_context["care_flags"]["living_goal"] = goal
            st.session_state.care_context = care_context
        if st.button("Finish", key="planner_finish"):
            st.session_state.step = "calculator"
            st.session_state.planner_step = 1
            st.rerun()

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
