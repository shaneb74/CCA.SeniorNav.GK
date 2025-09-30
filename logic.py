import streamlit as st
import random
from ui.helpers import radio_from_answer_map

st.markdown('''<style>
    .stMarkdown p {
        font-size: 22px !important;
    }
    .stRadio label {
        font-size: 18px !important;
        margin-top: 5px;
    }
</style>''', unsafe_allow_html=True)



# Enhanced CSS for readability and layout
st.markdown(
    """
    <style>
    .question-text {
        font-size: 22px !important;
        font-weight: 500;
        line-height: 1.6;
        margin-bottom: 15px;
        color: #2c3e50;
    }
    .stRadio > div {
        font-size: 18px !important;
        line-height: 1.5;
        padding: 8px 0;
        color: #34495e;
    }
    .stRadio label {
        margin-left: 10px;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        margin: 5px 0;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {}
    }

care_context = st.session_state.care_context

def run_tests():
    test_cases = [
        {
            "name": "Alex - COPD + Cane",
            "funding": "Not worried—I can afford any care I need",
            "cognition": "Noticeable problems—like missing meds or appointments",
            "caregiver": "Someone checks in occasionally",
            "meds": "Yes",
            "med_adherence": "I’m pretty sure, with reminders",
            "independence": "I need help with some of these tasks regularly",
            "mobility": "I use a cane or walker for longer distances",
            "social": "Monthly calls",
            "geography": "Needs a ride, but manageable",
            "safety": "Mostly safe, but a few concerns",
            "fall": "No",
            "chronic": ["COPD"],
            "preference": "Very important—I strongly want to stay home"
        },
        {
            "name": "Jane - Early Dementia",
            "funding": "Not worried—I can afford any care I need",
            "cognition": "Occasional lapses—like forgetting what I was saying",
            "caregiver": "Support most days",
            "meds": "Yes",
            "med_adherence": "I need help sometimes",
            "independence": "I’m fully independent and handle all tasks on my own",
            "mobility": "I walk easily without any support",
            "social": "Daily visits or calls",
            "geography": "Easy—I can walk or drive",
            "safety": "Very safe—I have everything I need",
            "fall": "No",
            "chronic": ["Dementia"],
            "preference": "Not important—I’m open to other options"
        },
        {
            "name": "Bob - Poor with Support",
            "funding": "Very worried—cost is a big concern for me",
            "cognition": "My memory feels sharp—no real issues",
            "caregiver": "Someone’s with me all the time",
            "meds": "No",
            "med_adherence": "No",
            "independence": "I occasionally need reminders or light assistance",
            "mobility": "I use a cane or walker for longer distances",
            "social": "Weekly check-ins",
            "geography": "Pretty hard without help",
            "safety": "Mostly safe, but a few concerns",
            "fall": "Yes",
            "chronic": [],
            "preference": "Somewhat important—I’d prefer to stay but could move"
        },
        {
            "name": "Isolated Emma",
            "funding": "Somewhat worried—I’d need to budget carefully",
            "cognition": "Noticeable problems—like missing meds or appointments",
            "caregiver": "No regular support",
            "meds": "Yes",
            "med_adherence": "I can’t count on myself",
            "independence": "I rely on someone else for most daily tasks",
            "mobility": "I am mostly immobile or need a wheelchair",
            "social": "Mostly alone",
            "geography": "Impossible alone",
            "safety": "Often feel at risk",
            "fall": "Yes",
            "chronic": ["CHF"],
            "preference": "Not important—I’m open to other options"
        },
        {
            "name": "Mobile Mike",
            "funding": "Not worried—I can afford any care I need",
            "cognition": "Serious confusion—like losing track of time, place, or familiar faces",
            "caregiver": "Support most days",
            "meds": "Yes",
            "med_adherence": "I manage them rock-solid",
            "independence": "I’m fully independent and handle all tasks on my own",
            "mobility": "I walk easily without any support",
            "social": "Daily visits or calls",
            "geography": "Easy—I can walk or drive",
            "safety": "Very safe—I have everything I need",
            "fall": "No",
            "chronic": ["Dementia"],
            "preference": "Very important—I strongly want to stay home"
        },
        {
            "name": "Falls-Prone Fred",
            "funding": "Very worried—cost is a big concern for me",
            "cognition": "Occasional lapses—like forgetting what I was saying",
            "caregiver": "Someone checks in occasionally",
            "meds": "No",
            "med_adherence": "No",
            "independence": "I need help with some of these tasks regularly",
            "mobility": "I need assistance for most movement around the home",
            "social": "Weekly check-ins",
            "geography": "Needs a ride, but manageable",
            "safety": "Sometimes I feel unsafe",
            "fall": "Yes",
            "chronic": ["Arthritis"],
            "preference": "Somewhat important—I’d prefer to stay but could move"
        },
        {
            "name": "Full-Time Care Carol",
            "funding": "Not worried—I can afford any care I need",
            "cognition": "My memory feels sharp—no real issues",
            "caregiver": "Someone’s with me all the time",
            "meds": "Yes",
            "med_adherence": "I manage them rock-solid",
            "independence": "I rely on someone else for most daily tasks",
            "mobility": "I am mostly immobile or need a wheelchair",
            "social": "Daily visits or calls",
            "geography": "Easy—I can walk or drive",
            "safety": "Very safe—I have everything I need",
            "fall": "No",
            "chronic": [],
            "preference": "Very important—I strongly want to stay home"
        },
        {
            "name": "No-Meds Nancy",
            "funding": "Somewhat worried—I’d need to budget carefully",
            "cognition": "Noticeable problems—like missing meds or appointments",
            "caregiver": "Support most days",
            "meds": "No",
            "med_adherence": "No",
            "independence": "I occasionally need reminders or light assistance",
            "mobility": "I use a cane or walker for longer distances",
            "social": "Monthly calls",
            "geography": "Pretty hard without help",
            "safety": "Mostly safe, but a few concerns",
            "fall": "No",
            "chronic": ["Hypertension"],
            "preference": "Not important—I’m open to other options"
        },
        {
            "name": "Home-Hater Hank",
            "funding": "Very worried—cost is a big concern for me",
            "cognition": "Serious confusion—like losing track of time, place, or familiar faces",
            "caregiver": "No regular support",
            "meds": "Yes",
            "med_adherence": "I need help sometimes",
            "independence": "I rely on someone else for most daily tasks",
            "mobility": "I need assistance for most movement around the home",
            "social": "Mostly alone",
            "geography": "Impossible alone",
            "safety": "Often feel at risk",
            "fall": "Yes",
            "chronic": ["Parkinson's"],
            "preference": "Not important—I’m open to other options"
        },
        {
            "name": "Mild Mary",
            "funding": "Not worried—I can afford any care I need",
            "cognition": "Occasional lapses—like forgetting what I was saying",
            "caregiver": "Someone’s with me all the time",
            "meds": "Yes",
            "med_adherence": "I’m pretty sure, with reminders",
            "independence": "I’m fully independent and handle all tasks on my own",
            "mobility": "I walk easily without any support",
            "social": "Daily visits or calls",
            "geography": "Easy—I can walk or drive",
            "safety": "Very safe—I have everything I need",
            "fall": "No",
            "chronic": [],
            "preference": "Very important—I strongly want to stay home"
        }
    ]

    st.write("### Test Case Results")
    st.write("| Name                  | Score | Recommendation            | Top 3 Issues                          |")
    st.write("|-----------------------|-------|---------------------------|---------------------------------------|")
    for case in test_cases:
        # Simulate setting care_context
        care_context["care_flags"] = {}
        care_context["derived_flags"] = {}
        care_context["care_flags"]["funding_confidence"] = case["funding"]
        care_context["care_flags"]["cognitive_function"] = case["cognition"]
        care_context["care_flags"]["caregiver_support"] = case["caregiver"]
        care_context["care_flags"]["med_adherence"] = case["med_adherence"] if case["meds"] == "Yes" else "No"
        care_context["care_flags"]["independence_level"] = case["independence"]
        care_context["care_flags"]["mobility_issue"] = case["mobility"] != "I walk easily without any support"
        care_context["derived_flags"]["inferred_mobility_aid"] = case["mobility"]
        care_context["care_flags"]["social_connection"] = case["social"]
        care_context["care_flags"]["geographic_access"] = case["geography"]
        care_context["care_flags"]["falls_risk"] = case["safety"] in ["Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"]
        care_context["derived_flags"]["recent_fall"] = case["fall"] == "Yes"
        care_context["care_flags"]["chronic_conditions"] = case["chronic"]
        care_context["care_flags"]["living_goal"] = case["preference"]

        # Score calculation
        flags = []
        if care_context["care_flags"]["funding_confidence"] in ["Very worried—cost is a big concern for me", "Somewhat worried—I’d need to budget carefully"]:
            flags.append("needs_financial_assistance")
        elif care_context["care_flags"]["funding_confidence"] == "Not worried—I can afford any care I need":
            flags.append("can_afford_care")

        cog = care_context["care_flags"]["cognitive_function"]
        conditions = care_context["care_flags"]["chronic_conditions"]
        if "Serious confusion" in cog or "Dementia" in conditions or "Parkinson's" in conditions:
            flags.append("severe_cognitive_risk")
        elif "Noticeable problems" in cog:
            flags.append("moderate_cognitive_decline")
        elif "Occasional lapses" in cog:
            flags.append("mild_cognitive_decline")

        support = care_context["care_flags"]["caregiver_support"]
        if "No regular support" in support:
            flags.append("no_support")
        elif "Someone checks in occasionally" in support:
            flags.append("limited_support")
        elif "Support most days" in support or "Someone’s with me all the time" in support:
            flags.append("adequate_support")

        if care_context["care_flags"]["med_adherence"] in ["I need help sometimes", "I can’t count on myself"]:
            flags.append("med_adherence_risk")

        indep = care_context["care_flags"]["independence_level"]
        if "I rely on someone else for most daily tasks" in indep:
            flags.append("high_dependence")
        elif "I need help with some of these tasks regularly" in indep:
            flags.append("moderate_dependence")

        mobility = care_context["derived_flags"]["inferred_mobility_aid"]
        if "I need assistance for most movement around the home" in mobility or "I am mostly immobile or need a wheelchair" in mobility:
            flags.append("high_mobility_dependence")
        elif "I use a cane or walker for longer distances" in mobility:
            flags.append("moderate_mobility")

        social = care_context["care_flags"]["social_connection"]
        if "Mostly alone" in social:
            flags.append("high_risk")
        elif "Monthly calls" in social:
            flags.append("moderate_risk")

        geo = care_context["care_flags"]["geographic_access"]
        if "Pretty hard without help" in geo or "Impossible alone" in geo:
            flags.append("very_low_access")

        safety = care_context["care_flags"]["falls_risk"]
        if safety:
            flags.append("moderate_safety_concern")

        if care_context["derived_flags"]["recent_fall"]:
            flags.append("high_safety_concern")

        score = 0
        if "severe_cognitive_risk" in flags and "adequate_support" in flags:
            score += 10
        elif "severe_cognitive_risk" in flags:
            score += 15
        if "moderate_cognitive_decline" in flags:
            score += 5
        if "mild_cognitive_decline" in flags:
            score += 3
        if "high_dependence" in flags or "high_mobility_dependence" in flags:
            score += 10
        if "moderate_dependence" in flags or "moderate_mobility" in flags:
            score += 5
        if "no_support" in flags:
            score += 7
        if "limited_support" in flags:
            pass  # No penalty for borderline support
        if "adequate_support" in flags:
            score -= 3  # Reduced to balance no-care threshold
        if "high_risk" in flags:
            score += 6
        if "moderate_risk" in flags:
            score += 3
        if "med_adherence_risk" in flags:
            score += 6
        if "very_low_access" in flags:
            score += 4
        if "moderate_safety_concern" in flags:
            score += 5
        if "high_safety_concern" in flags:
            score += 8
        if "chronic_health_risk" in flags:
            score += 7

        # Floor score at 0
        score = max(0, score)

        # Determine recommendation
        recommendation = "No Care Needed at This Time"
        issues = []
        if ("severe_cognitive_risk" in flags and "no_support" in flags) or score >= 25:
            recommendation = "Memory Care"
            issues = [f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns', 'dealing with severe memory issues']) if 'severe_cognitive_risk' in flags else ''}",
                      f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else ''}",
                      f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else ''}"]
        elif score >= 15:
            recommendation = "Assisted Living"
            issues = [f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                      f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                      f"{random.choice(['having no one around to help', 'lacking regular support']) if 'no_support' in flags else random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                      f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns']) if 'severe_cognitive_risk' in flags else random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                      f"{random.choice(['facing safety risks at home', 'having major safety concerns']) if 'high_safety_concern' in flags else random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
        elif score >= 8:
            recommendation = "In-Home Care with Support"
            issues = [f"{random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                      f"{random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                      f"{random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                      f"{random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                      f"{random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
        issues = [i for i in issues if i][:3]  # Top 3 issues

        st.write(f"| {case['name']} | {score} | {recommendation} | {', '.join(issues) if issues else 'None'} |")

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
            st.markdown("<p class='question-text'>Your Financial Confidence</p>", unsafe_allow_html=True)
            st.write("First, let’s talk about your finances.")
            funding_options = {
                "1": "Not worried—I can afford any care I need",
                "2": "Somewhat worried—I’d need to budget carefully",
                "3": "Very worried—cost is a big concern for me",
                "4": "I am on Medicaid"
            }
            funding_key = radio_from_answer_map(
                label="How confident are you that your savings will cover long-term care?",
                amap=funding_options,
                key="funding_confidence_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if funding_key:
                funding_confidence = funding_options[funding_key]
                if funding_confidence == "I am on Medicaid":
                    st.write("We can connect you to Medicaid-friendly care options—just tap here.", unsafe_allow_html=True)
                    if st.button("Get Options", key="medicaid_options"):
                        st.session_state.step = "tools"
                        st.rerun()
                else:
                    care_context["care_flags"]["funding_confidence"] = funding_confidence
                    st.session_state.care_context = care_context
                    st.write(f"You feel: {care_context['care_flags']['funding_confidence']}")
            if st.button("Next", key="planner_next_1", disabled=not funding_key or funding_confidence == "I am on Medicaid"):
                st.session_state.planner_step = 2
                st.rerun()
            if st.button("Go Back", key="planner_back_1", disabled=True):
                pass

        elif st.session_state.planner_step == 2:
            st.markdown("<p class='question-text'>Your Cognition</p>", unsafe_allow_html=True)
            st.write("Next, let’s talk about your memory and thinking.")
            cognition_options = {
                "1": "My memory feels sharp—no real issues",
                "2": "Occasional lapses—like forgetting what I was saying",
                "3": "Noticeable problems—like missing meds or appointments",
                "4": "Serious confusion—like losing track of time, place, or familiar faces"
            }
            cognition_key = radio_from_answer_map(
                label="How would you describe your memory and focus?",
                amap=cognition_options,
                key="cognition_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if cognition_key:
                cognition = cognition_options[cognition_key]
                care_context["care_flags"]["cognitive_function"] = cognition
                st.session_state.care_context = care_context
                st.write(f"You noted: {care_context['care_flags']['cognitive_function']}")
            if st.button("Next", key="planner_next_2", disabled=not cognition_key):
                st.session_state.planner_step = 3
                st.rerun()
            if st.button("Go Back", key="planner_back_2"):
                st.session_state.planner_step = 1
                st.rerun()

        elif st.session_state.planner_step == 3:
            st.markdown("<p class='question-text'>Your Caregiver Support</p>", unsafe_allow_html=True)
            cog = care_context["care_flags"].get("cognitive_function", "")
            funding = care_context["care_flags"].get("funding_confidence", "")
            if "Occasional lapses" in cog or "Noticeable problems" in cog or "Serious confusion" in cog:
                if "Not worried—I can afford any care I need" in funding:
                    st.write(f"Great, you’re financially secure. With {cog.lower()}, would 24/7 caregivers at home work?")
                else:
                    st.write(f"Since you’ve noted {cog.lower()}, it’s key to know: who’s there if memory slips?")
            else:
                st.write("How often do you have someone to help with daily needs?")
            caregiver_options = {
                "1": "Someone’s with me all the time",
                "2": "Support most days",
                "3": "Someone checks in occasionally",
                "4": "No regular support"
            }
            caregiver_key = radio_from_answer_map(
                label="How often is someone available to assist you?",
                amap=caregiver_options,
                key="caregiver_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if caregiver_key:
                caregiver = caregiver_options[caregiver_key]
                care_context["care_flags"]["caregiver_support"] = caregiver
                st.session_state.care_context = care_context
                st.write(f"Support level: {care_context['care_flags']['caregiver_support']}")
            if st.button("Next", key="planner_next_3", disabled=not caregiver_key):
                st.session_state.planner_step = 4
                st.rerun()
            if st.button("Go Back", key="planner_back_3"):
                st.session_state.planner_step = 2
                st.rerun()

        elif st.session_state.planner_step == 4:
            st.markdown("<p class='question-text'>Your Medication Management</p>", unsafe_allow_html=True)
            takes_meds = st.radio(
                "Do you take any daily prescription meds (e.g., for heart, mood, or memory)?",
                ["No", "Yes"],
                index=0,
                key="takes_meds_select"
            )
            if takes_meds == "Yes":
                cog = care_context["care_flags"].get("cognitive_function", "")
                if "Occasional lapses" in cog or "Noticeable problems" in cog or "Serious confusion" in cog:
                    st.write(f"Since you’ve noted {cog.lower()}, how confident are you with your meds?")
                else:
                    st.write("How confident are you managing your meds?")
                med_options = {
                    "1": "I manage them rock-solid",
                    "2": "I’m pretty sure, with reminders",
                    "3": "I need help sometimes",
                    "4": "I can’t count on myself"
                }
                med_key = radio_from_answer_map(
                    label="How do you handle your medications?",
                    amap=med_options,
                    key="med_confidence_select",
                    default_key="1",
                    show_debug=st.session_state.get("show_qa", False)
                )
                if med_key:
                    med_confidence = med_options[med_key]
                    care_context["care_flags"]["med_adherence"] = med_confidence
                    st.session_state.care_context = care_context
                    st.write(f"Med management: {care_context['care_flags']['med_adherence']}")
            if st.button("Next", key="planner_next_4", disabled=(takes_meds != "No" and not med_key)):
                st.session_state.planner_step = 5
                st.rerun()
            if st.button("Go Back", key="planner_back_4"):
                st.session_state.planner_step = 3
                st.rerun()

        elif st.session_state.planner_step == 5:
            st.markdown("<p class='question-text'>Your Daily Independence</p>", unsafe_allow_html=True)
            st.write("Now, let’s look at your daily routine.")
            independence_options = {
                "1": "I’m fully independent and handle all tasks on my own",
                "2": "I occasionally need reminders or light assistance",
                "3": "I need help with some of these tasks regularly",
                "4": "I rely on someone else for most daily tasks"
            }
            independence_key = radio_from_answer_map(
                label="How independent are you with tasks like bathing, dressing, or meals?",
                amap=independence_options,
                key="independence_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if independence_key:
                independence = independence_options[independence_key]
                care_context["care_flags"]["independence_level"] = independence
                st.session_state.care_context = care_context
                st.write(f"Independence: {care_context['care_flags']['independence_level']}")
            if st.button("Next", key="planner_next_5", disabled=not independence_key):
                st.session_state.planner_step = 6
                st.rerun()
            if st.button("Go Back", key="planner_back_5"):
                st.session_state.planner_step = 4
                st.rerun()

        elif st.session_state.planner_step == 6:
            st.markdown("<p class='question-text'>Your Mobility</p>", unsafe_allow_html=True)
            st.write("Let’s talk about getting around.")
            mobility_options = {
                "1": "I walk easily without any support",
                "2": "I use a cane or walker for longer distances",
                "3": "I need assistance for most movement around the home",
                "4": "I am mostly immobile or need a wheelchair"
            }
            mobility_key = radio_from_answer_map(
                label="How would you describe your mobility?",
                amap=mobility_options,
                key="mobility_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if mobility_key:
                mobility = mobility_options[mobility_key]
                care_context["care_flags"]["mobility_issue"] = mobility != mobility_options["1"]
                if mobility != mobility_options["1"]:
                    care_context["derived_flags"]["inferred_mobility_aid"] = mobility
                st.session_state.care_context = care_context
                st.write(f"Mobility: {care_context['care_flags']['mobility_issue']}")
            if st.button("Next", key="planner_next_6", disabled=not mobility_key):
                st.session_state.planner_step = 7
                st.rerun()
            if st.button("Go Back", key="planner_back_6"):
                st.session_state.planner_step = 5
                st.rerun()

        elif st.session_state.planner_step == 7:
            st.markdown("<p class='question-text'>Your World</p>", unsafe_allow_html=True)
            st.write("Finally, let’s look at your living situation.")

            st.markdown("<p class='question-text'>Social Connection</p>", unsafe_allow_html=True)
            st.write("How connected are you with family, friends, or neighbors?")
            social_options = {
                "1": "Daily visits or calls",
                "2": "Weekly check-ins",
                "3": "Monthly calls",
                "4": "Mostly alone"
            }
            social_key = radio_from_answer_map(
                label="How often do you see or hear from people close to you?",
                amap=social_options,
                key="social_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if social_key:
                social = social_options[social_key]
                care_context["care_flags"]["social_connection"] = social
                st.session_state.care_context = care_context
                st.write(f"Social: {care_context['care_flags']['social_connection']}")

            st.markdown("<p class='question-text'>Geography & Access</p>", unsafe_allow_html=True)
            chronic_conditions = care_context["care_flags"].get("chronic_conditions", [])
            if chronic_conditions:
                st.write(f"With conditions like {', '.join(chronic_conditions)}, how easy is it to reach doctors?")
            else:
                st.write("How easy is it to reach doctors or stores?")
            geo_options = {
                "1": "Easy—I can walk or drive",
                "2": "Needs a ride, but manageable",
                "3": "Pretty hard without help",
                "4": "Impossible alone"
            }
            geo_key = radio_from_answer_map(
                label="How accessible are healthcare and services?",
                amap=geo_options,
                key="geography_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if geo_key:
                geography = geo_options[geo_key]
                care_context["care_flags"]["geographic_access"] = geography
                st.session_state.care_context = care_context
                st.write(f"Access: {care_context['care_flags']['geographic_access']}")

            st.markdown("<p class='question-text'>Home Safety</p>", unsafe_allow_html=True)
            st.write("How safe do you feel at home?")
            safety_options = {
                "1": "Very safe—I have everything I need",
                "2": "Mostly safe, but a few concerns",
                "3": "Sometimes I feel unsafe",
                "4": "Often feel at risk"
            }
            safety_key = radio_from_answer_map(
                label="How safe is your home for falls or emergencies?",
                amap=safety_options,
                key="safety_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if safety_key:
                safety = safety_options[safety_key]
                care_context["care_flags"]["falls_risk"] = safety in ["Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"]
                st.session_state.care_context = care_context
                st.write(f"Safety: {care_context['care_flags']['falls_risk']}")

            st.markdown("<p class='question-text'>Fall History</p>", unsafe_allow_html=True)
            st.write("Based on your safety answer, let’s check this.")
            fall_options = {"1": "Yes", "2": "No", "3": "Unsure"}
            fall_key = radio_from_answer_map(
                label="Have you fallen in the last six months?",
                amap=fall_options,
                key="fall_history_select",
                default_key="2",
                show_debug=st.session_state.get("show_qa", False)
            )
            if fall_key:
                fall_history = fall_options[fall_key]
                care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
                st.session_state.care_context = care_context
                st.write(f"Fall history: {care_context['derived_flags'].get('recent_fall', 'Not set')}")

            st.markdown("<p class='question-text'>Chronic Conditions</p>", unsafe_allow_html=True)
            st.write("Any ongoing health issues?")
            condition_options = ["Diabetes", "Hypertension", "Dementia", "Parkinson's", "COPD", "CHF", "Arthritis", "Stroke"]
            conditions = st.multiselect("Which chronic conditions do you have?", condition_options, key="chronic_conditions_select")
            if conditions:
                care_context["care_flags"]["chronic_conditions"] = conditions
                st.session_state.care_context = care_context
                st.write(f"Chronic conditions: {', '.join(care_context['care_flags']['chronic_conditions'])}")

            if st.button("Next", key="planner_next_7", disabled=not (social_key and geo_key and safety_key and fall_key and conditions is not None)):
                st.session_state.planner_step = 8
                st.rerun()
            if st.button("Go Back", key="planner_back_7"):
                st.session_state.planner_step = 6
                st.rerun()

        elif st.session_state.planner_step == 8:
            st.markdown("<p class='question-text'>Your Home Preference</p>", unsafe_allow_html=True)
            st.write("Lastly, how do you feel about staying home?")
            goal_options = {
                "1": "Not important—I’m open to other options",
                "2": "Somewhat important—I’d prefer to stay but could move",
                "3": "Very important—I strongly want to stay home"
            }
            goal_key = radio_from_answer_map(
                label="How important is it to stay in your current home?",
                amap=goal_options,
                key="goal_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if goal_key:
                goal = goal_options[goal_key]
                care_context["care_flags"]["living_goal"] = goal
                st.session_state.care_context = care_context
                st.write(f"Preference: {care_context['care_flags']['living_goal']}")
            if st.button("Get Recommendation", key="planner_next_8", disabled=not goal_key):
                st.session_state.planner_step = 9
                st.rerun()
            if st.button("Go Back", key="planner_back_8"):
                st.session_state.planner_step = 7
                st.rerun()

        elif st.session_state.planner_step == 9:
            st.subheader("Care Recommendation")
            st.write("Based on your answers, here’s our suggestion.")
            flags = []
            # Financial
            funding = care_context["care_flags"].get("funding_confidence", "")
            if funding in ["Very worried—cost is a big concern for me", "Somewhat worried—I’d need to budget carefully"]:
                flags.append("needs_financial_assistance")
            elif funding == "Not worried—I can afford any care I need":
                flags.append("can_afford_care")

            # Cognition
            cog = care_context["care_flags"].get("cognitive_function", "")
            conditions = care_context["care_flags"].get("chronic_conditions", [])
            if "Serious confusion" in cog or "Dementia" in conditions or "Parkinson's" in conditions:
                flags.append("severe_cognitive_risk")
            elif "Noticeable problems" in cog:
                flags.append("moderate_cognitive_decline")
            elif "Occasional lapses" in cog:
                flags.append("mild_cognitive_decline")

            # Caregiver Support
            support = care_context["care_flags"].get("caregiver_support", "")
            if "No regular support" in support:
                flags.append("no_support")
            elif "Someone checks in occasionally" in support:
                flags.append("limited_support")
            elif "Support most days" in support or "Someone’s with me all the time" in support:
                flags.append("adequate_support")

            # Medication Adherence
            med_adherence = care_context["care_flags"].get("med_adherence", "No")
            if med_adherence in ["I need help sometimes", "I can’t count on myself"]:
                flags.append("med_adherence_risk")

            # Independence
            indep = care_context["care_flags"].get("independence_level", "")
            if "I rely on someone else for most daily tasks" in indep:
                flags.append("high_dependence")
            elif "I need help with some of these tasks regularly" in indep:
                flags.append("moderate_dependence")

            # Mobility
            mobility = care_context["derived_flags"].get("inferred_mobility_aid", "")
            if "I need assistance for most movement around the home" in mobility or "I am mostly immobile or need a wheelchair" in mobility:
                flags.append("high_mobility_dependence")
            elif "I use a cane or walker for longer distances" in mobility:
                flags.append("moderate_mobility")

            # Social Connection
            social = care_context["care_flags"].get("social_connection", "")
            if "Mostly alone" in social:
                flags.append("high_risk")
            elif "Monthly calls" in social:
                flags.append("moderate_risk")

            # Geography & Access
            geo = care_context["care_flags"].get("geographic_access", "")
            if "Pretty hard without help" in geo or "Impossible alone" in geo:
                flags.append("very_low_access")

            # Home Safety
            safety = care_context["care_flags"].get("falls_risk", False)
            if safety:
                flags.append("moderate_safety_concern")

            # Fall History
            if care_context["derived_flags"].get("recent_fall", False):
                flags.append("high_safety_concern")

            # Score Calculation
            score = 0
            if "severe_cognitive_risk" in flags and "adequate_support" in flags:
                score += 10
            elif "severe_cognitive_risk" in flags:
                score += 15
            if "moderate_cognitive_decline" in flags:
                score += 5
            if "mild_cognitive_decline" in flags:
                score += 3
            if "high_dependence" in flags or "high_mobility_dependence" in flags:
                score += 10
            if "moderate_dependence" in flags or "moderate_mobility" in flags:
                score += 5
            if "no_support" in flags:
                score += 7
            if "limited_support" in flags:
                pass  # No penalty for borderline support
            if "adequate_support" in flags:
                score -= 3  # Reduced to balance no-care threshold
            if "high_risk" in flags:
                score += 6
            if "moderate_risk" in flags:
                score += 3
            if "med_adherence_risk" in flags:
                score += 6
            if "very_low_access" in flags:
                score += 4
            if "moderate_safety_concern" in flags:
                score += 5
            if "high_safety_concern" in flags:
                score += 8
            if "chronic_health_risk" in flags:
                score += 7

            # Floor score at 0
            score = max(0, score)

            # Determine recommendation
            recommendation = "No Care Needed at This Time"
            issues = []
            if ("severe_cognitive_risk" in flags and "no_support" in flags) or score >= 25:
                recommendation = "Memory Care"
                issues = [f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns', 'dealing with severe memory issues']) if 'severe_cognitive_risk' in flags else ''}",
                          f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else ''}",
                          f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else ''}"]
            elif score >= 15:
                recommendation = "Assisted Living"
                issues = [f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                          f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                          f"{random.choice(['having no one around to help', 'lacking regular support']) if 'no_support' in flags else random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                          f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns']) if 'severe_cognitive_risk' in flags else random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                          f"{random.choice(['facing safety risks at home', 'having major safety concerns']) if 'high_safety_concern' in flags else random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
            elif score >= 8:
                recommendation = "In-Home Care with Support"
                issues = [f"{random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                          f"{random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                          f"{random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                          f"{random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                          f"{random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
            issues = [i for i in issues if i][:3]  # Top 3 issues

            st.write(f"| {case['name']} | {score} | {recommendation} | {', '.join(issues) if issues else 'None'} |")

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
            st.markdown("<p class='question-text'>Your Financial Confidence</p>", unsafe_allow_html=True)
            st.write("First, let’s talk about your finances.")
            funding_options = {
                "1": "Not worried—I can afford any care I need",
                "2": "Somewhat worried—I’d need to budget carefully",
                "3": "Very worried—cost is a big concern for me",
                "4": "I am on Medicaid"
            }
            funding_key = radio_from_answer_map(
                label="How confident are you that your savings will cover long-term care?",
                amap=funding_options,
                key="funding_confidence_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if funding_key:
                funding_confidence = funding_options[funding_key]
                if funding_confidence == "I am on Medicaid":
                    st.write("We can connect you to Medicaid-friendly care options—just tap here.", unsafe_allow_html=True)
                    if st.button("Get Options", key="medicaid_options"):
                        st.session_state.step = "tools"
                        st.rerun()
                else:
                    care_context["care_flags"]["funding_confidence"] = funding_confidence
                    st.session_state.care_context = care_context
                    st.write(f"You feel: {care_context['care_flags']['funding_confidence']}")
            if st.button("Next", key="planner_next_1", disabled=not funding_key or funding_confidence == "I am on Medicaid"):
                st.session_state.planner_step = 2
                st.rerun()
            if st.button("Go Back", key="planner_back_1", disabled=True):
                pass

        elif st.session_state.planner_step == 2:
            st.markdown("<p class='question-text'>Your Cognition</p>", unsafe_allow_html=True)
            st.write("Next, let’s talk about your memory and thinking.")
            cognition_options = {
                "1": "My memory feels sharp—no real issues",
                "2": "Occasional lapses—like forgetting what I was saying",
                "3": "Noticeable problems—like missing meds or appointments",
                "4": "Serious confusion—like losing track of time, place, or familiar faces"
            }
            cognition_key = radio_from_answer_map(
                label="How would you describe your memory and focus?",
                amap=cognition_options,
                key="cognition_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if cognition_key:
                cognition = cognition_options[cognition_key]
                care_context["care_flags"]["cognitive_function"] = cognition
                st.session_state.care_context = care_context
                st.write(f"You noted: {care_context['care_flags']['cognitive_function']}")
            if st.button("Next", key="planner_next_2", disabled=not cognition_key):
                st.session_state.planner_step = 3
                st.rerun()
            if st.button("Go Back", key="planner_back_2"):
                st.session_state.planner_step = 1
                st.rerun()

        elif st.session_state.planner_step == 3:
            st.markdown("<p class='question-text'>Your Caregiver Support</p>", unsafe_allow_html=True)
            cog = care_context["care_flags"].get("cognitive_function", "")
            funding = care_context["care_flags"].get("funding_confidence", "")
            if "Occasional lapses" in cog or "Noticeable problems" in cog or "Serious confusion" in cog:
                if "Not worried—I can afford any care I need" in funding:
                    st.write(f"Great, you’re financially secure. With {cog.lower()}, would 24/7 caregivers at home work?")
                else:
                    st.write(f"Since you’ve noted {cog.lower()}, it’s key to know: who’s there if memory slips?")
            else:
                st.write("How often do you have someone to help with daily needs?")
            caregiver_options = {
                "1": "Someone’s with me all the time",
                "2": "Support most days",
                "3": "Someone checks in occasionally",
                "4": "No regular support"
            }
            caregiver_key = radio_from_answer_map(
                label="How often is someone available to assist you?",
                amap=caregiver_options,
                key="caregiver_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if caregiver_key:
                caregiver = caregiver_options[caregiver_key]
                care_context["care_flags"]["caregiver_support"] = caregiver
                st.session_state.care_context = care_context
                st.write(f"Support level: {care_context['care_flags']['caregiver_support']}")
            if st.button("Next", key="planner_next_3", disabled=not caregiver_key):
                st.session_state.planner_step = 4
                st.rerun()
            if st.button("Go Back", key="planner_back_3"):
                st.session_state.planner_step = 2
                st.rerun()

        elif st.session_state.planner_step == 4:
            st.markdown("<p class='question-text'>Your Medication Management</p>", unsafe_allow_html=True)
            takes_meds = st.radio(
                "Do you take any daily prescription meds (e.g., for heart, mood, or memory)?",
                ["No", "Yes"],
                index=0,
                key="takes_meds_select"
            )
            if takes_meds == "Yes":
                cog = care_context["care_flags"].get("cognitive_function", "")
                if "Occasional lapses" in cog or "Noticeable problems" in cog or "Serious confusion" in cog:
                    st.write(f"Since you’ve noted {cog.lower()}, how confident are you with your meds?")
                else:
                    st.write("How confident are you managing your meds?")
                med_options = {
                    "1": "I manage them rock-solid",
                    "2": "I’m pretty sure, with reminders",
                    "3": "I need help sometimes",
                    "4": "I can’t count on myself"
                }
                med_key = radio_from_answer_map(
                    label="How do you handle your medications?",
                    amap=med_options,
                    key="med_confidence_select",
                    default_key="1",
                    show_debug=st.session_state.get("show_qa", False)
                )
                if med_key:
                    med_confidence = med_options[med_key]
                    care_context["care_flags"]["med_adherence"] = med_confidence
                    st.session_state.care_context = care_context
                    st.write(f"Med management: {care_context['care_flags']['med_adherence']}")
            if st.button("Next", key="planner_next_4", disabled=(takes_meds != "No" and not med_key)):
                st.session_state.planner_step = 5
                st.rerun()
            if st.button("Go Back", key="planner_back_4"):
                st.session_state.planner_step = 3
                st.rerun()

        elif st.session_state.planner_step == 5:
            st.markdown("<p class='question-text'>Your Daily Independence</p>", unsafe_allow_html=True)
            st.write("Now, let’s look at your daily routine.")
            independence_options = {
                "1": "I’m fully independent and handle all tasks on my own",
                "2": "I occasionally need reminders or light assistance",
                "3": "I need help with some of these tasks regularly",
                "4": "I rely on someone else for most daily tasks"
            }
            independence_key = radio_from_answer_map(
                label="How independent are you with tasks like bathing, dressing, or meals?",
                amap=independence_options,
                key="independence_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if independence_key:
                independence = independence_options[independence_key]
                care_context["care_flags"]["independence_level"] = independence
                st.session_state.care_context = care_context
                st.write(f"Independence: {care_context['care_flags']['independence_level']}")
            if st.button("Next", key="planner_next_5", disabled=not independence_key):
                st.session_state.planner_step = 6
                st.rerun()
            if st.button("Go Back", key="planner_back_5"):
                st.session_state.planner_step = 4
                st.rerun()

        elif st.session_state.planner_step == 6:
            st.markdown("<p class='question-text'>Your Mobility</p>", unsafe_allow_html=True)
            st.write("Let’s talk about getting around.")
            mobility_options = {
                "1": "I walk easily without any support",
                "2": "I use a cane or walker for longer distances",
                "3": "I need assistance for most movement around the home",
                "4": "I am mostly immobile or need a wheelchair"
            }
            mobility_key = radio_from_answer_map(
                label="How would you describe your mobility?",
                amap=mobility_options,
                key="mobility_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if mobility_key:
                mobility = mobility_options[mobility_key]
                care_context["care_flags"]["mobility_issue"] = mobility != mobility_options["1"]
                if mobility != mobility_options["1"]:
                    care_context["derived_flags"]["inferred_mobility_aid"] = mobility
                st.session_state.care_context = care_context
                st.write(f"Mobility: {care_context['care_flags']['mobility_issue']}")
            if st.button("Next", key="planner_next_6", disabled=not mobility_key):
                st.session_state.planner_step = 7
                st.rerun()
            if st.button("Go Back", key="planner_back_6"):
                st.session_state.planner_step = 5
                st.rerun()

        elif st.session_state.planner_step == 7:
            st.markdown("<p class='question-text'>Your World</p>", unsafe_allow_html=True)
            st.write("Finally, let’s look at your living situation.")

            st.markdown("<p class='question-text'>Social Connection</p>", unsafe_allow_html=True)
            st.write("How connected are you with family, friends, or neighbors?")
            social_options = {
                "1": "Daily visits or calls",
                "2": "Weekly check-ins",
                "3": "Monthly calls",
                "4": "Mostly alone"
            }
            social_key = radio_from_answer_map(
                label="How often do you see or hear from people close to you?",
                amap=social_options,
                key="social_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if social_key:
                social = social_options[social_key]
                care_context["care_flags"]["social_connection"] = social
                st.session_state.care_context = care_context
                st.write(f"Social: {care_context['care_flags']['social_connection']}")

            st.markdown("<p class='question-text'>Geography & Access</p>", unsafe_allow_html=True)
            chronic_conditions = care_context["care_flags"].get("chronic_conditions", [])
            if chronic_conditions:
                st.write(f"With conditions like {', '.join(chronic_conditions)}, how easy is it to reach doctors?")
            else:
                st.write("How easy is it to reach doctors or stores?")
            geo_options = {
                "1": "Easy—I can walk or drive",
                "2": "Needs a ride, but manageable",
                "3": "Pretty hard without help",
                "4": "Impossible alone"
            }
            geo_key = radio_from_answer_map(
                label="How accessible are healthcare and services?",
                amap=geo_options,
                key="geography_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if geo_key:
                geography = geo_options[geo_key]
                care_context["care_flags"]["geographic_access"] = geography
                st.session_state.care_context = care_context
                st.write(f"Access: {care_context['care_flags']['geographic_access']}")

            st.markdown("<p class='question-text'>Home Safety</p>", unsafe_allow_html=True)
            st.write("How safe do you feel at home?")
            safety_options = {
                "1": "Very safe—I have everything I need",
                "2": "Mostly safe, but a few concerns",
                "3": "Sometimes I feel unsafe",
                "4": "Often feel at risk"
            }
            safety_key = radio_from_answer_map(
                label="How safe is your home for falls or emergencies?",
                amap=safety_options,
                key="safety_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if safety_key:
                safety = safety_options[safety_key]
                care_context["care_flags"]["falls_risk"] = safety in ["Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"]
                st.session_state.care_context = care_context
                st.write(f"Safety: {care_context['care_flags']['falls_risk']}")

            st.markdown("<p class='question-text'>Fall History</p>", unsafe_allow_html=True)
            st.write("Based on your safety answer, let’s check this.")
            fall_options = {"1": "Yes", "2": "No", "3": "Unsure"}
            fall_key = radio_from_answer_map(
                label="Have you fallen in the last six months?",
                amap=fall_options,
                key="fall_history_select",
                default_key="2",
                show_debug=st.session_state.get("show_qa", False)
            )
            if fall_key:
                fall_history = fall_options[fall_key]
                care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
                st.session_state.care_context = care_context
                st.write(f"Fall history: {care_context['derived_flags'].get('recent_fall', 'Not set')}")

            st.markdown("<p class='question-text'>Chronic Conditions</p>", unsafe_allow_html=True)
            st.write("Any ongoing health issues?")
            condition_options = ["Diabetes", "Hypertension", "Dementia", "Parkinson's", "COPD", "CHF", "Arthritis", "Stroke"]
            conditions = st.multiselect("Which chronic conditions do you have?", condition_options, key="chronic_conditions_select")
            if conditions:
                care_context["care_flags"]["chronic_conditions"] = conditions
                st.session_state.care_context = care_context
                st.write(f"Chronic conditions: {', '.join(care_context['care_flags']['chronic_conditions'])}")

            if st.button("Next", key="planner_next_7", disabled=not (social_key and geo_key and safety_key and fall_key and conditions is not None)):
                st.session_state.planner_step = 8
                st.rerun()
            if st.button("Go Back", key="planner_back_7"):
                st.session_state.planner_step = 6
                st.rerun()

        elif st.session_state.planner_step == 8:
            st.markdown("<p class='question-text'>Your Home Preference</p>", unsafe_allow_html=True)
            st.write("Lastly, how do you feel about staying home?")
            goal_options = {
                "1": "Not important—I’m open to other options",
                "2": "Somewhat important—I’d prefer to stay but could move",
                "3": "Very important—I strongly want to stay home"
            }
            goal_key = radio_from_answer_map(
                label="How important is it to stay in your current home?",
                amap=goal_options,
                key="goal_select",
                default_key="1",
                show_debug=st.session_state.get("show_qa", False)
            )
            if goal_key:
                goal = goal_options[goal_key]
                care_context["care_flags"]["living_goal"] = goal
                st.session_state.care_context = care_context
                st.write(f"Preference: {care_context['care_flags']['living_goal']}")
            if st.button("Get Recommendation", key="planner_next_8", disabled=not goal_key):
                st.session_state.planner_step = 9
                st.rerun()
            if st.button("Go Back", key="planner_back_8"):
                st.session_state.planner_step = 7
                st.rerun()

        elif st.session_state.planner_step == 9:
            st.subheader("Care Recommendation")
            st.write("Based on your answers, here’s our suggestion.")
            flags = []
            # Financial
            funding = care_context["care_flags"].get("funding_confidence", "")
            if funding in ["Very worried—cost is a big concern for me", "Somewhat worried—I’d need to budget carefully"]:
                flags.append("needs_financial_assistance")
            elif funding == "Not worried—I can afford any care I need":
                flags.append("can_afford_care")

            # Cognition
            cog = care_context["care_flags"].get("cognitive_function", "")
            conditions = care_context["care_flags"].get("chronic_conditions", [])
            if "Serious confusion" in cog or "Dementia" in conditions or "Parkinson's" in conditions:
                flags.append("severe_cognitive_risk")
            elif "Noticeable problems" in cog:
                flags.append("moderate_cognitive_decline")
            elif "Occasional lapses" in cog:
                flags.append("mild_cognitive_decline")

            # Caregiver Support
            support = care_context["care_flags"].get("caregiver_support", "")
            if "No regular support" in support:
                flags.append("no_support")
            elif "Someone checks in occasionally" in support:
                flags.append("limited_support")
            elif "Support most days" in support or "Someone’s with me all the time" in support:
                flags.append("adequate_support")

            # Medication Adherence
            med_adherence = care_context["care_flags"].get("med_adherence", "No")
            if med_adherence in ["I need help sometimes", "I can’t count on myself"]:
                flags.append("med_adherence_risk")

            # Independence
            indep = care_context["care_flags"].get("independence_level", "")
            if "I rely on someone else for most daily tasks" in indep:
                flags.append("high_dependence")
            elif "I need help with some of these tasks regularly" in indep:
                flags.append("moderate_dependence")

            # Mobility
            mobility = care_context["derived_flags"].get("inferred_mobility_aid", "")
            if "I need assistance for most movement around the home" in mobility or "I am mostly immobile or need a wheelchair" in mobility:
                flags.append("high_mobility_dependence")
            elif "I use a cane or walker for longer distances" in mobility:
                flags.append("moderate_mobility")

            # Social Connection
            social = care_context["care_flags"].get("social_connection", "")
            if "Mostly alone" in social:
                flags.append("high_risk")
            elif "Monthly calls" in social:
                flags.append("moderate_risk")

            # Geography & Access
            geo = care_context["care_flags"].get("geographic_access", "")
            if "Pretty hard without help" in geo or "Impossible alone" in geo:
                flags.append("very_low_access")

            # Home Safety
            safety = care_context["care_flags"].get("falls_risk", False)
            if safety:
                flags.append("moderate_safety_concern")

            # Fall History
            if care_context["derived_flags"].get("recent_fall", False):
                flags.append("high_safety_concern")

            # Score Calculation
            score = 0
            if "severe_cognitive_risk" in flags and "adequate_support" in flags:
                score += 10
            elif "severe_cognitive_risk" in flags:
                score += 15
            if "moderate_cognitive_decline" in flags:
                score += 5
            if "mild_cognitive_decline" in flags:
                score += 3
            if "high_dependence" in flags or "high_mobility_dependence" in flags:
                score += 10
            if "moderate_dependence" in flags or "moderate_mobility" in flags:
                score += 5
            if "no_support" in flags:
                score += 7
            if "limited_support" in flags:
                pass  # No penalty for borderline support
            if "adequate_support" in flags:
                score -= 3  # Reduced to balance no-care threshold
            if "high_risk" in flags:
                score += 6
            if "moderate_risk" in flags:
                score += 3
            if "med_adherence_risk" in flags:
                score += 6
            if "very_low_access" in flags:
                score += 4
            if "moderate_safety_concern" in flags:
                score += 5
            if "high_safety_concern" in flags:
                score += 8
            if "chronic_health_risk" in flags:
                score += 7

            # Floor score at 0
            score = max(0, score)

            # Determine recommendation
            recommendation = "No Care Needed at This Time"
            issues = []
            if ("severe_cognitive_risk" in flags and "no_support" in flags) or score >= 25:
                recommendation = "Memory Care"
                issues = [f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns', 'dealing with severe memory issues']) if 'severe_cognitive_risk' in flags else ''}",
                          f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else ''}",
                          f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else ''}"]
            elif score >= 15:
                recommendation = "Assisted Living"
                issues = [f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                          f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                          f"{random.choice(['having no one around to help', 'lacking regular support']) if 'no_support' in flags else random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                          f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns']) if 'severe_cognitive_risk' in flags else random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                          f"{random.choice(['facing safety risks at home', 'having major safety concerns']) if 'high_safety_concern' in flags else random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
            elif score >= 8:
                recommendation = "In-Home Care with Support"
                issues = [f"{random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                          f"{random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                          f"{random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                          f"{random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                          f"{random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
            issues = [i for i in issues if i][:3]  # Top 3 issues

            st.write(f"| {case['name']} | {score} | {recommendation} | {', '.join(issues) if issues else 'None'} |")

def render_step(step):
    if step == "intro":
        st.title("Senior Navigator")
        st.write("Welcome! Start by exploring your care options.")
        if st.button("Get Started"):
            st.session_state.step = "planner"
            st.session_state.planner_step = 1
            st.rerun()
    elif step == "planner":
        render_planner()
    else:
        st.error("Unknown step: " + step)
