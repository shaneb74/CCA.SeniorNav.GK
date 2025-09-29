import streamlit as st
from ui.helpers import radio_from_answer_map
import random

if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {}
    }

care_context = st.session_state.care_context

RECOMMENDATION_LOGIC = {
    "scoring": {
        "in_home": {
            "care_burden": 1,
            "social_isolation": 1,
            "mental_health_concern": 1,
            "financial_feasibility": 1,
            "home_safety": 1,
            "geographic_access": 1,
            "cognitive_function": 1
        },
        "assisted_living": {
            "care_burden": 3,
            "social_isolation": 3,
            "mental_health_concern": 2,
            "home_safety": 2,
            "geographic_access": 2,
            "cognitive_function": 2
        }
    },
    "dependence_flag_logic": {
        "trigger_if_flags": [
            "high_dependence",
            "high_mobility_dependence",
            "no_support",
            "severe_cognitive_risk",
            "high_safety_concern"
        ],
        "criteria": "Trigger if any 2 or more of the above flags are present",
        "message_template": "{greeting} {name}, we see you’re navigating challenges like {key_issues}. {recommendation} would offer the support and safety you need. {preference_clause}"
    },
    "social_isolation_warning": {
        "trigger_if_flags": [
            "high_risk",
            "mental_health_concern"
        ],
        "message_template": "{greeting} {name}, feeling lonely or down can weigh on you. {recommendation} could bring more connection and warmth to your days. {preference_clause}"
    },
    "cognitive_decline_warning": {
        "trigger_if_flags": [
            "moderate_cognitive_decline",
            "severe_cognitive_risk"
        ],
        "criteria": "Show if moderate_cognitive_decline or severe_cognitive_risk is present",
        "message_template": "{greeting} {name}, those memory challenges are something to watch. {recommendation} can provide the right support to keep you safe. {preference_clause}"
    },
    "final_decision_thresholds": {
        "assisted_living": "Recommend if assisted_living score >= 6",
        "in_home_with_support": "Recommend if in_home score >= 3 and assisted_living score < 6",
        "no_care_needed": "Recommend if in_home score < 3 and assisted_living score < 3 and no dependence flags"
    },
    "final_recommendation": {
        "memory_care_override": {
            "trigger_if_flags": [
                "severe_cognitive_risk"
            ],
            "criteria": "Always trigger if severe_cognitive_risk and no_support are present",
            "message_template": "{greeting} {name}, with significant memory challenges and no one around to help, memory care is the best option to keep you safe. {preference_clause}"
        }
    },
    "message_templates": {
        "greeting": [
            "We’re here for you",
            "We understand this is a big step",
            "It’s good you’re looking into this",
            "We’re glad you’re taking this step",
            "Let’s find the best fit for you"
        ],
        "preference_clause": {
            "strong_home": "Since staying home is important to you, let’s see how we can make that work with extra support.",
            "pref_home": "You’d prefer to stay home, so let’s explore ways to make that possible.",
            "open": "You’re open to options, so let’s look at assisted living communities that feel like home.",
            "unsure": "If you’re unsure, let’s talk through the options together."
        },
        "key_issues": {
            "high_dependence": [
                "needing daily help with tasks",
                "relying on assistance for daily activities",
                "having high dependence on support",
                "requiring help for everyday needs",
                "depending on others for routine tasks"
            ],
            "high_mobility_dependence": [
                "needing a lot of help to get around",
                "relying on assistance for mobility",
                "having high mobility needs",
                "requiring support to move safely",
                "depending on help for movement"
            ],
            "no_support": [
                "having no one around to help",
                "lacking regular support",
                "being on your own most of the time",
                "not having daily assistance",
                "missing consistent help"
            ],
            "severe_cognitive_risk": [
                "facing serious memory challenges",
                "having significant cognitive concerns",
                "dealing with severe memory issues",
                "experiencing serious cognitive changes",
                "navigating major cognitive risks"
            ],
            "high_safety_concern": [
                "facing safety risks at home",
                "having major safety concerns",
                "dealing with high risk of falls or emergencies",
                "needing more safety measures",
                "worrying about safety in your home"
            ],
            "high_risk": [
                "facing high social isolation",
                "feeling very isolated",
                "having significant social disconnection",
                "dealing with strong feelings of loneliness",
                "experiencing high isolation risks"
            ],
            "mental_health_concern": [
                "dealing with down moments",
                "feeling down or lonely",
                "having mental health concerns",
                "experiencing emotional challenges",
                "navigating mental health issues"
            ],
            "moderate_dependence": [
                "needing some help with tasks",
                "requiring occasional assistance",
                "having moderate dependence on support",
                "depending on help for some activities",
                "needing moderate daily support"
            ],
            "moderate_mobility": [
                "needing some mobility help",
                "requiring occasional support to get around",
                "having moderate mobility needs",
                "using aids for longer distances",
                "managing with some mobility assistance"
            ],
            "moderate_cognitive_decline": [
                "noticing some memory changes",
                "experiencing moderate memory issues",
                "dealing with slight forgetfulness",
                "having moderate cognitive concerns",
                "navigating some cognitive changes"
            ],
            "mild_cognitive_decline": [
                "having slight forgetfulness",
                "noticing mild memory changes",
                "dealing with minor cognitive issues",
                "experiencing slight cognitive decline",
                "managing mild memory concerns"
            ],
            "moderate_safety_concern": [
                "having some safety concerns",
                "feeling somewhat unsafe at times",
                "dealing with moderate risk at home",
                "needing some safety improvements",
                "worrying a bit about falls or emergencies"
            ],
            "low_access": [
                "needing help to access services",
                "finding it tough to reach pharmacies or doctors",
                "struggling to get to essential services",
                "having trouble accessing stores or care"
            ],
            "very_low_access": [
                "having no easy way to reach services",
                "relying on others to get to stores or doctors",
                "no simple access to pharmacies or doctors",
                "needing a lot of help to reach services",
                "finding services really hard to access"
            ],
            "needs_financial_assistance": [
                "worrying about the cost of care",
                "needing help to make care affordable",
                "feeling concerned about paying for support",
                "finding care costs a big challenge",
                "stressing about how to cover care expenses"
            ],
            "can_afford_care": [
                "having no worries about care costs",
                "being financially secure for any care",
                "feeling confident about covering care expenses",
                "able to afford care without stress",
                "comfortable with paying for any care needed"
            ],
            "moderate_financial_concern": [
                "needing to budget carefully for care",
                "being mindful of care costs",
                "managing finances but watching costs closely",
                "feeling some concern about care expenses",
                "keeping an eye on care costs to stay comfortable"
            ]
        },
        "flag_to_category_mapping": {
            "high_dependence": "care_burden",
            "moderate_dependence": "care_burden",
            "high_mobility_dependence": "care_burden",
            "moderate_mobility": "care_burden",
            "high_risk": "social_isolation",
            "moderate_risk": "social_isolation",
            "mental_health_concern": "mental_health_concern",
            "no_support": "caregiver_support",
            "limited_support": "caregiver_support",
            "moderate_cognitive_decline": "cognitive_function",
            "mild_cognitive_decline": "cognitive_function",
            "severe_cognitive_risk": "cognitive_function",
            "moderate_safety_concern": "home_safety",
            "high_safety_concern": "home_safety",
            "low_access": "geographic_access",
            "very_low_access": "geographic_access",
            "needs_financial_assistance": "financial_feasibility",
            "moderate_financial_concern": "financial_feasibility",
            "can_afford_care": "financial_feasibility"
        }
    }
}

