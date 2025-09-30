import streamlit as st
import random

# Lock fonts early-no helpers, no overrides
st.markdown(
    '''<style>
    .stMarkdown {
        font-size: 22px !important;
    }
    .stRadio > div > label span {
        font-size: 24px !important;
    }
    .stRadio > div > label {
        line-height: 1.5;
        margin: 6px 0;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>''',
    unsafe_allow_html=True
)

# Session state setup
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {}
    }

care_context = st.session_state.care_context

def render_planner():
    st.header("Guided Care Plan")
    st.write("Let’s walk through your care needs.")
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1

    # Step 1: Funding
    if st.session_state.planner_step == 1:
        st.subheader("Your Financial Confidence")
        st.write("Let’s start with something personal—how do you feel about your finances?")
        funding_options = {
            "1": "Not worried—I can afford any care I need",
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
        if funding_confidence == "I am on Medicaid":
            st.write("That’s great—we can help you find Medicaid-friendly options. Interested?")
            if st.button("Yes, Show Me", key="medicaid_options"):
                st.session_state.step = "tools"
                st.rerun()
        elif funding_confidence:
            care_context["care_flags"]["funding_confidence"] = funding_confidence
            st.session_state.care_context = care_context
            st.write(f"I hear you—it sounds like you feel {care_context['care_flags']['funding_confidence'].lower()}. That’s a good starting point.")
        if st.button("Next", key="planner_next_1", disabled=not funding_confidence or funding_confidence == "I am on Medicaid"):
            st.session_state.planner_step = 2
            st.rerun()
        if st.button("Go Back", key="planner_back_1", disabled=True):
            pass

    # Step 2: Cognition
    elif st.session_state.planner_step == 2:
        st.subheader("Your Cognition")
        st.write("Now, let’s talk about your memory and thinking—how’s it been for you lately?")
        cognition_options = {
            "1": "My memory feels sharp—no real issues",
            "2": "Occasional lapses—like forgetting what I was saying",
            "3": "Noticeable problems—like missing meds or appointments",
            "4": "Serious confusion—like losing track of time, place, or familiar faces"
        }
        cognition_options_list = list(cognition_options.values())
        cognition = st.radio(
            "How would you describe your memory and focus these days?",
            cognition_options_list,
            key="cognition_select"
        )
        if cognition:
            care_context["care_flags"]["cognitive_function"] = cognition
            st.session_state.care_context = care_context
            if "lapses" in cognition.lower() or "problems" in cognition.lower() or "confusion" in cognition.lower():
                st.write(f"Thanks for sharing that. When those {cognition.split('—')[0].lower()} happen, is there someone around to help?")
            else:
                st.write(f"That’s reassuring to hear. You’re doing great with {cognition.lower()}.")
        if st.button("Next", key="planner_next_2", disabled=not cognition):
            st.session_state.planner_step = 3
            st.rerun()
        if st.button("Go Back", key="planner_back_2"):
            st.session_state.planner_step = 1
            st.rerun()

    # Step 3: Caregiver Support
    elif st.session_state.planner_step == 3:
        st.subheader("Your Caregiver Support")
        cog = care_context["care_flags"].get("cognitive_function", "")
        funding = care_context["care_flags"].get("funding_confidence", "")
        if "lapses" in cog.lower() or "problems" in cog.lower() or "confusion" in cog.lower():
            if "Not worried—I can afford any care I need" in funding:
                st.write(f"With your financial security and {cog.lower()}, would having 24/7 caregivers at home be an option?")
            else:
                st.write(f"Since you mentioned {cog.lower()}, who steps in when memory gets tricky?")
        else:
            st.write("It’s good to know who’s there for you—how often does someone help with daily needs?")
        caregiver_options = {
            "1": "Someone’s with me all the time",
            "2": "Support most days",
            "3": "Someone checks in occasionally",
            "4": "No regular support"
        }
        caregiver_options_list = list(caregiver_options.values())
        caregiver = st.radio(
            "How often do you have someone to lean on for help?",
            caregiver_options_list,
            key="caregiver_select"
        )
        if caregiver:
            care_context["care_flags"]["caregiver_support"] = caregiver
            st.session_state.care_context = care_context
            if "No regular support" in caregiver:
                st.write("That can feel isolating. Would you like help finding someone to check in?")
            else:
                st.write(f"That sounds comforting—{caregiver.lower()} is a solid support.")
        if st.button("Next", key="planner_next_3", disabled=not caregiver):
            st.session_state.planner_step = 4
            st.rerun()
        if st.button("Go Back", key="planner_back_3"):
            st.session_state.planner_step = 2
            st.rerun()

    # Step 4: Medication Management
    elif st.session_state.planner_step == 4:
        st.subheader("Your Medication Management")
        takes_meds = st.radio(
            "Do you take any daily meds, like for your heart, mood, or memory?",
            ["No", "Yes"],
            index=0,
            key="takes_meds_select"
        )
        if takes_meds == "Yes":
            cog = care_context["care_flags"].get("cognitive_function", "")
            if "lapses" in cog.lower() or "problems" in cog.lower() or "confusion" in cog.lower():
                st.write(f"With {cog.lower()}, how do you feel about keeping up with your meds?")
            else:
                st.write("You’re on meds—how confident are you managing them?")
            med_options = {
                "1": "I manage them rock-solid",
                "2": "I’m pretty sure, with reminders",
                "3": "I need help sometimes",
                "4": "I can’t count on myself"
            }
            med_options_list = list(med_options.values())
            med_confidence = st.radio(
                "How do you feel about staying on top of your medications?",
                med_options_list,
                key="med_confidence_select"
            )
            if med_confidence:
                care_context["care_flags"]["med_adherence"] = med_confidence
                st.session_state.care_context = care_context
                if "need help" in med_confidence.lower() or "can’t count" in med_confidence.lower():
                    st.write("That’s okay—we can find ways to make it easier. Want to explore options?")
                else:
                    st.write(f"Good to know—you’re handling {med_confidence.lower()} well.")
        if st.button("Next", key="planner_next_4", disabled=(takes_meds != "No" and not med_confidence)):
            st.session_state.planner_step = 5
            st.rerun()
        if st.button("Go Back", key="planner_back_4"):
            st.session_state.planner_step = 3
            st.rerun()

    # Step 5: Daily Independence
    elif st.session_state.planner_step == 5:
        st.subheader("Your Daily Independence")
        st.write("Let’s talk about your day-to-day—how are you managing?")
        independence_options = {
            "1": "I’m fully independent and handle all tasks on my own",
            "2": "I occasionally need reminders or light assistance",
            "3": "I need help with some of these tasks regularly",
            "4": "I rely on someone else for most daily tasks"
        }
        independence_options_list = list(independence_options.values())
        independence = st.radio(
            "How much support do you need with things like bathing, dressing, or meals?",
            independence_options_list,
            key="independence_select"
        )
        if independence:
            care_context["care_flags"]["independence_level"] = independence
            st.session_state.care_context = care_context
            if "need help" in independence.lower() or "rely" in independence.lower():
                st.write("That’s normal—want to talk about what help looks like for you?")
            else:
                st.write(f"Nice—you’re doing great with {independence.lower()}.")
        if st.button("Next", key="planner_next_5", disabled=not independence):
            st.session_state.planner_step = 6
            st.rerun()
        if st.button("Go Back", key="planner_back_5"):
            st.session_state.planner_step = 4
            st.rerun()

    # Step 6: Mobility
    elif st.session_state.planner_step == 6:
        st.subheader("Your Mobility")
        st.write("How’s getting around been for you lately?")
        mobility_options = {
            "1": "I walk easily without any support",
            "2": "I use a cane or walker for longer distances",
            "3": "I need assistance for most movement around the home",
            "4": "I am mostly immobile or need a wheelchair"
        }
        mobility_options_list = list(mobility_options.values())
        mobility = st.radio(
            "How would you describe how you move around these days?",
            mobility_options_list,
            key="mobility_select"
        )
        if mobility:
            care_context["care_flags"]["mobility_issue"] = mobility != mobility_options_list[0]
            if mobility != mobility_options_list[0]:
                care_context["derived_flags"]["inferred_mobility_aid"] = mobility
            st.session_state.care_context = care_context
            if "assistance" in mobility.lower() or "immobile" in mobility.lower():
                st.write("That can be a challenge. Is there anything making it harder at home?")
            else:
                st.write(f"Great—you’re moving well with {mobility.lower()}.")
        if st.button("Next", key="planner_next_6", disabled=not mobility):
            st.session_state.planner_step = 7
            st.rerun()
        if st.button("Go Back", key="planner_back_6"):
            st.session_state.planner_step = 5
            st.rerun()

    # Step 7: Your World
    elif st.session_state.planner_step == 7:
        st.subheader("Your World")
        st.write("So, tell me—what’s home like for you these days?")
        social = st.radio(
            "How often do you connect with family, friends, or neighbors?",
            ["Daily visits or calls", "Weekly check-ins", "Monthly calls", "Mostly alone"],
            key="social_select"
        )
        if social:
            care_context["care_flags"]["social_connection"] = social
            st.session_state.care_context = care_context
            if "mostly alone" in social.lower():
                st.write("That can feel isolating. Do family or neighbors check in at all?")
            else:
                st.write(f"That’s nice—{social.lower()} keeps things connected.")

        st.write("What about getting out—how easy is it to reach doctors or stores?")
        geography = st.radio(
            "How accessible are healthcare and services for you?",
            ["Easy—I can walk or drive", "Needs a ride, but manageable", "Pretty hard without help", "Impossible alone"],
            key="geography_select"
        )
        if geography:
            care_context["care_flags"]["geographic_access"] = geography
            st.session_state.care_context = care_context
            if "hard" in geography.lower() or "impossible" in geography.lower():
                st.write("That sounds tough. Is transportation the main hurdle?")
            else:
                st.write(f"Good to know—{geography.lower()} works for you.")

        st.write("Any little things make you worry about safety at home?")
        safety = st.radio(
            "How safe do you feel with falls or emergencies?",
            ["Very safe—I have everything I need", "Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"],
            key="safety_select"
        )
        if safety:
            care_context["care_flags"]["falls_risk"] = safety in ["Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"]
            st.session_state.care_context = care_context
            if "unsafe" in safety.lower() or "concerns" in safety.lower():
                st.write("That’s worth a closer look. Anything specific, like stairs or lighting?")
            else:
                st.write(f"Glad to hear—{safety.lower()} sounds reassuring.")

        st.write("Based on that, let’s check something quick—have you had any falls lately?")
        fall_history = st.radio(
            "Have you fallen in the last six months?",
            ["Yes", "No", "Unsure"],
            key="fall_history_select"
        )
        if fall_history:
            care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
            st.session_state.care_context = care_context
            if fall_history == "Yes":
                st.write("Thanks for letting me know. Was it a one-time thing or something recurring?")
            else:
                st.write(f"Good—{fall_history.lower()} is a positive sign.")

        st.write("Any ongoing health issues we should know about?")
        condition_options = ["Diabetes", "Hypertension", "Dementia", "Parkinson's", "COPD", "CHF", "Arthritis", "Stroke"]
        conditions = st.multiselect("Which chronic conditions do you have?", condition_options, key="chronic_conditions_select")
        if conditions:
            care_context["care_flags"]["chronic_conditions"] = conditions
            st.session_state.care_context = care_context
            if len(conditions) > 1:
                st.write(f"Got it—you’re managing {', '.join(conditions[:-1]) + ' and ' + conditions[-1]}. That’s a lot—any giving you trouble?")
            else:
                st.write(f"Noted—{', '.join(conditions)} is on our radar. How’s that been for you?")

        if st.button("Next", key="planner_next_7", disabled=not (social and geography and safety and fall_history and conditions is not None)):
            st.session_state.planner_step = 8
            st.rerun()
        if st.button("Go Back", key="planner_back_7"):
            st.session_state.planner_step = 6
            st.rerun()

    # Step 8: Home Preference
    elif st.session_state.planner_step == 8:
        st.subheader("Your Home Preference")
        st.write("Lastly, how do you feel about staying in your current home?")
        goal_options = {
            "1": "Not important—I’m open to other options",
            "2": "Somewhat important—I’d prefer to stay but could move",
            "3": "Very important—I strongly want to stay home"
        }
        goal_options_list = list(goal_options.values())
        goal = st.radio(
            "How much does staying home mean to you right now?",
            goal_options_list,
            key="goal_select"
        )
        if goal:
            care_context["care_flags"]["living_goal"] = goal
            st.session_state.care_context = care_context
            if "important" in goal.lower():
                st.write("I get it—home’s special. What makes it so important to you?")
            else:
                st.write(f"That’s flexible—{goal.lower()} gives us room to explore.")
        if st.button("Get Recommendation", key="planner_next_8", disabled=not goal):
            st.session_state.planner_step = 9
            st.rerun()
        if st.button("Go Back", key="planner_back_8"):
            st.session_state.planner_step = 7
            st.rerun()

    # Step 9: Recommendation
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

        # Chronic Conditions
        conditions = care_context["care_flags"].get("chronic_conditions", [])
        if "CHF" in conditions or "COPD" in conditions:
            if "high_mobility_dependence" in flags or "high_safety_concern" in flags:
                flags.append("chronic_health_risk")

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
            score -= 5
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

        # Recommendation Logic
        if ("severe_cognitive_risk" in flags and "no_support" in flags) or score >= 25:
            recommendation = "Memory Care"
            issues = [f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns', 'dealing with severe memory issues']) if 'severe_cognitive_risk' in flags else ''}",
                      f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else ''}",
                      f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else ''}"]
            issues = [i for i in issues if i]
            st.write("**Care Recommendation: Memory Care**")
            message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, with {', '.join(issues[:-1]) + (' and ' if len(issues) > 1 else '') + issues[-1] if issues else 'significant challenges'}, Memory Care is the safest choice. If you have 24/7 skilled care at home, aging in place could work—let’s explore that."
        elif score >= 15:
            recommendation = "Assisted Living"
            issues = [f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                      f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                      f"{random.choice(['having no one around to help', 'lacking regular support']) if 'no_support' in flags else random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                      f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns']) if 'severe_cognitive_risk' in flags else random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                      f"{random.choice(['facing safety risks at home', 'having major safety concerns']) if 'high_safety_concern' in flags else random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
            issues = [i for i in issues if i][:3]  # Top 3 issues
            st.write("**Care Recommendation: Assisted Living**")
            preference = {
                "Very important—I strongly want to stay home": "Since staying home is important to you, let’s see how we can make that work with extra support.",
                "Somewhat important—I’d prefer to stay but could move": "You’d prefer to stay home, so let’s explore ways to make that possible.",
                "Not important—I’m open to other options": "You’re open to options, so let’s look at assisted living communities that feel like home."
            }.get(care_context["care_flags"].get("living_goal", ""), "If you’re unsure, let’s talk through the options together.")
            message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, we see you’re navigating challenges like {', '.join(issues[:-1]) + (' and ' if len(issues) > 1 else '') + issues[-1] if issues else 'various needs'}. Assisted Living would offer the support and safety you need. {preference}"
        elif score >= 8:
            recommendation = "In-Home Care with Support"
            issues = [f"{random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                      f"{random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                      f"{random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                      f"{random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                      f"{random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
            issues = [i for i in issues if i][:3]  # Top 3 issues
            st.write("**Care Recommendation: In-Home Care with Support**")
            preference = {
                "Very important—I strongly want to stay home": "Since staying home is important to you, let’s see how we can make that work with extra support.",
                "Somewhat important—I’d prefer to stay but could move": "You’d prefer to stay home, so let’s explore ways to make that possible.",
                "Not important—I’m open to other options": "You’re open to options, so let’s look at assisted living communities that feel like home."
            }.get(care_context["care_flags"].get("living_goal", ""), "If you’re unsure, let’s talk through the options together.")
            message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, we see you’re navigating challenges like {', '.join(issues[:-1]) + (' and ' if len(issues) > 1 else '') + issues[-1] if issues else 'mild needs'}. In-Home Care with Support would offer the help you need. {preference}"
        else:
            recommendation = "No Care Needed at This Time"
            st.write("**Care Recommendation: No Care Needed at This Time**")
            message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, it looks like you\'re managing well for now."
        st.write(message)

        if st.button("Restart", key="planner_restart"):
            st.session_state.planner_step = 1
            st.session_state.care_context = {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}}
            st.rerun()

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
