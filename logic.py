import streamlit as st

# Canonical question order and prompts; some steps personalized with name
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
         "I need regular help with some tasks (like meals, bathing, or managing meds)",
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
        ["Diabetes","Hypertension","Dementia","Parkinson's","Stroke","CHF","COPD","Arthritis"]),
    # Step 10 rewritten: home setup safety
    ("home_setup_safety", "How safe and manageable is {name_possessive} home for daily living as they age? Think stairs, bathrooms, lighting, grab bars, fall risks.",
        ["Ready for aging in place",
         "Mostly safe, needs a few improvements",
         "Not well set up / risky"]),
    # Step 11: fall window 6 months
    ("recent_fall", "Has {name} had a fall in the last 6 months?",
        ["Yes","No","Not sure"]),
    # Step 12: willingness to change setting
    ("move_willingness", "When it comes to where care happens, how open is {name} to changes if they’re recommended?",
        ["Strong preference to stay home",
         "Prefer home, open if strongly advised",
         "Open to either home or a move",
         "Comfortable with moving if it’s the better fit"]),
]

def _display_guided_header():
    st.markdown("### Guided Care Plan")

def _name_or_default():
    ctx = st.session_state.care_context
    n = ctx.get("person_a_name") or "the person you’re planning for"
    possessive = n + "'" if n.endswith("s") else n + "'s"
    return n, possessive

def _derive_after_answers():
    ctx = st.session_state.care_context
    flags = ctx.get("flags", {})
    derived = ctx.setdefault("derived", {})

    # Home setup derived flags
    safety = flags.get("home_setup_safety")
    if safety == "Ready for aging in place":
        derived["prep_checklist_trigger"] = False
        derived["home_mod_priority"] = "low"
        ctx["flags"]["home_setup_safety_value"] = "ready"
    elif safety == "Mostly safe, needs a few improvements":
        derived["prep_checklist_trigger"] = True
        derived["home_mod_priority"] = "medium"
        ctx["flags"]["home_setup_safety_value"] = "minor_improvements"
    elif safety == "Not well set up / risky":
        derived["prep_checklist_trigger"] = True
        derived["home_mod_priority"] = "high"
        ctx["flags"]["home_setup_safety_value"] = "unsafe"

    # Recent fall flags
    rf = flags.get("recent_fall")
    if rf == "Yes":
        ctx["flags"]["recent_fall_bool"] = True
        ctx["flags"]["recent_fall_window"] = "0_6mo"
    elif rf == "No":
        ctx["flags"]["recent_fall_bool"] = False
        ctx["flags"]["recent_fall_window"] = None
    elif rf == "Not sure":
        ctx["flags"]["recent_fall_bool"] = "unknown"
        ctx["flags"]["recent_fall_window"] = None

    # Fall risk derived
    fall_risk = False
    if ctx["flags"].get("recent_fall_bool") is True:
        fall_risk = True
    if flags.get("mobility") in ["Regularly uses a walker","Uses a wheelchair"]:
        fall_risk = True
    if ctx["flags"].get("home_setup_safety_value") in ["minor_improvements","unsafe"]:
        fall_risk = True
    derived["fall_risk"] = "high" if fall_risk else "low"

    # Placement resistance derived
    mw = flags.get("move_willingness")
    if mw == "Strong preference to stay home":
        derived["placement_resistance"] = "high"
        ctx["flags"]["move_willingness_value"] = "resistant"
    elif mw == "Prefer home, open if strongly advised":
        derived["placement_resistance"] = "medium"
        ctx["flags"]["move_willingness_value"] = "reluctant_flexible"
    elif mw == "Open to either home or a move":
        derived["placement_resistance"] = "low"
        ctx["flags"]["move_willingness_value"] = "neutral"
    elif mw == "Comfortable with moving if it’s the better fit":
        derived["placement_resistance"] = "low"
        ctx["flags"]["move_willingness_value"] = "willing"

def _render_recommendation():
    _display_guided_header()
    st.subheader("Recommendation")
    ctx = st.session_state.care_context
    flags = ctx.get("flags", {})
    derived = ctx.get("derived", {})
    name, _ = _name_or_default()

    chronic = set(ctx.get("chronic_conditions", []))
    cognition = flags.get("cognition_level")
    funding = flags.get("funding_confidence")
    willingness = flags.get("move_willingness_value")
    home_safety_val = flags.get("home_setup_safety_value")
    fall_risk = derived.get("fall_risk", "low")

    # Simple decision sketch (placeholder for your engine call)
    recommendation = None
    reasons = []

    # Memory Care trigger
    if "Dementia" in chronic or cognition == "Serious confusion":
        recommendation = "Memory Care"
        reasons.append("Memory changes require 24/7 support")

        # Messaging variants
        if flags.get("move_willingness_value") in ["resistant","reluctant_flexible"]:
            reasons.append("Home is possible only with reliable 24/7 support and safety upgrades")
        if funding == "Very confident — I can afford any care I need" and willingness in ["resistant","reluctant_flexible"]:
            reasons.append("Resources make full-time in-home care feasible, but coverage must be round-the-clock")
        if home_safety_val in ["minor_improvements","unsafe"] or fall_risk == "high":
            reasons.append("Current home risks suggest a supervised setting is safer")
    else:
        # Non-memory-care placeholder logic
        if fall_risk == "high" or home_safety_val in ["minor_improvements","unsafe"]:
            recommendation = "Assisted Living (consider)"
            reasons.append("Safety and mobility needs suggest regular supervision")
        else:
            recommendation = "In-Home Care (with supports)"
            reasons.append("Current risks appear manageable at home with supports")

    st.write(f"**Recommended:** {recommendation}")
    if reasons:
        st.write("**Why:**")
        for r in reasons[:3]:
            st.write(f"- {r}")

    # QA preview
    if st.session_state.qa_mode:
        st.markdown("**Engine preview (flags & derived):**")
        st.json({"flags": flags, "chronic_conditions": list(chronic), "derived": derived})

    if st.button("Start over"):
        st.session_state.planner_step = 0
        st.rerun()

def run_flow():
    care_context = st.session_state.care_context
    step = st.session_state.planner_step

    # Step 0: Audiencing
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
        return

    # Steps 1..12
    if 1 <= step <= len(QUESTIONS):
        st.markdown("### Guided Care Plan")
        name, name_possessive = _name_or_default()
        key, prompt_tmpl, options = QUESTIONS[step-1]
        prompt = prompt_tmpl.format(name=name, name_possessive=name_possessive)
        st.subheader(f"Step {step}: {prompt}")

        if key == "chronic_conditions":
            # Multiselect with stable key and no default; sync after widget
            _ = st.multiselect("Select all that apply", QUESTIONS[8][2], key="chronic_conditions")
            care_context["chronic_conditions"] = list(st.session_state.get("chronic_conditions", []))
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
            # don't block on chronic conditions; others require a selection
            next_disabled = False if key == "chronic_conditions" else care_context["flags"].get(key) is None
            if st.button("Next", disabled=next_disabled):
                st.session_state.planner_step = step + 1
                st.rerun()
        return

    # After last answer, derive and show recommendation
    _derive_after_answers()
    _render_recommendation()
