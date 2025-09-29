import streamlit as st
from ui.helpers import radio_from_answer_map
import random
import unicodedata
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {}
    }
care_context = st.session_state.care_context
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
        audience_type = st.radio("Who are you planning for?", audience_options_list, key="audience_type_select")
        if audience_type:
            care_context["audience_type"] = audience_type
            care_context["professional_role"] = None
            care_context["relation"] = None
            if audience_type == "Planning as a professional":
                professional_sub_options = {
                    "1": "Discharge planner",
                    "2": "Making a referral"
                }
                professional_sub_options_list = list(professional_sub_options.values())
                sub_type = st.radio("What’s your role?", professional_sub_options_list, key="professional_sub_type")
                if sub_type:
                    care_context["professional_role"] = sub_type
            st.session_state.care_context = care_context
            st.write(f"Planning for: {care_context.get('audience_type', 'not specified yet')} as {care_context.get('professional_role', 'self')}")
        if st.button("Next", key="audiencing_next_1", disabled=not audience_type):
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
            relation_key = st.radio("Who is this person to you?", relation_options_list, key="relation_select")
            if name and relation_key:
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
            relation1_key = st.radio("Who is the first person to you?", relation1_options_list, key="relation1_select")
            name2 = st.text_input("What’s the second person’s name? (e.g., Tom Smith)", key="person_name2")
            relation2_options = {
                "1": "Parent",
                "2": "Spouse",
                "3": "Other family member",
                "4": "Friend"
            }
            relation2_options_list = list(relation2_options.values())
            relation2_key = st.radio("Who is the second person to you?", relation2_options_list, key="relation2_select")
            if name1 and name2 and relation1_key and relation2_key:
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
            st.write(f"Okay—we’re building this for {', '.join(care_context['people'])} as {care_context.get('professional_role')}")
        if st.button("Proceed to Guided Care Plan", key="audiencing_proceed", disabled=not (care_context.get("audience_type") and care_context.get("people") and care_context.get("relation"))):
            if (care_context["audience_type"] == "Planning for one person" and care_context["people"] and care_context["relation"]) or (care_context["audience_type"] == "Planning for two people" and len(care_context["people"]) == 2 and care_context["relation"]) or (care_context["audience_type"] == "Planning as a professional"):
                st.session_state.step = "planner"
                st.session_state.audiencing_step = 1
                st.rerun()
