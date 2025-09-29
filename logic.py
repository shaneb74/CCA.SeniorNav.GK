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
        st.subheader("Step 1: Who Are You Planning For?")
        audience_options = {
            "1": "Planning for one person",
            "2": "Planning for two people",
            "3": "Planning as a professional"
        }
        audience_type = st.radio("Who are you planning for?", [audience_options["1"], audience_options["2"], audience_options["3"]], key="audience_type_select", index=0)
        if audience_type:
            care_context["audience_type"] = audience_type
            care_context["professional_role"] = None
            if audience_type == "Planning as a professional":
                professional_sub_options = {
                    "1": "Discharge planner",
                    "2": "Making a referral"
                }
                sub_type = st.radio("What’s your role?", [professional_sub_options["1"], professional_sub_options["2"]], key="professional_sub_type", index=0)
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
        st.subheader("Step 2: Name Capture")
        st.write("Great—let’s make it personal. Who are we helping?")
        if care_context["audience_type"] in ["Planning for one person", "Planning for two people"]:
            if care_context["audience_type"] == "Planning for one person":
                name = st.text_input("What’s their name? (First and last, e.g., John Doe)", key="person_name")
                if name:
                    care_context["people"] = [name]
            else:  # Two people
                name1 = st.text_input("What’s the first person’s name? (e.g., Mary Smith)", key="person_name1")
                name2 = st.text_input("What’s the second person’s name? (e.g., Tom Smith)", key="person_name2")
                if name1 and name2:
                    care_context["people"] = [name1, name2]
            st.session_state.care_context = care_context
            if care_context["people"]:
                st.write(f"Okay—we’re building this for {', '.join(care_context['people'])} as {care_context.get('professional_role', 'yourself or a loved one')}.")
        elif care_context["audience_type"] == "Planning as a professional":
            client_name = st.text_input("Client name (optional, e.g., Jane Doe)", key="client_name")
            if client_name:
                care_context["people"] = [client_name]
            else:
                care_context["people"] = ["Client"]
            st.session_state.care_context = care_context
            st.write(f"Okay—we’re building this for {', '.join(care_context['people'])} as {care_context.get('professional_role')}.")
        if st.button("Proceed to Guided Care Plan", key="audiencing_proceed"):
            if care_context["people"]:
                st.session_state.step = "planner"
                st.session_state.audiencing_step = 1  # Reset for next use
                st.rerun()

