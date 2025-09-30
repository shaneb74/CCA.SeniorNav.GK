import streamlit as st

QUESTIONS = [
    ("funding_confidence", "How confident do you feel about being able to afford care if you need it?",
        ["Very confident — I can afford any care I need",
         "Somewhat confident — I’d need to budget carefully",
         "Not confident — cost would be a major concern",
         "I am on Medicaid"]),
    ("cognition_level", "How’s {name_possessive} memory and thinking been lately?",
        ["Sharp — no real issues",
         "Occasional lapses",
         "Noticeable problems (miss meds/appointments)",
         "Serious confusion"]),
    ("adl_need", "How much support does {name} usually need with daily activities like meals, bathing, or chores?",
        ["I handle most things on my own",
         "I occasionally need reminders or light assistance",
         "I need regular help with some tasks",
         "I rely on someone else for most daily tasks"]),
    ("meds_complexity", "Does {name} take medications, and how complex is the routine?",
        ["No, none",
         "Few / simple",
         "Several / complex",
         "Not sure"]),
    ("independence_level", "How independent is {name} overall with day-to-day life?",
        ["Independent",
         "Needs some help",
         "Needs a lot of help"]),
    ("mobility", "How does {name} usually get around?",
        ["Gets around easily without assistance",
         "Sometimes uses a cane",
         "Regularly uses a walker",
         "Uses a wheelchair"]),
    ("social_isolation", "How connected does {name} feel to others day-to-day?",
        ["Frequent visitors and activities",
         "Sometimes see people, but not often",
         "Often feels alone with little contact"]),
    ("geographic_access", "How easy is it for {name} to get to services like doctors, stores, or activities?",
        ["Very easy",
         "Somewhat easy",
         "Difficult"]),
    ("chronic_conditions", "Does {name} have any ongoing health conditions? Select all that apply.",
        ["Diabetes","Hypertension","Dementia","Parkinson’s","Stroke","CHF","COPD","Arthritis"]),
    ("home_safety", "How safe does {name} feel at home?",
        ["Very safe",
         "Some concerns",
         "Often feels at risk"]),
    ("recent_fall", "Has {name} had a fall lately?",
        ["Yes","No","Unsure"]),
    ("home_preference", "When {name} thinks about the future, where would they prefer to receive care?",
        ["Prefer to stay home",
         "Open to assisted living if advised",
         "Memory care if needed"])
]

def _display_guided_header():
    st.markdown("### Guided Care Plan")

def _name_or_default():
    ctx = st.session_state.care_context
    n = ctx.get("person_a_name") or "the person you’re planning for"
    # possessive helper
    possessive = n + "'" if n.endswith("s") else n + "'s"
    return n, possessive

def run_flow():
    care_context = st.session_state.care_context
    step = st.session_state.planner_step

    # Step 0: Audiencing (app-level: Senior Care Navigator)
    if step == 0:
        st.subheader("Planning Context")
        care_context["audience_type"] = st.radio(
            "Who are you planning care for today?",
            ["One person","Two people","Professional"],
            index=0
        )
        if care_context["audience_type"] == "One person":
            care_context["person_a_name"] = st.text_input("What’s their name?")
        elif care_context["audience_type"] == "Two people":
            care_context["person_a_name"] = st.text_input("What’s the first person’s name?")
            care_context["person_b_name"] = st.text_input("What’s the second person’s name?")
        else:
            who = st.radio("How many people are you helping?", ["One","Two"], horizontal=True, index=0)
            care_context["person_a_name"] = st.text_input("Person A name")
            care_context["person_b_name"] = st.text_input("Person B name (if applicable)") if who == "Two" else None

        if st.button("Next"):
            st.session_state.planner_step = 1
            st.rerun()

    # Steps 1..N: Guided Care Plan module
    elif 1 <= step <= len(QUESTIONS):
        _display_guided_header()
        name, name_possessive = _name_or_default()
        key, prompt_tmpl, options = QUESTIONS[step-1]
        prompt = prompt_tmpl.format(name=name, name_possessive=name_possessive)
        st.subheader(f"Step {step}: {prompt}")

        if key == "chronic_conditions":
            # store in top-level list for easy access
            care_context["chronic_conditions"] = st.multiselect("Select all that apply", options, default=care_context.get("chronic_conditions", []))
        else:
            sel = st.radio("", options, index=None, key=f"q_{key}")
            if sel is not None:
                care_context["flags"][key] = sel

        cols = st.columns(2)
        with cols[0]:
            if st.button("Back"):
                st.session_state.planner_step = max(0, step-1)
                st.rerun()
        with cols[1]:
            next_disabled = False
            if key == "chronic_conditions":
                next_disabled = False  # allow none selected
            else:
                next_disabled = care_context["flags"].get(key) is None
            if st.button("Next", disabled=next_disabled):
                st.session_state.planner_step = step + 1
                st.rerun()

    # Recommendation
    else:
        _display_guided_header()
        st.subheader("Recommendation")
        st.write("This is where your recommendation logic will run based on collected flags and chronic conditions.")
        st.code(str(st.session_state.care_context), language="python")
        if st.button("Start over"):
            st.session_state.planner_step = 0
            st.rerun()