def map_flags_to_categories(flags):
    category_scores = {"in_home": 0, "assisted_living": 0}
    for flag in flags:
        if flag in RECOMMENDATION_LOGIC["flag_to_category_mapping"]:
            category = RECOMMENDATION_LOGIC["flag_to_category_mapping"][flag]
            if category in RECOMMENDATION_LOGIC["scoring"]["in_home"]:
                category_scores["in_home"] += RECOMMENDATION_LOGIC["scoring"]["in_home"][category]
            if category in RECOMMENDATION_LOGIC["scoring"]["assisted_living"]:
                category_scores["assisted_living"] += RECOMMENDATION_LOGIC["scoring"]["assisted_living"][category]
    return category_scores

def check_dependence_flags(flags):
    dependence_flags = [flag for flag in RECOMMENDATION_LOGIC["dependence_flag_logic"]["trigger_if_flags"] if flag in flags]
    return len(dependence_flags) >= 2

def get_warning_message(warning_type, name, recommendation, preference_clause):
    template = RECOMMENDATION_LOGIC[warning_type]["message_template"]
    greeting = random.choice(RECOMMENDATION_LOGIC["message_templates"]["greeting"])
    return template.format(greeting=greeting, name=name, recommendation=recommendation, preference_clause=preference_clause)

