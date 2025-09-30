import streamlit as st

QUESTIONS = [
    ("funding_confidence", "How confident do you feel about being able to afford care if you need it?",
        ["Very confident — I can afford any care I need",
         "Somewhat confident — I’d need to budget carefully",
         "Not confident — cost would be a major concern",
         "I am on Medicaid"]),
    ("cognition_level", "How’s the person's memory and thinking been lately?",
        ["Sharp — no real issues",
         "Occasional lapses",
         "Noticeable problems (miss meds/appointments)",
         "Serious confusion"]),
    ("adl_need", "How much support does the person usually need with daily activities like meals, bathing, or chores?",
        ["I handle most things on my own",
         "I occasionally need reminders or light assistance",
         "I need regular help with some tasks",
         "I rely on someone else for most daily tasks"]),
    ("meds_complexity", "Does the person take medications, and how complex is the routine?",
        ["No, none",
         "Few / simple",
         "Several / complex",
         "Not sure"]),
    ("independence_level", "How independent is the person overall with day-to-day life?",
        ["Independent",
         "Needs some help",
         "Needs a lot of help"]),
    ("mobility", "How does the person usually get around?",
        ["Gets around easily without assistance",
         "Sometimes uses a cane",
         "Regularly uses a walker",
         "Uses a wheelchair"]),
    ("social_isolation", "How connected does the person feel to others day-to-day?",
        ["Frequent visitors and activities",
         "Sometimes see people, but not often",
         "Often feels alone with little contact"]),
    ("geographic_access", "How easy is it for the person to get to services like doctors, stores, or activities?",
        ["Very easy",
         "Somewhat easy",
         "Difficult"]),
    ("chronic_conditions", "Does the person have any ongoing health conditions? Select all that apply.",
        ["Diabetes","Hypertension","Dementia","Parkinson’s","Stroke","CHF","COPD","Arthritis"]),
    ("home_safety", "How safe does the person feel at home?",
        ["Very safe",
         "Some concerns",
         "Often feels at risk"]),
    ("recent_fall", "Has the person had a fall lately?",
        ["Yes","No","Unsure"]),
    ("home_preference", "When the person thinks about the future, where would they prefer to receive care?",
        ["Prefer to stay home",
         "Open to assisted living if advised",
         "Memory care if needed"])
]

def run_flow():
    care_context = st.session_state.care_context
    step = st.session_state.planner_step

    if step == 0:
        st.subheader("Planning Context")
        care_context["audience_type"] = st.radio(
            "Who are you planning care for today?",
            ["One person","Two people","Professional"]
        )
        if care_context["audience_type"] == "One person":
            care_context["person_a_name"] = st.text_input("What’s their name?")
        elif care_context["audience_type"] == "Two people":
            care_context["person_a_name"] = st.text_input("What’s the first person’s name?")
            care_context["person_b_name"] = st.text_input("What’s the second person’s name?")
        else:
            care_context["person_a_name"] = st.text_input("Person A name")
            care_context["person_b_name"] = st.text_input("Person B name (if applicable)")
        if st.button("Next"):
            st.session_state.planner_step = 1
            st.experimental_rerun()
    elif 1 <= step <= len(QUESTIONS):
        key, prompt, options = QUESTIONS[step-1]
        st.subheader(f"Step {step}: {prompt}")
        if key == "chronic_conditions":
            care_context[key] = st.multiselect(prompt, options)
        else:
            care_context["flags"][key] = st.radio(prompt, options)
        if st.button("Next"):
            st.session_state.planner_step += 1
            st.experimental_rerun()
    else:
        st.subheader("Recommendation")
        st.write("Here is where the recommendation logic will run based on collected data.")
