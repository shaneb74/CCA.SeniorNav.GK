import streamlit as st

def show_question_header(title: str, info_bullets: list[str] | None = None):
    cols = st.columns([1, 0.08])
    with cols[0]:
        st.markdown(f"**{title}**")
    if info_bullets:
        with cols[1]:
            try:
                with st.popover("i", use_container_width=False):
                    for i, bullet in enumerate(info_bullets, start=1):
                        st.markdown(f"{i}. {bullet}")
            except Exception:
                with st.expander("More info"):
                    for i, bullet in enumerate(info_bullets, start=1):
                        st.markdown(f"{i}. {bullet}")

QUESTIONS = [
    ("funding_confidence", "How would you describe your financial situation when it comes to paying for care?",
        ["Very confident", "Somewhat confident", "Not confident", "On Medicaid"],
        ["Very confident means cost won't limit choices.",
         "Somewhat confident means choices are possible with budgeting.",
         "Not confident means cost will strongly shape options.",
         "On Medicaid routes to Medicaid resources."]),
    ("cognition_level", "How would you rate your memory and thinking in daily life?",
        ["Sharp", "Sometimes forgetful", "Frequent memory issues", "Serious confusion"],
        ["We'll pair this with medications and safety to gauge supervision needs."]),
    ("adl_need", "How independent are you with daily tasks like bathing, cooking, and chores?",
        ["Independent", "Occasional reminders", "Regular help", "Full-time help"],
        ["ADLs are 'activities of daily living' such as meals, bathing, dressing, and household chores."]),
    ("meds_complexity", "Do you take medications, and how manageable is the routine?",
        ["None", "A few, easy to manage", "Several, harder to manage", "Not sure"],
        ["This helps us understand missed-med risk when combined with cognition."]),
    ("independence_level", "Overall, how much help do you need day-to-day?",
        ["Independent", "Some help", "Significant help", "Full-time help"],
        None),
    ("mobility", "How do you usually get around?",
        ["I walk easily", "I use a cane", "I use a walker", "I use a wheelchair"],
        ["We mean typical movement at home and outside."]),
    ("social_isolation", "How often do you connect with friends, family, or activities?",
        ["Frequent contact", "Occasional contact", "Rarely see others", "Often alone"],
        None),
    ("geographic_access", "How accessible are services like pharmacies, grocery stores, and doctors from your home?",
        ["Very easy", "Somewhat easy", "Difficult"],
        None),
    ("chronic_conditions", "Do you have any ongoing health conditions? Select all that apply.",
        ["Diabetes","Hypertension","Dementia","Parkinson's","Stroke","CHF","COPD","Arthritis"],
        ["Select all that apply. Dementia strongly influences recommendations."]),
    ("home_setup_safety", "How safe and manageable is your home for daily living as you age?",
        ["Well-prepared", "Mostly safe", "Needs modifications", "Not suitable"],
        ["Think stairs, bathrooms, lighting, grab bars, and trip hazards. We'll suggest an in-home safety assessment if needed."]),
    ("recent_fall", "Has there been a fall in the last 6 months?",
        ["Yes","No","Not sure"],
        ["Recent falls increase the need for supervision or home changes."]),
    ("move_willingness", "If care is recommended, how open are you to changing where care happens?",
        ["I prefer to stay home", "I'd rather stay home but open if needed", "I'm comfortable either way", "I'm comfortable moving"],
        ["This helps us frame recommendations. It doesn't override safety."]),
]

def _display_guided_header():
    st.markdown("### Guided Care Plan")

def _name_or_default():
    ctx = st.session_state.care_context
    n = ctx.get("person_a_name") or "the person you're planning for"
    possessive = n + "'" if n.endswith("s") else n + "'s"
    return n, possessive