def get_recommendation(name, flags, living_goal):
    preference_key = {
        "Very important—I strongly want to stay home": "strong_home",
        "Somewhat important—I’d prefer to stay but could move": "pref_home",
        "Not important—I’m open to other options": "open"
    }.get(living_goal, "unsure")
    preference_clause = RECOMMENDATION_LOGIC["message_templates"]["preference_clause"].get(
        preference_key,
        "If you’re unsure, let’s talk through the options together."
    )
    key_issues = ", ".join(
        random.choice(RECOMMENDATION_LOGIC["message_templates"]["key_issues"].get(flag, ["various challenges"]))
        for flag in flags
        if flag in RECOMMENDATION_LOGIC["message_templates"]["key_issues"]
    )
    scores = map_flags_to_categories(flags)
    dependence_triggered = check_dependence_flags(flags)
    if "severe_cognitive_risk" in flags and "no_support" in flags:
        recommendation = "Memory Care"
        message = RECOMMENDATION_LOGIC["final_recommendation"]["memory_care_override"]["message_template"].format(
            greeting=random.choice(RECOMMENDATION_LOGIC["message_templates"]["greeting"]),
            name=name,
            preference_clause=preference_clause
        )
    elif scores["assisted_living"] >= 6:
        recommendation = "Assisted Living"
        message = RECOMMENDATION_LOGIC["dependence_flag_logic"]["message_template"].format(
            greeting=random.choice(RECOMMENDATION_LOGIC["message_templates"]["greeting"]),
            name=name,
            key_issues=key_issues,
            recommendation=recommendation,
            preference_clause=preference_clause
        )
        if any(flag in flags for flag in RECOMMENDATION_LOGIC["social_isolation_warning"]["trigger_if_flags"]):
            message += " " + get_warning_message("social_isolation_warning", name, recommendation, preference_clause)
        if any(flag in flags for flag in RECOMMENDATION_LOGIC["cognitive_decline_warning"]["trigger_if_flags"]):
            message += " " + get_warning_message("cognitive_decline_warning", name, recommendation, preference_clause)
    elif scores["in_home"] >= 3 and scores["assisted_living"] < 6:
        recommendation = "In-Home Care with Support"
        message = RECOMMENDATION_LOGIC["dependence_flag_logic"]["message_template"].format(
            greeting=random.choice(RECOMMENDATION_LOGIC["message_templates"]["greeting"]),
            name=name,
            key_issues=key_issues,
            recommendation=recommendation,
            preference_clause=preference_clause
        )
        if any(flag in flags for flag in RECOMMENDATION_LOGIC["social_isolation_warning"]["trigger_if_flags"]):
            message += " " + get_warning_message("social_isolation_warning", name, recommendation, preference_clause)
        if any(flag in flags for flag in RECOMMENDATION_LOGIC["cognitive_decline_warning"]["trigger_if_flags"]):
            message += " " + get_warning_message("cognitive_decline_warning", name, recommendation, preference_clause)
    elif scores["in_home"] < 3 and scores["assisted_living"] < 3 and not dependence_triggered:
        recommendation = "No Care Needed at This Time"
        message = f"{random.choice(RECOMMENDATION_LOGIC['message_templates']['greeting'])} {name}, it looks like you’re managing well for now. {preference_clause}"
    else:
        recommendation = "Assisted Living"
        message = RECOMMENDATION_LOGIC["dependence_flag_logic"]["message_template"].format(
            greeting=random.choice(RECOMMENDATION_LOGIC["message_templates"]["greeting"]),
            name=name,
            key_issues=key_issues,
            recommendation=recommendation,
            preference_clause=preference_clause
        )
        if any(flag in flags for flag in RECOMMENDATION_LOGIC["social_isolation_warning"]["trigger_if_flags"]):
            message += " " + get_warning_message("social_isolation_warning", name, recommendation, preference_clause)
        if any(flag in flags for flag in RECOMMENDATION_LOGIC["cognitive_decline_warning"]["trigger_if_flags"]):
            message += " " + get_warning_message("cognitive_decline_warning", name, recommendation, preference_clause)
    return recommendation, message

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
            care_context["people"] = [client_name] if client_name else ["Client"]
            st.session_state.care_context = care_context
            st.write(f"Okay—we’re building this for {', '.join(care_context['people'])} as {care_context.get('professional_role')}")
        if st.button("Proceed to Guided Care Plan", key="audiencing_proceed",
                     disabled=not (care_context.get("audience_type") and care_context.get("people") and care_context.get("relation"))):
            if (care_context["audience_type"] == "Planning for one person" and care_context["people"] and care_context["relation"]) or \
               (care_context["audience_type"] == "Planning for two people" and len(care_context["people"]) == 2 and care_context["relation"]) or \
               (care_context["audience_type"] == "Planning as a professional"):
                st.session_state.step = "planner"
                st.session_state.audiencing_step = 1
                st.rerun()