def render_planner():
    st.header("Guided Care Plan")
    st.write("Let’s walk through a few questions to understand your care needs.")
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1
    if st.session_state.get("step") == "planner" and st.session_state.get("show_qa", True):
        with st.expander("View Answers & Flags", expanded=False):
            st.write("**Audience Type:**", care_context.get("audience_type", "Not set"))
            st.write("**People:**", ", ".join(care_context.get("people", [])))
            st.write("**Relation:**", care_context.get("relation", "Not set"))
            st.write("**Care Flags:**", {k: v for k, v in care_context.get("care_flags", {}).items() if v})
            st.write("**Derived Flags:**", {k: v for k, v in care_context.get("derived_flags", {}).items() if v})
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
            funding_confidence = st.radio("How confident are you that your savings will cover long-term care?", funding_options_list, key="funding_confidence_select")
            if funding_confidence:
                care_context["care_flags"]["funding_confidence"] = funding_confidence
                st.session_state.care_context = care_context
                if funding_confidence == "I am on Medicaid":
                    st.write("We can connect you to Medicaid-friendly care options—just tap here.", unsafe_allow_html=True)
                    if st.button("Get Options", key="medicaid_options"):
                        st.session_state.step = "tools"
                        st.rerun()
                st.write(f"You feel: {care_context['care_flags']['funding_confidence']}")
            if st.button("Proceed", key="planner_proceed_1", disabled=not funding_confidence):
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
            independence = st.radio("How independent are you with daily tasks such as bathing, dressing, and preparing meals?", independence_options_list, key="independence_select")
            if independence:
                care_context["care_flags"]["independence_level"] = independence
                st.session_state.care_context = care_context
                st.write(f"Independence level: {care_context['care_flags']['independence_level']}")
            if st.button("Proceed", key="planner_proceed_2", disabled=not independence):
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
            mobility = st.radio("How would you describe your mobility?", mobility_options_list, key="mobility_select")
            if mobility:
                care_context["care_flags"]["mobility_issue"] = mobility != mobility_options_list[0]
                if mobility != mobility_options_list[0]:
                    care_context["derived_flags"]["inferred_mobility_aid"] = mobility
                st.session_state.care_context = care_context
                st.write(f"Mobility: {care_context['care_flags']['mobility_issue']}")
            if st.button("Proceed", key="planner_proceed_3", disabled=not mobility):
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
            social = st.radio("How often do you feel lonely, down, or socially disconnected?", social_options_list, key="social_select")
            if social:
                care_context["care_flags"]["social_disconnection"] = social
                st.session_state.care_context = care_context
                st.write(f"Social connection: {care_context['care_flags']['social_disconnection']}")
            if st.button("Proceed", key="planner_proceed_4", disabled=not social):
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
            caregiver = st.radio("Do you have a caregiver or family member who can help regularly?", caregiver_options_list, key="caregiver_select")
            if caregiver:
                care_context["care_flags"]["caregiver_support"] = caregiver
                st.session_state.care_context = care_context
                st.write(f"Caregiver support: {care_context['care_flags']['caregiver_support']}")
            if st.button("Proceed", key="planner_proceed_5", disabled=not caregiver):
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
            cognition = st.radio("Thinking about your memory and focus, is someone usually around to help you?", cognition_options_list, key="cognition_select")
            if cognition:
                care_context["care_flags"]["cognitive_function"] = cognition
                st.session_state.care_context = care_context
                st.write(f"Cognitive function: {care_context['care_flags']['cognitive_function']}")
            if st.button("Proceed", key="planner_proceed_6", disabled=not cognition):
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
            safety = st.radio("How safe do you feel in your home in terms of fall risk, emergencies, or managing on your own?", safety_options_list, key="safety_select")
            if safety:
                care_context["care_flags"]["falls_risk"] = safety in [safety_options_list[1], safety_options_list[2]]
                st.session_state.care_context = care_context
                st.write(f"Safety: {care_context['care_flags']['falls_risk']}")
            if st.button("Proceed", key="planner_proceed_7", disabled=not safety):
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
            fall_history = st.radio("Have you had a fall in the past six months?", fall_options_list, key="fall_history_select")
            if fall_history:
                care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
                st.session_state.care_context = care_context
                st.write(f"Fall history: {care_context['derived_flags'].get('recent_fall', 'Not set')}")
            if st.button("Proceed", key="planner_proceed_8", disabled=not fall_history):
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
                st.write(f"Chronic conditions: {', '.join(care_context['care_flags']['chronic_conditions'])}")
            if st.button("Proceed", key="planner_proceed_9", disabled=not conditions):
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
            goal = st.radio("How important is it for you to stay in your current home?", goal_options_list, key="goal_select")
            if goal:
                care_context["care_flags"]["living_goal"] = goal
                st.session_state.care_context = care_context
                st.write(f"Home preference: {care_context['care_flags']['living_goal']}")
            if st.button("Proceed", key="planner_proceed_10", disabled=not goal):
                st.session_state.planner_step = 11
                st.rerun()
            if st.button("Go Back", key="planner_back_10"):
                st.session_state.planner_step = 9
                st.rerun()
        elif st.session_state.planner_step == 11:
            st.subheader("Get Your Recommendation")
            if st.button("Get My Care Recommendation"):
                st.subheader("Care Recommendation")
                def _norm(s):
                    if not isinstance(s, str):
                        return ""
                    s2 = unicodedata.normalize("NFKC", s).strip().lower()
                    return " ".join(s2.split())
                INDEPENDENCE_MAP = {
                    _norm("I’m fully independent and handle all tasks on my own"): "indep_full",
                    _norm("I occasionally need reminders or light assistance"): "indep_light",
                    _norm("I need help with some of these tasks regularly"): "indep_some",
                    _norm("I rely on someone else for most daily tasks"): "indep_most",
                }
                CAREGIVER_MAP = {
                    _norm("Yes, I have someone with me most of the time"): "support_most",
                    _norm("Yes, I have support a few days a week"): "support_some",
                    _norm("Infrequently—someone checks in occasionally"): "support_rare",
                    _norm("No regular caregiver or support available"): "support_none",
                }
                COGNITION_MAP = {
                    _norm("My memory’s sharp, no help needed"): "cog_clear",
                    _norm("Slight forgetfulness, but someone helps daily"): "cog_mild_help",
                    _norm("Noticeable problems, and support’s always there"): "cog_noticeable_with_support",
                    _norm("Noticeable problems, and I’m mostly on my own"): "cog_noticeable_alone",
                }
                SAFETY_MAP = {
                    _norm("Very safe—I have everything I need"): "safe_high",
                    _norm("Mostly safe, but a few things concern me"): "safe_medium",
                    _norm("Sometimes I feel unsafe or unsure"): "safe_low",
                }
                GOAL_MAP = {
                    _norm("Not important—I’m open to other options"): "goal_open",
                    _norm("Somewhat important—I’d prefer to stay but could move"): "goal_pref_home",
                    _norm("Very important—I strongly want to stay home"): "goal_strong_home",
                }
                independence_raw = care_context["care_flags"].get("independence_level", "")
                caregiver_raw = care_context["care_flags"].get("caregiver_support", "")
                cognitive_raw = care_context["care_flags"].get("cognitive_function", "")
                safety_raw = care_context["care_flags"].get("safety_level_text", "") or care_context["care_flags"].get("safety_select_text", "")
                living_goal_raw = care_context["care_flags"].get("living_goal", "")
                mobility_bool = bool(care_context["care_flags"].get("mobility_issue", False))
                falls_bool = bool(care_context["care_flags"].get("falls_risk", False))
                recent_fall = bool(care_context["derived_flags"].get("recent_fall", False))
                conditions = set(care_context["care_flags"].get("chronic_conditions", []))
                indep = INDEPENDENCE_MAP.get(_norm(independence_raw), "")
                careg = CAREGIVER_MAP.get(_norm(caregiver_raw), "")
                cogn = COGNITION_MAP.get(_norm(cognitive_raw), "")
                safe = SAFETY_MAP.get(_norm(safety_raw), "")
                goal = GOAL_MAP.get(_norm(living_goal_raw), "")
                has_dementia = any(c.strip().lower() == "dementia" for c in conditions)
                cog_severe = cogn in {"cog_noticeable_with_support", "cog_noticeable_alone"} or has_dementia
                low_support = careg in {"support_rare", "support_none"}
                limited_support = careg in {"support_some", "support_rare", "support_none"}
                safety_concern = falls_bool or recent_fall or safe in {"safe_medium", "safe_low"}
                high_adl_need = indep in {"indep_some", "indep_most"}
                in_home_blurbs = [
                    f"We're here for you, {care_context['people'][0]}. With some support at home, you can stay where you feel most comfortable—let's make it safe.",
                    f"It’s okay to need a hand, {care_context['people'][0]}. Staying home is doable with the right help—let’s set that up together.",
                    f"You’re managing well, {care_context['people'][0]}. A little in-home care can keep you rooted—we’ll find the best fit.",
                    f"No need to rush away, {care_context['people'][0]}. With some assistance, home can stay your haven—let’s plan it out.",
                    f"We see your strength, {care_context['people'][0]}. In-home care can ease the load so you stay put—ready to start?"
                ]
                assisted_blurbs = [
                    f"We’re looking out for you, {care_context['people'][0]}. Assisted living offers safety with your mobility challenges—let’s ensure you’re secure.",
                    f"It’s tough to manage alone, {care_context['people'][0]}. Assisted living brings support where you need it most—let’s make the move smooth.",
                    f"Your safety matters, {care_context['people'][0]}. With falls and limited help, assisted living could be your next step—let’s explore it.",
                    f"We’ve got your back, {care_context['people'][0]}. Assisted living fits with your needs—let’s find a place that feels right.",
                    f"You deserve peace, {care_context['people'][0]}. Assisted living can handle the risks—let’s get you settled with care."
                ]
                memory_blurbs = [
                    f"We’re here, {care_context['people'][0]}. Given your cognitive state, memory care is our recommendation to keep you safe—let’s explore options with more support.",
                    f"It’s alright, {care_context['people'][0]}. With your memory challenges, memory care is best—there may be ways to enhance support further.",
                    f"Your well-being matters, {care_context['people'][0]}. Memory care is advised due to cognitive needs—let’s look into additional care options.",
                    f"We care about you, {care_context['people'][0]}. Your cognitive state points to memory care—additional support could be tailored.",
                    f"You’re not alone, {care_context['people'][0]}. Memory care fits your cognitive needs—let’s find ways to boost that support."
                ]
                if cog_severe and (safety_concern or high_adl_need or limited_support):
                    recommendation = "Memory Care"
                    blurb = random.choice(memory_blurbs)
                    st.write(f"**Recommendation:** {recommendation}")
                    st.write(f"{blurb} Given the memory and safety considerations, a secure memory care setting is the safest fit.")
                elif indep in {"indep_full", "indep_light"} and careg in {"support_most", "support_some"} and goal in {"goal_strong_home", "goal_pref_home"} and not cog_severe:
                    recommendation = "In-Home Care"
                    blurb = random.choice(in_home_blurbs)
                    st.write(f"**Recommendation:** {recommendation}")
                    mobility_issue = "struggling with movement" if mobility_bool else "getting around okay"
                    st.write(f"{blurb} With {mobility_issue}, consistent in-home support can keep you safe where you are.")
                elif mobility_bool and safety_concern and low_support and goal in {"goal_open", "goal_unsure"} and not cog_severe:
                    recommendation = "Assisted Living"
                    blurb = random.choice(assisted_blurbs)
                    st.write(f"**Recommendation:** {recommendation}")
                    st.write(f"{blurb} This balances safety, daily help, and fewer burdens on family.")
                else:
                    recommendation = "Memory Care" if cog_severe else "Assisted Living"
                    blurb = random.choice(memory_blurbs if recommendation == "Memory Care" else assisted_blurbs)
                    st.write(f"**Recommendation:** {recommendation}")
                    if recommendation == "Memory Care":
                        st.write(f"{blurb} Based on cognition indicators, a dedicated memory setting is recommended.")
                    else:
                        st.write(f"{blurb} Based on overall risk and support, assisted living is the safer next step.")
                st.write(f"**Details:** Based on your answers, we suggest {recommendation}")
def render_step(step):
    if step == "intro":
        st.header("Welcome to Senior Navigator")
    elif step == "audiencing":
        render_audiencing()
    elif step == "planner":
        render_planner()
    else:
        st.error("Unknown step: " + step)