def _derive_after_answers():
    ctx = st.session_state.care_context
    flags = ctx.get("flags", {})
    derived = ctx.setdefault("derived", {})

    safety = flags.get("home_setup_safety")
    if safety == "Well-prepared":
        derived["prep_checklist_trigger"] = False
        derived["home_mod_priority"] = "low"
        ctx["flags"]["home_setup_safety_value"] = "ready"
    elif safety == "Mostly safe":
        derived["prep_checklist_trigger"] = True
        derived["home_mod_priority"] = "medium"
        ctx["flags"]["home_setup_safety_value"] = "minor_improvements"
    elif safety == "Needs modifications":
        derived["prep_checklist_trigger"] = True
        derived["home_mod_priority"] = "high"
        ctx["flags"]["home_setup_safety_value"] = "major_mods"
    elif safety == "Not suitable":
        derived["prep_checklist_trigger"] = True
        derived["home_mod_priority"] = "critical"
        ctx["flags"]["home_setup_safety_value"] = "unsuitable"

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

    fall_risk = False
    if ctx["flags"].get("recent_fall_bool") is True:
        fall_risk = True
    if flags.get("mobility") in ["I use a walker","I use a wheelchair"]:
        fall_risk = True
    if ctx["flags"].get("home_setup_safety_value") in ["minor_improvements","major_mods","unsuitable"]:
        fall_risk = True
    derived["fall_risk"] = "high" if fall_risk else "low"

    mw = flags.get("move_willingness")
    if mw == "I prefer to stay home":
        derived["placement_resistance"] = "high"
        ctx["flags"]["move_willingness_value"] = "resistant"
    elif mw == "I'd rather stay home but open if needed":
        derived["placement_resistance"] = "medium"
        ctx["flags"]["move_willingness_value"] = "reluctant_flexible"
    elif mw == "I'm comfortable either way":
        derived["placement_resistance"] = "low"
        ctx["flags"]["move_willingness_value"] = "neutral"
    elif mw == "I'm comfortable moving":
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

    recommendation = None
    reasons = []

    if "Dementia" in chronic or cognition == "Serious confusion":
        recommendation = "Memory Care"
        reasons.append("Memory changes require 24/7 support")
        if flags.get("move_willingness_value") in ["resistant","reluctant_flexible"]:
            reasons.append("Home is possible only with reliable 24/7 support and safety upgrades")
        if funding == "Very confident" and willingness in ["resistant","reluctant_flexible"]:
            reasons.append("Resources make full-time in-home care feasible, but coverage must be round-the-clock")
        if home_safety_val in ["minor_improvements","major_mods","unsuitable"] or fall_risk == "high":
            reasons.append("Current home risks suggest a supervised setting is safer")
    else:
        if fall_risk == "high" or home_safety_val in ["minor_improvements","major_mods","unsuitable"]:
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

    if st.session_state.qa_mode:
        st.markdown("**Engine preview (flags & derived):**")
        st.json({"flags": flags, "chronic_conditions": list(chronic), "derived": derived})

    if st.button("Start over", type="secondary"):
        st.session_state.planner_step = 0
        st.rerun()

def run_flow():
    care_context = st.session_state.care_context
    step = st.session_state.planner_step

    if step == 0:
        st.subheader("Planning Context")
        care_context["audience_type"] = st.radio(
            "Who are you planning care for today?",
            ["One person","Two people","Professional"],
            index=0
        )
        if care_context["audience_type"] == "One person":
            care_context["person_a_name"] = st.text_input("What's their name?")
        elif care_context["audience_type"] == "Two people":
            care_context["person_a_name"] = st.text_input("What's the first person's name?")
            care_context["person_b_name"] = st.text_input("What's the second person's name?")
        else:
            who = st.radio("How many people are you helping?", ["One","Two"], horizontal=True, index=0)
            care_context["person_a_name"] = st.text_input("Person A name")
            care_context["person_b_name"] = st.text_input("Person B name (if applicable)") if who == "Two" else None

        if st.button("Next", type="primary"):
            st.session_state.planner_step = 1
            st.rerun()
        return

    if 1 <= step <= len(QUESTIONS):
        _display_guided_header()
        key, prompt, options, bullets = QUESTIONS[step-1]
        show_question_header(f"Step {step}: {prompt}", bullets)

        if key == "chronic_conditions":
            _ = st.multiselect("Select all that apply", QUESTIONS[8][2], key="chronic_conditions")
            care_context["chronic_conditions"] = list(st.session_state.get("chronic_conditions", []))
        else:
            sel = st.radio("", options, index=None, key=f"q_{key}")
            if sel is not None:
                care_context["flags"][key] = sel

        cols = st.columns(2)
        with cols[0]:
            if st.button("Back", type="secondary"):
                st.session_state.planner_step = max(0, step-1)
                st.rerun()
        with cols[1]:
            next_disabled = False if key == "chronic_conditions" else care_context["flags"].get(key) is None
            if st.button("Next", disabled=next_disabled, type="primary"):
                st.session_state.planner_step = step + 1
                st.rerun()
        return

    _derive_after_answers()
    _render_recommendation()
