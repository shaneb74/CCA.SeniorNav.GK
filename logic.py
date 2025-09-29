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
            care_context["relation"] = None
            if audience_type == "Planning as a professional":
                professional_sub_options = {
                    "1": "Discharge planner",
                    "2": "Making a referral"
                }
                sub_type = st.radio("What’s your role?", [professional_sub_options["1"], professional_sub_options["2"]], key="professional_sub_type", index=0)
                care_context["professional_role"] = sub_type
            st.session_state.care_context = care_context
            st.write(f"Planning for: {care_context.get('audience_type', 'not specified yet')} as {care_context.get('professional_role', 'self')}")
        if st.button("Next", key="audiencing_next_1"):
            st.session_state.audiencing_step = 2
            st.rerun()

    if st.session_state.audiencing_step == 2:
        st.subheader("Step 2: Name and Relation")
        st.write("Great—let’s make it personal. Who are we helping?")
        if care_context["audience_type"] == "Planning for one person":
            name = st.text_input("What’s their name? (First and last, e.g., John Doe)", key="person_name")
            relation_options = {
                "1": "Myself",
                "2": "Parent",
                "3": "Spouse",
                "4": "Other family member",
                "5": "Friend"
            }
            relation_key = radio_from_answer_map("Who is this person to you?", relation_options, key="relation_select", default_key="1")
            if name and relation_key:
                care_context["people"] = [name]
                care_context["relation"] = relation_options[relation_key]
                st.session_state.care_context = care_context
                st.write(f"Okay—we’re building this for {name}, who is your {relation_options[relation_key].lower()}.")
        elif care_context["audience_type"] == "Planning for two people":
            name1 = st.text_input("What’s the first person’s name? (e.g., Mary Smith)", key="person_name1")
            relation1_options = {
                "1": "Myself",
                "2": "Parent",
                "3": "Spouse",
                "4": "Other family member",
                "5": "Friend"
            }
            relation1_key = radio_from_answer_map("Who is the first person to you?", relation1_options, key="relation1_select", default_key="2")
            name2 = st.text_input("What’s the second person’s name? (e.g., Tom Smith)", key="person_name2")
            relation2_options = {
                "1": "Parent",
                "2": "Spouse",
                "3": "Other family member",
                "4": "Friend"
            }
            relation2_key = radio_from_answer_map("Who is the second person to you?", relation2_options, key="relation2_select", default_key="1")
            if name1 and name2 and relation1_key and relation2_key:
                care_context["people"] = [name1, name2]
                care_context["relation"] = f"{relation1_options[relation1_key].lower()} and {relation2_options[relation2_key].lower()}"
                st.session_state.care_context = care_context
                st.write(f"Okay—we’re building this for {name1} and {name2}, who are your {care_context['relation']}.")
        elif care_context["audience_type"] == "Planning as a professional":
            client_name = st.text_input("Client name (optional, e.g., Jane Doe)", key="client_name")
            if client_name:
                care_context["people"] = [client_name]
            else:
                care_context["people"] = ["Client"]
            st.session_state.care_context = care_context
            st.write(f"Okay—we’re building this for {', '.join(care_context['people'])} as {care_context.get('professional_role')}.")
        if st.button("Proceed to Guided Care Plan", key="audiencing_proceed"):
            if (care_context["audience_type"] == "Planning for one person" and care_context["people"] and care_context["relation"]) or \
               (care_context["audience_type"] == "Planning for two people" and len(care_context["people"]) == 2 and care_context["relation"]) or \
               (care_context["audience_type"] == "Planning as a professional"):
                st.session_state.step = "planner"
                st.session_state.audiencing_step = 1  # Reset for next use
                st.rerun()

