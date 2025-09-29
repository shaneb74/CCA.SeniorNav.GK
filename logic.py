import streamlit as st
from ui.helpers import radio_from_answer_map
import random

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
        audience_options_list = list(audience_options.values())
        audience_type_idx = st.radio("Who are you planning for?", audience_options_list, key="audience_type_select", index=0)
        if audience_type_idx is not None:
            audience_type = audience_options_list[audience_type_idx]
            care_context["audience_type"] = audience_type
            care_context["professional_role"] = None
            care_context["relation"] = None
            if audience_type == "Planning as a professional":
                professional_sub_options = {
                    "1": "Discharge planner",
                    "2": "Making a referral"
                }
                professional_sub_options_list = list(professional_sub_options.values())
                sub_type_idx = st.radio("What’s your role?", professional_sub_options_list, key="professional_sub_type", index=0)
                if sub_type_idx is not None:
                    sub_type = professional_sub_options_list[sub_type_idx]
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
            relation_options_list = list(relation_options.values())
            relation_key_idx = st.radio("Who is this person to you?", relation_options_list, key="relation_select", index=0)
            if name and relation_key_idx is not None:
                relation_key = relation_options_list[relation_key_idx]
                care_context["people"] = [name]
                care_context["relation"] = relation_key
                st.session_state.care_context = care_context
                st.write(f"Okay—we’re building this for {name}, who is your {relation_key.lower()}.")
        elif care_context["audience_type"] == "Planning for two people":
            name1 = st.text_input("What’s the first person’s name? (e.g., Mary Smith)", key="person_name1")
            relation1_options = {
                "1": "Myself",
                "2": "Parent",
                "3": "Spouse",
                "4": "Other family member",
                "5": "Friend"
            }
            relation1_options_list = list(relation1_options.values())
            relation1_key_idx = st.radio("Who is the first person to you?", relation1_options_list, key="relation1_select", index=1)
            name2 = st.text_input("What’s the second person’s name? (e.g., Tom Smith)", key="person_name2")
            relation2_options = {
                "1": "Parent",
                "2": "Spouse",
                "3": "Other family member",
                "4": "Friend"
            }
            relation2_options_list = list(relation2_options.values())
            relation2_key_idx = st.radio("Who is the second person to you?", relation2_options_list, key="relation2_select", index=0)
            if name1 and name2 and relation1_key_idx is not None and relation2_key_idx is not None:
                relation1_key = relation1_options_list[relation1_key_idx]
                relation2_key = relation2_options_list[relation2_key_idx]
                care_context["people"] = [name1, name2]
                care_context["relation"] = f"{relation1_key.lower()} and {relation2_key.lower()}"
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

    # QA Drawer at the bottom, out of the way (hidden during Audiencing Step 2)
    if st.session_state.get("step") == "planner" or st.session_state.get("audiencing_step", 1) != 2:
        with st.expander("View Answers & Flags", expanded=False):
            st.write("**Audience Type:**", care_context.get("audience_type", "Not set"))
            st.write("**People:**", ", ".join(care_context.get("people", [])))
            st.write("**Relation:**", care_context.get("relation", "Not set"))
            st.write("**Care Flags:**", {k: v for k, v in care_context.get("care_flags", {}).items() if v})
            st.write("**Derived Flags:**", {k: v for k, v in care_context.get("derived_flags", {}).items() if v})

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
            funding_options_list = list(funding_options.values())
            funding_confidence_idx = st.radio("How confident are you that your savings will cover long-term care?", funding_options_list, key="funding_confidence_select", index=0, help="Note: Medicaid is not Medicare. Medicaid helps with long-term care for those with limited income and assets, while Medicare covers hospital and doctor visits.")
            if funding_confidence_idx is not None:
                funding_confidence = funding_options_list[funding_confidence_idx]
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
            independence_options_list = list(independence_options.values())
            independence_idx = st.radio("How independent are you with daily tasks such as bathing, dressing, and preparing meals?", independence_options_list, key="independence_select", index=0)
            if independence_idx is not None:
                independence = independence_options_list[independence_idx]
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
            st.write("How would you describe your mobility? (e.g., walking, driving, or using rideshare)")
            mobility_options = {
                "1": "I walk easily without any support",
                "2": "I use a cane or walker for longer distances",
                "3": "I need assistance for most movement around the home",
                "4": "I am mostly immobile or need a wheelchair"
            }
            mobility_options_list = list(mobility_options.values())
            mobility_idx = st.radio("How would you describe your mobility?", mobility_options_list, key="mobility_select", index=0)
            if mobility_idx is not None:
                mobility = mobility_options_list[mobility_idx]
                care_context["care_flags"]["mobility_issue"] = mobility != mobility_options_list[0]
                if mobility != mobility_options_list[0]:
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
            social_options_list = list(social_options.values())
            social_idx = st.radio("How often do you feel lonely, down, or socially disconnected?", social_options_list, key="social_select", index=0)
            if social_idx is not None:
                social = social_options_list[social_idx]
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
            caregiver_options_list = list(caregiver_options.values())
            caregiver_idx = st.radio("Do you have a caregiver or family member who can help regularly?", caregiver_options_list, key="caregiver_select", index=0)
            if caregiver_idx is not None:
                caregiver = caregiver_options_list[caregiver_idx]
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
            cognition_options_list = list(cognition_options.values())
            cognition_idx = st.radio("Thinking about your memory and focus, is someone usually around to help you?", cognition_options_list, key="cognition_select", index=0)
            if cognition_idx is not None:
                cognition = cognition_options_list[cognition_idx]
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
            safety_options_list = list(safety_options.values())
            safety_idx = st.radio("How safe do you feel in your home in terms of fall risk, emergencies, or managing on your own?", safety_options_list, key="safety_select", index=0)
            if safety_idx is not None:
                safety = safety_options_list[safety_idx]
                care_context["care_flags"]["falls_risk"] = safety in [safety_options_list[1], safety_options_list[2]]
                st.session_state.care_context = care_context
                st.write(f"Safety: {care_context['care_flags']['falls_risk']}.")
            if st.button("Proceed", key="planner_proceed_7"):
                st.session_state.planner_step = 8
                st.rerun()
            if st.button("Go Back", key="planner_back_7"):
                st.session_state.planner_step = 6
                st.rerun()

        elif st.session_state.planner_step == 8:
            st.subheader("Step 8: Fall History")
            st.write("Have you had a fall recently?")
            fall_options = {
                "1": "Yes",
                "2": "No",
                "3": "Unsure"
            }
            fall_options_list = list(fall_options.values())
            fall_history_idx = st.radio("Have you had a fall in the past six months?", fall_options_list, key="fall_history_select", index=0)
            if fall_history_idx is not None:
                fall_history = fall_options_list[fall_history_idx]
                care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
                st.session_state.care_context = care_context
                st.write(f"Fall history: {care_context['derived_flags'].get('recent_fall', 'Not set')}.")
            if st.button("Proceed", key="planner_proceed_8"):
                st.session_state.planner_step = 9
                st.rerun()
            if st.button("Go Back", key="planner_back_8"):
                st.session_state.planner_step = 7
                st.rerun()

        elif st.session_state.planner_step == 9:
            st.subheader("Step 9: Chronic Conditions")
            st.write("Which chronic conditions do you have?")
            condition_options = ["Diabetes", "Hypertension", "Dementia", "COPD", "CHF", "Arthritis", "Parkinson's", "Stroke"]
            conditions = st.multiselect("Which chronic conditions do you have?", condition_options, key="chronic_conditions_select")
            if conditions:
                care_context["care_flags"]["chronic_conditions"] = conditions
                st.session_state.care_context = care_context
                st.write(f"Chronic conditions: {', '.join(care_context['care_flags']['chronic_conditions'])}.")
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
            goal_options_list = list(goal_options.values())
            goal_idx = st.radio("How important is it for you to stay in your current home?", goal_options_list, key="goal_select", index=0)
            if goal_idx is not None:
                goal = goal_options_list[goal_idx]
                care_context["care_flags"]["living_goal"] = goal
                st.session_state.care_context = care_context
                st.write(f"Home preference: {care_context['care_flags']['living_goal']}.")
            if st.button("Proceed", key="planner_proceed_10"):
                st.session_state.planner_step = 11
                st.rerun()
            if st.button("Go Back", key="planner_back_10"):
                st.session_state.planner_step = 9
                st.rerun()

        elif st.session_state.planner_step == 11:
            st.subheader("Get Your Recommendation")
            if st.button("Get My Care Recommendation"):
                # Recommendation Logic
                st.subheader("Care Recommendation")
                # Default values for robustness
                independence = care_context["care_flags"].get("independence_level", "")
                caregiver = care_context["care_flags"].get("caregiver_support", "Yes, I have someone with me most of the time")
                mobility = care_context["care_flags"].get("mobility_issue", False)
                falls_risk = care_context["care_flags"].get("falls_risk", False)
                cognitive = care_context["care_flags"].get("cognitive_function", "My memory’s sharp, no help needed")
                recent_fall = care_context["derived_flags"].get("recent_fall", False)
                living_goal = care_context["care_flags"].get("living_goal", "Not important—I’m open to other options")
                chronic_conditions = care_context["care_flags"].get("chronic_conditions", [])
                accessibility = care_context["care_flags"].get("accessibility", "I can walk to most of them easily")

                # Initialize mobility_issue with a default
                mobility_issue = "getting around okay" if not mobility else "struggling with movement"

                # Conversational blurbs (5 per condition, empathetic, dynamic)
                in_home_blurbs = [
                    f"We're here for you, {care_context['people'][0]}. With some support at home, you can stay where you feel most comfortable—let's make it safe.",
                    f"It’s okay to need a hand, {care_context['people'][0]}. Staying home is doable with the right help—let’s set that up together.",
                    f"You’re managing well, {care_context['people'][0]}. A little in-home care can keep you rooted—we’ll find the best fit.",
                    f"No need to rush away, {care_context['people'][0]}. With some assistance, home can stay your haven—let’s plan it out.",
                    f"We see your strength, {care_context['people'][0]}. In-home care can ease the load so you stay put—ready to start?",
                ]
                assisted_blurbs = [
                    f"We’re looking out for you, {care_context['people'][0]}. Assisted living offers safety with your mobility challenges—let’s ensure you’re secure.",
                    f"It’s tough to manage alone, {care_context['people'][0]}. Assisted living brings support where you need it most—let’s make the move smooth.",
                    f"Your safety matters, {care_context['people'][0]}. With falls and limited help, assisted living could be your next step—let’s explore it.",
                    f"We’ve got your back, {care_context['people'][0]}. Assisted living fits with your needs—let’s find a place that feels right.",
                    f"You deserve peace, {care_context['people'][0]}. Assisted living can handle the risks—let’s get you settled with care.",
                ]
                memory_blurbs = [
                    f"We’re here, {care_context['people'][0]}. Given your cognitive state, memory care is our recommendation to keep you safe—let’s explore options with more support.",
                    f"It’s alright, {care_context['people'][0]}. With your memory challenges, memory care is best—there may be ways to enhance support further.",
                    f"Your well-being matters, {care_context['people'][0]}. Memory care is advised due to cognitive needs—let’s look into additional care options.",
                    f"We care about you, {care_context['people'][0]}. Your cognitive state points to memory care—additional support could be tailored.",
                    f"You’re not alone, {care_context['people'][0]}. Memory care fits your cognitive needs—let’s find ways to boost that support.",
                ]
                consult_blurbs = [
                    f"We’re with you, {care_context['people'][0]}. Your needs are unique—a specialist will confirm the best path forward.",
                    f"It’s a big choice, {care_context['people'][0]}. A consult will pinpoint the right care—let’s connect you with an expert.",
                    f"You’re doing great, {care_context['people'][0]}. A professional can refine your care plan—let’s get that started.",
                    f"We see the balance, {care_context['people'][0]}. A consult will clarify your options—let’s make it happen together.",
                    f"No rush, {care_context['people'][0]}. An expert will guide us—let’s set up that next step.",
                ]

                # Memory Care (highest priority if cognitive issues or dementia with no support)
                if ((cognitive in ["Noticeable problems, and support's always there", "Noticeable problems, and I'm mostly on my own"] or
                     "Dementia" in chronic_conditions) and
                    caregiver in ["Infrequently—someone checks in occasionally", "No regular caregiver or support available"]):
                    recommendation = "Memory Care"
                    blurb = random.choice(memory_blurbs)
                    st.write(f"**Recommendation:** {recommendation}")
                    if living_goal in ["Very important—I strongly want to stay home", "Somewhat important—I’d prefer to stay but could move"]:
                        st.write(f"{blurb} Given your cognitive state and lack of support, memory care is essential—let’s explore enhanced care options.")
                    else:
                        st.write(f"{blurb} With your cognitive needs and no regular help, memory care is the safest choice—let’s look into more support.")

                # In-Home Care (only if no cognitive/memory risk and viable support)
                elif (independence in ["I need help with some of these tasks regularly", "I rely on someone else for most daily tasks"] and
                      caregiver in ["Infrequently—someone checks in occasionally", "No regular caregiver or support available"] and
                      living_goal in ["Very important—I strongly want to stay home", "Somewhat important—I’d prefer to stay but could move"] and
                      cognitive not in ["Noticeable problems, and support's always there", "Noticeable problems, and I'm mostly on my own"] and
                      "Dementia" not in chronic_conditions and
                      accessibility in ["I can walk to most of them easily", "I can drive or get a ride with little trouble"]):
                    recommendation = "In-Home Care"
                    blurb = random.choice(in_home_blurbs)
                    st.write(f"**Recommendation:** {recommendation}")
                    st.write(f"{blurb} With {mobility_issue} and limited help, in-home support can work, especially with nearby services.")

                # Assisted Living (only if no cognitive/memory risk and safety concerns)
                elif (mobility and falls_risk and
                      caregiver in ["Infrequently—someone checks in occasionally", "No regular caregiver or support available"] and
                      living_goal in ["Not important—I’m open to other options", "Unsure"] and
                      cognitive not in ["Noticeable problems, and support's always there", "Noticeable problems, and I'm mostly on my own"] and
                      "Dementia" not in chronic_conditions):
                    recommendation = "Assisted Living"
                    blurb = random.choice(assisted_blurbs)
                    if living_goal == "Very important—I strongly want to stay home":
                        st.write(f"**Recommendation:** {recommendation}")
                        st.write(f"{blurb} Your safety’s the priority with falls and {mobility_issue}—this is the safest option now.")
                    else:
                        st.write(f"**Recommendation:** {recommendation}")
                        st.write(f"{blurb} Since you’re {mobility_issue} and help is sparse, especially in a remote area, this keeps you secure.")

                st.write(f"**Details:** Based on your answers, we suggest {recommendation}.")

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