def render_planner():
    st.header("Guided Care Plan")
    st.write("Let’s walk through a few questions to understand your care needs.")
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1
    if st.session_state.get("step") == "planner" and st.session_state.get("show_qa", False):
        with st.expander("Answers & Flags", expanded=True):
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
            funding_confidence = st.radio(
                "How confident are you that your savings will cover long-term care?",
                funding_options_list,
                key="funding_confidence_select"
            )
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
            independence = st.radio(
                "How independent are you with daily tasks such as bathing, dressing, and preparing meals?",
                independence_options_list,
                key="independence_select"
            )
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
            social = st.radio(
                "How often do you feel lonely, down, or socially disconnected?",
                social_options_list,
                key="social_select"
            )
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
            caregiver = st.radio(
                "Do you have a caregiver or family member who can help regularly?",
                caregiver_options_list,
                key="caregiver_select"
            )
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
            cognition = st.radio(
                "Thinking about your memory and focus, is someone usually around to help you?",
                cognition_options_list,
                key="cognition_select"
            )
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
            safety = st.radio(
                "How safe do you feel in your home in terms of fall risk, emergencies, or managing on your own?",
                safety_options_list,
                key="safety_select"
            )
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
            fall_options = {"1": "Yes", "2": "No", "3": "Unsure"}
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
                flags = []
                indep = care_context["care_flags"].get("independence_level")
                if indep in ["I rely on someone else for most daily tasks"]:
                    flags.append("high_dependence")
                elif indep in ["I need help with some of these tasks regularly"]:
                    flags.append("moderate_dependence")
                if care_context["care_flags"].get("mobility_issue"):
                    flags.append("high_mobility_dependence")
                elif care_context["derived_flags"].get("inferred_mobility_aid") in [
                    "I use a cane or walker for longer distances",
                    "I need assistance for most movement around the home"
                ]:
                    flags.append("moderate_mobility")
                social = care_context["care_flags"].get("social_disconnection")
                if social in ["Often—I feel isolated or down much of the time"]:
                    flags.append("high_risk")
                elif social in ["Sometimes—I connect weekly but have some down moments"]:
                    flags.append("moderate_risk")
                if social in ["Often—I feel isolated or down much of the time", "Sometimes—I connect weekly but have some down moments"]:
                    flags.append("mental_health_concern")
                support = care_context["care_flags"].get("caregiver_support")
                if support in ["No regular caregiver or support available"]:
                    flags.append("no_support")
                elif support in ["Infrequently—someone checks in occasionally"]:
                    flags.append("limited_support")
                elif support in ["Yes, I have someone with me most of the time", "Yes, I have support a few days a week"]:
                    flags.append("adequate_support")
                cog = care_context["care_flags"].get("cognitive_function")
                if cog in ["Noticeable problems, and I’m mostly on my own"]:
                    flags.append("severe_cognitive_risk")
                elif cog in ["Noticeable problems, and support’s always there"]:
                    flags.append("moderate_cognitive_decline")
                elif cog in ["Slight forgetfulness, but someone helps daily"]:
                    flags.append("mild_cognitive_decline")
                has_falls_risk = bool(care_context["care_flags"].get("falls_risk"))
                recent_fall = bool(care_context["derived_flags"].get("recent_fall", False))
                if has_falls_risk and recent_fall:
                    flags.append("high_safety_concern")
                elif has_falls_risk:
                    flags.append("moderate_safety_concern")
                funding = care_context["care_flags"].get("funding_confidence")
                if funding in ["Very worried—cost is a big concern for me", "I am on Medicaid"]:
                    flags.append("needs_financial_assistance")
                elif funding in ["Somewhat worried—I’d need to budget carefully"]:
                    flags.append("moderate_financial_concern")
                elif funding in ["Not worried—I can cover any care I need"]:
                    flags.append("can_afford_care")
                name = care_context["people"][0] if care_context["people"] else "friend"
                living_goal = care_context["care_flags"].get("living_goal", "Not important—I’m open to other options")
                recommendation, message = get_recommendation(name, flags, living_goal)
                st.write(message)

def render_step(step):
    if step == "intro":
        st.title("Senior Navigator")
        st.write("Welcome! Start by exploring your options.")
        if st.button("Get Started"):
            st.session_state.step = "audiencing"
            st.session_state.audiencing_step = 1
            st.rerun()
    elif step == "qa":
        st.header("QA View")
        with st.expander("Answers & Flags", expanded=True):
            st.write("**Audience Type:**", care_context.get("audience_type", "Not set"))
            st.write("**People:**", ", ".join(care_context.get("people", [])))
            st.write("**Relation:**", care_context.get("relation", "Not set"))
            st.write("**Care Flags:**", {k: v for k, v in care_context.get("care_flags", {}).items() if v})
            st.write("**Derived Flags:**", {k: v for k, v in care_context.get("derived_flags", {}).items() if v})
    elif step == "audiencing":
        render_audiencing()
    elif step == "planner":
        render_planner()
    elif step == "cost_planner":
        st.header("Cost Planner")
        st.write("This section is under development.")
    elif step == "advisor":
        st.header("Plan for My Advisor")
        st.write("This section is under development.")
    else:
        st.error("Unknown step: " + step)