# ### Guided Care Plan Functions
def render_planner():
    st.header("Guided Care Plan")
    st.write("Let’s walk through a few questions to understand your care needs.")
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1

    # QA Drawer at the bottom, out of the way
    with st.expander("View Answers & Flags", expanded=False):
        st.write("**Audience Type:**", care_context.get("audience_type", "Not set"))
        st.write("**People:**", ", ".join(care_context.get("people", [])))
        st.write("**Relation:**", care_context.get("relation", "Not set"))
        for flag_type in ["care_flags", "derived_flags"]:
            st.write(f"**{flag_type.replace('_', ' ').title()}:**", care_context.get(flag_type, {}))

    # Step-based question rendering in a frame
    with st.container():
        if st.session_state.planner_step == 1:
            st.subheader("Step 1: Financial Confidence")
            st.write("Are you worried about covering the costs of care?")
            funding_options = {
                "1": "Not worried—I can cover any care I need",
                "2": "Somewhat worried—I’d need to budget carefully",
                "3": "Very worried—cost is a big concern for me",
                "4": "I am on Medicaid"
            }
            funding_confidence = st.radio("How confident are you that your savings will cover long-term care?", [funding_options["1"], funding_options["2"], funding_options["3"], funding_options["4"]], key="funding_confidence_select", index=0, help="Note: Medicaid is not Medicare. Medicaid helps with long-term care for those with limited income and assets, while Medicare covers hospital and doctor visits.")
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
                pass

        elif st.session_state.planner_step == 2:
            st.subheader("Step 2: Daily Independence")
            st.write("How independent are you with daily tasks?")
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
                st.write(f"Independence level: {care_context['care_flags']['independence_level']}.")
            if st.button("Proceed", key="planner_proceed_2"):
                st.session_state.planner_step = 3
                st.rerun()
            if st.button("Go Back", key="planner_back_2"):
                st.session_state.planner_step = 1
                st.rerun()

        elif st.session_state.planner_step == 3:
            st.subheader("Step 3: Mobility")
            st.write("How would you describe your mobility?")
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
                st.write(f"Mobility: {care_context['care_flags']['mobility_issue']}.")
            if st.button("Proceed", key="planner_proceed_3"):
                st.session_state.planner_step = 4
                st.rerun()
            if st.button("Go Back", key="planner_back_3"):
                st.session_state.planner_step = 2
                st.rerun()

        elif st.session_state.planner_step == 4:
            st.subheader("Step 4: Social Connection")
            st.write("How often do you feel lonely, down, or socially disconnected?")
            social_options = {
                "1": "Rarely—I’m socially active and feel good most days",
                "2": "Sometimes—I connect weekly but have some down moments",
                "3": "Often—I feel isolated or down much of the time"
            }
            social = st.radio("How often do you feel lonely, down, or socially disconnected?", [social_options["1"], social_options["2"], social_options["3"]], key="social_select", index=0)
            if social:
                care_context["care_flags"]["social_disconnection"] = social
                st.session_state.care_context = care_context
                st.write(f"Social connection: {care_context['care_flags']['social_disconnection']}.")
            if st.button("Proceed", key="planner_proceed_4"):
                st.session_state.planner_step = 5
                st.rerun()
            if st.button("Go Back", key="planner_back_4"):
                st.session_state.planner_step = 3
                st.rerun()

        elif st.session_state.planner_step == 5:
            st.subheader("Step 5: Caregiver Support")
            st.write("Do you have a caregiver or family member who can help regularly?")
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
                st.write(f"Caregiver support: {care_context['care_flags']['caregiver_support']}.")
            if st.button("Proceed", key="planner_proceed_5"):
                st.session_state.planner_step = 6
                st.rerun()
            if st.button("Go Back", key="planner_back_5"):
                st.session_state.planner_step = 4
                st.rerun()

        elif st.session_state.planner_step == 6:
            st.subheader("Step 6: Cognitive Function")
            st.write("Thinking about your memory and focus, is someone usually around to help you?")
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
                st.write(f"Cognitive function: {care_context['care_flags']['cognitive_function']}.")
            if st.button("Proceed", key="planner_proceed_6"):
                st.session_state.planner_step = 7
                st.rerun()
            if st.button("Go Back", key="planner_back_6"):
                st.session_state.planner_step = 5
                st.rerun()

        elif st.session_state.planner_step == 7:
            st.subheader("Step 7: Home Safety")
            st.write("How safe do you feel in your home?")
            safety_options = {
                "1": "Very safe—I have everything I need",
                "2": "Mostly safe, but a few things concern me",
                "3": "Sometimes I feel unsafe or unsure"
            }
            safety = st.radio("How safe do you feel in your home in terms of fall risk, emergencies, or managing on your own?", [safety_options["1"], safety_options["2"], safety_options["3"]], key="safety_select", index=0)
            if safety:
                care_context["care_flags"]["falls_risk"] = safety in [safety_options["2"], safety_options["3"]]
                st.session_state.care_context = care_context
                st.write(f"Safety: {care_context['care_flags']['falls_risk']}.")
            if st.button("Proceed", key="planner_proceed_7"):
                st.session_state.planner_step = 8
                st.rerun()
            if st.button("Go Back", key="planner_back_7"):
                st.session_state.planner_step = 6
                st.rerun()

        elif st.session_state.planner_step == 8:
            st.subheader("Step 8: Chronic Conditions")
            st.write("Which chronic conditions do you have?")
            condition_options = ["Diabetes", "Hypertension", "Dementia", "COPD", "CHF", "Arthritis", "Parkinson's", "Stroke"]
            conditions = st.multiselect("Which chronic conditions do you have?", condition_options, key="chronic_conditions_select")
            if conditions:
                care_context["care_flags"]["chronic_conditions"] = conditions
                st.session_state.care_context = care_context
                st.write(f"Chronic conditions: {', '.join(care_context['care_flags']['chronic_conditions'])}.")
            if st.button("Proceed", key="planner_proceed_8"):
                st.session_state.planner_step = 9
                st.rerun()
            if st.button("Go Back", key="planner_back_8"):
                st.session_state.planner_step = 7
                st.rerun()

        elif st.session_state.planner_step == 9:
            st.subheader("Step 9: Accessibility")
            st.write("How accessible are services from your home?")
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
                st.write(f"Accessibility: {care_context['care_flags']['accessibility']}.")
            if st.button("Proceed", key="planner_proceed_9"):
                st.session_state.planner_step = 10
                st.rerun()
            if st.button("Go Back", key="planner_back_9"):
                st.session_state.planner_step = 8
                st.rerun()

        elif st.session_state.planner_step == 10:
            st.subheader("Step 10: Home Preference")
            st.write("How important is it for you to stay in your current home?")
            goal_options = {
                "1": "Not important—I’m open to other options",
                "2": "Somewhat important—I’d prefer to stay but could move",
                "3": "Very important—I strongly want to stay home"
            }
            goal = st.radio("How important is it for you to stay in your current home?", [goal_options["1"], goal_options["2"], goal_options["3"]], key="goal_select", index=0)
            if goal:
                care_context["care_flags"]["living_goal"] = goal
                st.session_state.care_context = care_context
                st.write(f"Home preference: {care_context['care_flags']['living_goal']}.")
            if st.button("Finish", key="planner_finish"):
                st.session_state.step = "calculator"
                st.session_state.planner_step = 1
                st.rerun()
            if st.button("Go Back", key="planner_back_10"):
                st.session_state.planner_step = 9
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