# ### Guided Care Plan Functions
def render_planner():
    st.header("Guided Care Plan")
    st.write("Let’s walk through a few questions to understand your care needs.")
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1

    # QA Drawer
    with st.expander("View Answers & Flags", expanded=False):
        st.write("**Audience Type:**", care_context.get("audience_type", "Not set"))
        st.write("**People:**", ", ".join(care_context.get("people", [])))
        for flag_type in ["care_flags", "derived_flags"]:
            st.write(f"**{flag_type.replace('_', ' ').title()}:**", care_context.get(flag_type, {}))

    # Step-based question rendering
    if st.session_state.planner_step == 1:
        with st.container():
            st.subheader("Step 1: Financial Confidence")
            st.write("We know these choices can weigh heavy. Let’s start with where you stand on covering care.")
            funding_options = {
                "1": "Not worried—I can cover any care I need",
                "2": "Somewhat worried—I’d need to budget carefully",
                "3": "Very worried—cost is a big concern for me",
                "4": "I am on Medicaid"
            }
            funding_confidence = st.radio("Are you worried about covering the costs of care?", [funding_options["1"], funding_options["2"], funding_options["3"], funding_options["4"]], key="funding_confidence_select", index=0, help="Select the option that best reflects your financial situation.")
            if funding_confidence:
                care_context["care_flags"]["funding_confidence"] = funding_confidence
                st.session_state.care_context = care_context
                if funding_confidence == "I am on Medicaid":
                    st.write("We can connect you to Medicaid-friendly care options—just tap here.", unsafe_allow_html=True)
                    if st.button("Get Options", key="medicaid_options"):
                        st.session_state.step = "tools"
                        st.rerun()
                st.write(f"You feel: {care_context['care_flags']['funding_confidence']}.")
            if st.button("Proceed", key="planner_proceed_1"):
                st.session_state.planner_step = 2
                st.rerun()
            if st.button("Go Back", key="planner_back_1", disabled=True):
                pass  # Disabled on first step

    elif st.session_state.planner_step == 2:
        with st.container():
            st.subheader("Step 2: Daily Independence & Mobility")
            st.write("Let’s get a sense of how you or your loved one manage daily life and getting around.")
            independence_options = {
                "1": "I’m fully independent and handle all tasks on my own",
                "2": "I occasionally need reminders or light assistance",
                "3": "I need help with some of these tasks regularly",
                "4": "I rely on someone else for most daily tasks"
            }
            independence = st.radio("How independent are you with daily tasks such as bathing, dressing, and preparing meals?", [independence_options["1"], independence_options["2"], independence_options["3"], independence_options["4"]], key="independence_select", index=0)
            if independence:
                care_context["care_flags"]["independence_level"] = independence
                st.session_state.care_context = care_context
            mobility_options = {
                "1": "I walk easily without any support",
                "2": "I use a cane or walker for longer distances",
                "3": "I need assistance for most movement around the home",
                "4": "I am mostly immobile or need a wheelchair"
            }
            mobility = st.radio("How would you describe your mobility?", [mobility_options["1"], mobility_options["2"], mobility_options["3"], mobility_options["4"]], key="mobility_select", index=0)
            if mobility:
                care_context["care_flags"]["mobility_issue"] = mobility != mobility_options["1"]
                if mobility != mobility_options["1"]:
                    care_context["derived_flags"]["inferred_mobility_aid"] = mobility
                st.session_state.care_context = care_context
            st.write(f"Independence: {care_context['care_flags'].get('independence_level', 'Not set')}, Mobility: {care_context['care_flags'].get('mobility_issue', 'Not set')}")
            if st.button("Proceed", key="planner_proceed_2"):
                st.session_state.planner_step = 3
                st.rerun()
            if st.button("Go Back", key="planner_back_2"):
                st.session_state.planner_step = 1
                st.rerun()

    elif st.session_state.planner_step == 3:
        with st.container():
            st.subheader("Step 3: Social Connection & Caregiver Support")
            st.write("Let’s think about how you’re feeling and who’s there to help.")
            social_options = {
                "1": "Rarely—I’m socially active and feel good most days",
                "2": "Sometimes—I connect weekly but have some down moments",
                "3": "Often—I feel isolated or down much of the time"
            }
            social = st.radio("How often do you feel lonely, down, or socially disconnected?", [social_options["1"], social_options["2"], social_options["3"]], key="social_select", index=0)
            if social:
                care_context["care_flags"]["social_disconnection"] = social
                st.session_state.care_context = care_context
            caregiver_options = {
                "1": "Yes, I have someone with me most of the time",
                "2": "Yes, I have support a few days a week",
                "3": "Infrequently—someone checks in occasionally",
                "4": "No regular caregiver or support available"
            }
            caregiver = st.radio("Do you have a caregiver or family member who can help regularly?", [caregiver_options["1"], caregiver_options["2"], caregiver_options["3"], caregiver_options["4"]], key="caregiver_select", index=0)
            if caregiver:
                care_context["care_flags"]["caregiver_support"] = caregiver
                st.session_state.care_context = care_context
            st.write(f"Social Connection: {care_context['care_flags'].get('social_disconnection', 'Not set')}, Caregiver Support: {care_context['care_flags'].get('caregiver_support', 'Not set')}")
            if st.button("Proceed", key="planner_proceed_3"):
                st.session_state.planner_step = 4
                st.rerun()
            if st.button("Go Back", key="planner_back_3"):
                st.session_state.planner_step = 2
                st.rerun()

    elif st.session_state.planner_step == 4:
        with st.container():
            st.subheader("Step 4: Cognitive Function & Home Safety")
            st.write("Let’s check in on memory and how safe things feel at home.")
            cognition_options = {
                "1": "My memory’s sharp, no help needed",
                "2": "Slight forgetfulness, but someone helps daily",
                "3": "Noticeable problems, and support’s always there",
                "4": "Noticeable problems, and I’m mostly on my own"
            }
            cognition = st.radio("Thinking about your memory and focus, is someone usually around to help you?", [cognition_options["1"], cognition_options["2"], cognition_options["3"], cognition_options["4"]], key="cognition_select", index=0)
            if cognition:
                care_context["care_flags"]["cognitive_function"] = cognition
                st.session_state.care_context = care_context
            safety_options = {
                "1": "Very safe—I have everything I need",
                "2": "Mostly safe, but a few things concern me",
                "3": "Sometimes I feel unsafe or unsure"
            }
            safety = st.radio("How safe do you feel in your home in terms of fall risk, emergencies, or managing on your own?", [safety_options["1"], safety_options["2"], safety_options["3"]], key="safety_select", index=0)
            if safety:
                care_context["care_flags"]["falls_risk"] = safety in [safety_options["2"], safety_options["3"]]
                st.session_state.care_context = care_context
            st.write(f"Cognitive Function: {care_context['care_flags'].get('cognitive_function', 'Not set')}, Safety: {care_context['care_flags'].get('falls_risk', 'Not set')}")
            if st.button("Proceed", key="planner_proceed_4"):
                st.session_state.planner_step = 5
                st.rerun()
            if st.button("Go Back", key="planner_back_4"):
                st.session_state.planner_step = 3
                st.rerun()

    elif st.session_state.planner_step == 5:
        with st.container():
            st.subheader("Step 5: Accessibility & Goals")
            st.write("Let’s look at how easy it is to get around and what you’d like for the future.")
            accessibility_options = {
                "1": "I can walk to most of them easily",
                "2": "I can drive or get a ride with little trouble",
                "3": "It’s difficult to get to these places without help",
                "4": "I have no easy access and need assistance to get anywhere"
            }
            accessibility = st.radio("How accessible are services like pharmacies, grocery stores, and doctor’s offices from your home?", [accessibility_options["1"], accessibility_options["2"], accessibility_options["3"], accessibility_options["4"]], key="accessibility_select", index=0)
            if accessibility:
                care_context["care_flags"]["accessibility"] = accessibility
                st.session_state.care_context = care_context
            goal_options = {
                "1": "Stay home",
                "2": "Assisted living",
                "3": "Memory care",
                "4": "Unsure"
            }
            goal = st.radio("What is your preferred living arrangement?", [goal_options["1"], goal_options["2"], goal_options["3"], goal_options["4"]], key="goal_select", index=0)
            if goal:
                care_context["care_flags"]["living_goal"] = goal
                if goal == "Stay home":
                    care_context["derived_flags"]["in_home_care_modification"] = True
                    st.write("Considering staying home? We can suggest modifications like ramps or grab bars in the Cost Planner.")
                else:
                    care_context["derived_flags"]["in_home_care_modification"] = False
                    if goal == "Unsure":
                        st.write("On the fence between assisted living and in-home care? Check the Cost Planner for options to stay home longer.")
                st.session_state.care_context = care_context
            st.write(f"Accessibility: {care_context['care_flags'].get('accessibility', 'Not set')}, Living Goal: {care_context['care_flags'].get('living_goal', 'Not set')}, In-Home Mod: {care_context['derived_flags'].get('in_home_care_modification', 'Not set')}")
            if st.button("Finish", key="planner_finish"):
                st.session_state.step = "calculator"
                st.session_state.planner_step = 1
                st.rerun()
            if st.button("Go Back", key="planner_back_5"):
                st.session_state.planner_step = 4
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
