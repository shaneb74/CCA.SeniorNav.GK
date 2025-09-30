import streamlit as st
from .questions import QUESTIONS

def _q_header(title: str):
    st.markdown(f"<div class='q-title'>{title}</div>", unsafe_allow_html=True)

def _guided_header():
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
    if flags.get("mobility") in ["I use a walker", "I use a wheelchair"]:
        fall_risk = True
    if ctx["flags"].get("home_setup_safety_value") in ["minor_improvements", "major_mods", "unsuitable"]:
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

    adl = flags.get("adl_dependency")
    if adl == "Independent":
        ctx["flags"]["adl_bucket"] = "independent"
    elif adl == "Occasional reminders":
        ctx["flags"]["adl_bucket"] = "occasional_reminders"
    elif adl == "Help with some tasks":
        ctx["flags"]["adl_bucket"] = "partial_support"
    elif adl == "Rely on help for most tasks":
        ctx["flags"]["adl_bucket"] = "dependent"

    cg = flags.get("caregiver_support_level")
    if cg == "I have support most of the time":
        ctx["flags"]["caregiver_bucket"] = "full_support"
    elif cg == "I have support a few days a week":
        ctx["flags"]["caregiver_bucket"] = "part_time_support"
    elif cg == "I have support occasionally":
        ctx["flags"]["caregiver_bucket"] = "occasional_support"
    elif cg == "I don’t have regular support":
        ctx["flags"]["caregiver_bucket"] = "no_support"

def _render_recommendation():
    _guided_header()
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
        if flags.get("move_willingness_value") in ["resistant", "reluctant_flexible"]:
            reasons.append("Home is possible only with reliable 24/7 support and safety upgrades")
        if funding == "Very confident" and willingness in ["resistant", "reluctant_flexible"]:
            reasons.append("Resources make full-time in-home care feasible, but coverage must be round-the-clock")
        if home_safety_val in ["minor_improvements", "major_mods", "unsuitable"] or fall_risk == "high":
            reasons.append("Current home risks suggest a supervised setting is safer")
    else:
        if fall_risk == "high" or home_safety_val in ["minor_improvements", "major_mods", "unsuitable"]:
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
    if "qa_mode" not in st.session_state:
        st.session_state.qa_mode = False
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 0
    if "care_context" not in st.session_state:
        st.session_state.care_context = {
            "audience_type": None,
            "person_a_name": None,
            "person_b_name": None,
            "flags": {},
            "chronic_conditions": [],
            "derived": {}
        }
    if "chronic_conditions" not in st.session_state:
        st.session_state.chronic_conditions = []

    care_context = st.session_state.care_context
    step = st.session_state.planner_step

    # Step 0 – Audiencing
    if step == 0:
        st.subheader("Planning Context")
        # Larger prompt line
        st.markdown("<div class='q-prompt'>Who are you planning care for today?</div>", unsafe_allow_html=True)
        care_context["audience_type"] = st.radio(
            "",  # empty label; we render our own prompt above
            ["One person", "Two people", "Professional"],
            index=0
        )
        if care_context["audience_type"] == "One person":
            care_context["person_a_name"] = st.text_input("What's their name?")
        elif care_context["audience_type"] == "Two people":
            care_context["person_a_name"] = st.text_input("What's the first person's name?")
            care_context["person_b_name"] = st.text_input("What's the second person's name?")
        else:
            who = st.radio("How many people are you helping?", ["One", "Two"], horizontal=True, index=0)
            care_context["person_a_name"] = st.text_input("Person A name")
            care_context["person_b_name"] = st.text_input("Person B name (if applicable)") if who == "Two" else None

        if st.button("Next", type="primary"):
            st.session_state.planner_step = 1
            st.rerun()
        return

    # Steps 1..N
    if 1 <= step <= len(QUESTIONS):
        _guided_header()
        key, prompt, options, bullets = QUESTIONS[step - 1]
        _q_header(f"Step {step}: {prompt}")

        if key == "chronic_conditions":
            _ = st.multiselect("Select all that apply", QUESTIONS[8][2], key="chronic_conditions")
            care_context["chronic_conditions"] = list(st.session_state.get("chronic_conditions", []))
        else:
            sel = st.radio("", options, index=None, key=f"q_{key}")
            if sel is not None:
                care_context["flags"][key] = sel

        # spacing before actions
        st.markdown("<div style='height: 1.25rem'></div>", unsafe_allow_html=True)

        # Centered Back/Next row
        sp1, col_back, col_next, sp2 = st.columns([2, 1, 1, 2])
        with col_back:
            if st.button("Back", type="secondary", use_container_width=True):
                st.session_state.planner_step = max(0, step - 1)
                st.rerun()
        with col_next:
            next_disabled = False if key == "chronic_conditions" else care_context["flags"].get(key) is None
            if st.button("Next", disabled=next_disabled, type="primary", use_container_width=True):
                st.session_state.planner_step = step + 1
                st.rerun()

        # Info popover well below buttons
        if bullets:
            st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
            lower_row = st.container()
            with lower_row:
                l, m, r = st.columns([1, 2, 1])
                with m:
                    with st.popover("Why we ask", use_container_width=True):
                        for i, bullet in enumerate(bullets, start=1):
                            st.markdown(f"{i}. {bullet}")
            st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        return

    # After last answer
    _derive_after_answers()
    _render_recommendation()
