import streamlit as st

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def _q_header(title: str):
    st.markdown(f"**{title}**")

def _q_info_below(bullets):
    if not bullets:
        return
    st.markdown('<div class="scn-why-wrap">', unsafe_allow_html=True)
    with st.expander("Why we ask"):
        for i, b in enumerate(bullets, start=1):
            st.markdown(f"{i}. {b}")
    st.markdown('</div>', unsafe_allow_html=True)

def _guided_header():
    st.markdown("### Guided Care Plan")

def _name_or_default():
    ctx = st.session_state.care_context
    n = ctx.get("person_a_name") or "the person you're planning for"
    possessive = n + "'" if n.endswith("s") else n + "'s"
    return n, possessive

# ------------------------------------------------------------------------------
# Questions (stems, options, info)
# ------------------------------------------------------------------------------
QUESTIONS = [
    ("funding_confidence",
     "How would you describe your financial situation when it comes to paying for care?",
     ["Very confident", "Somewhat confident", "Not confident", "On Medicaid"],
     [
         "Very confident means cost won't limit choices.",
         "Somewhat confident means choices are possible with budgeting.",
         "Not confident means cost will strongly shape options.",
         "On Medicaid routes to Medicaid resources."
     ]),

    ("cognition_level",
     "How would you rate your memory and thinking in daily life?",
     ["Sharp", "Sometimes forgetful", "Frequent memory issues", "Serious confusion"],
     ["We'll pair this with medications and safety to gauge supervision needs."]),

    ("adl_dependency",
     "How well can you manage everyday activities like bathing, dressing, or preparing meals on your own?",
     ["Independent", "Occasional reminders", "Help with some tasks", "Rely on help for most tasks"],
     [
         "ADLs (activities of daily living) include bathing, dressing, meals, and chores.",
         "This helps us understand how much daily support is needed."
     ]),

    ("meds_complexity",
     "Do you take medications, and how manageable is the routine?",
     ["None", "A few, easy to manage", "Several, harder to manage", "Not sure"],
     ["This helps us understand missed-med risk when combined with cognition."]),

    ("caregiver_support_level",
     "How much regular support do you have from a caregiver or family member?",
     ["I have support most of the time",
      "I have support a few days a week",
      "I have support occasionally",
      "I don’t have regular support"],
     [
         "This shows whether consistent caregiver help is available.",
         "Strong support can offset higher daily needs."
     ]),

    ("mobility",
     "How do you usually get around?",
     ["I walk easily", "I use a cane", "I use a walker", "I use a wheelchair"],
     ["We mean typical movement at home and outside."]),

    ("social_isolation",
     "How often do you connect with friends, family, or activities?",
     ["Frequent contact", "Occasional contact", "Rarely see others", "Often alone"],
     None),

    ("geographic_access",
     "How accessible are services like pharmacies, grocery stores, and doctors from your home?",
     ["Very easy", "Moderate", "Difficult", "Very difficult"],
     ["This helps plan logistics and support for errands, meds, and visits."]),

    ("chronic_conditions",
     "Do you have any ongoing health conditions? Select all that apply.",
     ["Diabetes","Hypertension","Dementia","Parkinson's","Stroke","CHF","COPD","Arthritis"],
     ["Select all that apply. Dementia strongly influences recommendations."]),

    ("home_setup_safety",
     "How safe and manageable is your home for daily living as you age?",
     ["Well-prepared", "Mostly safe", "Needs modifications", "Not suitable"],
     ["Think stairs, bathrooms, lighting, grab bars, and trip hazards. We'll suggest an in-home safety assessment if needed."]),

    ("recent_fall",
     "Has there been a fall in the last 6 months?",
     ["Yes","No","Not sure"],
     ["Recent falls increase the need for supervision or home changes."]),

    ("move_willingness",
     "If care is recommended, how open are you to changing where care happens?",
     ["I prefer to stay home",
      "I'd rather stay home but open if needed",
      "I'm comfortable either way",
      "I'm comfortable moving"],
     ["This helps us frame recommendations. It doesn't override safety."]),
]

# ------------------------------------------------------------------------------
# Derived flags & minimal recommendation sketch
# ------------------------------------------------------------------------------
def _derive_after_answers():
    ctx = st.session_state.care_context
    flags = ctx.get("flags", {})
    derived = ctx.setdefault("derived", {})

    # Home setup normalization
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

    # Recent fall
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

    # Fall risk
    fall_risk = False
    if ctx["flags"].get("recent_fall_bool") is True:
        fall_risk = True
    if flags.get("mobility") in ["I use a walker", "I use a wheelchair"]:
        fall_risk = True
    if ctx["flags"].get("home_setup_safety_value") in ["minor_improvements", "major_mods", "unsuitable"]:
        fall_risk = True
    derived["fall_risk"] = "high" if fall_risk else "low"

def _render_recommendation():
    _guided_header()
    st.subheader("Recommendation")

    ctx = st.session_state.care_context
    flags = ctx.get("flags", {})
    derived = ctx.get("derived", {})
    name, _ = _name_or_default()

    chronic = set(ctx.get("chronic_conditions", []))
    cognition = flags.get("cognition_level")
    home_safety_val = flags.get("home_setup_safety_value")
    fall_risk = derived.get("fall_risk", "low")

    recommendation = "In-Home Care (with supports)"
    reasons = []

    if "Dementia" in chronic or cognition == "Serious confusion":
        recommendation = "Memory Care"
        reasons.append("Memory changes suggest 24/7 supervision")
    elif fall_risk == "high" or home_safety_val in ["major_mods", "unsuitable"]:
        recommendation = "Assisted Living (consider)"
        reasons.append("Safety and mobility needs indicate regular supervision")

    st.write(f"**Recommended:** {recommendation}")
    if reasons:
        st.write("**Why:**")
        for r in reasons[:3]:
            st.write(f"- {r}")

    if st.session_state.get("qa_mode"):
        st.markdown("**Engine preview (flags & derived):**")
        st.json({"flags": flags, "chronic_conditions": list(chronic), "derived": derived})

    if st.button("Start over", type="secondary"):
        st.session_state.planner_step = 0
        st.session_state.pop("route", None)
        st.rerun()

# ------------------------------------------------------------------------------
# Off-ramps & professional flows (placeholders)
# ------------------------------------------------------------------------------
def _render_medicaid_offramp():
    st.markdown("### Medicaid Workflow")
    st.write("It looks like Medicaid is the best path. We’ll route you to Medicaid resources and support.")
    st.info("Placeholder page: wire up referral links, coverage explainer, and intake later.")
    if st.button("Start over", type="secondary"):
        st.session_state.planner_step = 0
        st.session_state.pop("route", None)
        st.rerun()

def _render_professional_discharge():
    st.markdown("### Professional: Hospital Discharge Planner")
    st.write("Thanks for the referral. This space will collect discharge context and required placement details.")
    st.info("Placeholder page: add facility filters, urgency, and patient disposition later.")
    if st.button("Start over", type="secondary"):
        st.session_state.planner_step = 0
        st.session_state.pop("route", None)
        st.rerun()

def _render_professional_referral():
    st.markdown("### Professional: Referring Provider")
    st.write("Thanks for the referral. This space will collect basic context for our advisor handoff.")
    st.info("Placeholder page: add contact handoff, urgency flag, and HIPAA note later.")
    if st.button("Start over", type="secondary"):
        st.session_state.planner_step = 0
        st.session_state.pop("route", None)
        st.rerun()

# ------------------------------------------------------------------------------
# Main flow
# ------------------------------------------------------------------------------
def render():
    # bootstrap session
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 0
    if "care_context" not in st.session_state:
        st.session_state.care_context = {"flags": {}}

    # If we're in a special route, render that and bounce
    route = st.session_state.get("route")
    if route == "medicaid_offramp":
        _render_medicaid_offramp(); return
    if route == "pro_discharge":
        _render_professional_discharge(); return
    if route == "pro_referral":
        _render_professional_referral(); return

    _run_flow()

def _run_flow():
    care_context = st.session_state.care_context
    step = st.session_state.planner_step

    # Step 0 – Audiencing (+ professional fork)
    if step == 0:
        st.subheader("Who are you planning care for today?")
        audience = st.radio(
            "",
            ["One person", "Two people", "Professional"],
            horizontal=True,
            key="audience_type",
            index=0,
        )

        # Names for individuals
        if audience == "One person":
            care_context["person_a_name"] = st.text_input("What's their name?", value=care_context.get("person_a_name", ""))
            care_context["person_b_name"] = None

        elif audience == "Two people":
            care_context["person_a_name"] = st.text_input("First person's name", value=care_context.get("person_a_name", ""))
            care_context["person_b_name"] = st.text_input("Second person's name", value=care_context.get("person_b_name", ""))

        else:
            # Professional fork: role, then route to placeholder page
            st.markdown("**Which best describes your role today?**")
            pro_choice = st.radio(
                "",
                ["Hospital discharge planner", "Referring professional"],
                horizontal=True,
                index=0,
                key="pro_role",
            )

        # Nav row
        st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.button("Back", type="secondary", disabled=True)
        with c2:
            if st.button("Next", type="primary"):
                if audience == "Professional":
                    st.session_state.route = "pro_discharge" if st.session_state.get("pro_role") == "Hospital discharge planner" else "pro_referral"
                    st.rerun()
                else:
                    st.session_state.planner_step = 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Steps 1..N
    if 1 <= step <= len(QUESTIONS):
        _guided_header()
        key, prompt, options, bullets = QUESTIONS[step - 1]

        _q_header(f"Step {step}: {prompt}")

        # Render control
        if key == "chronic_conditions":
            sel = st.multiselect("Select all that apply", QUESTIONS[8][2], default=care_context.get("chronic_conditions", []), key="cc_multi")
            care_context["chronic_conditions"] = list(sel)
        else:
            sel = st.radio("", options, index=None, key=f"q_{key}")
            if sel is not None:
                care_context["flags"][key] = sel

        # Nav row with Medicaid off-ramp detection
        st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Back", type="secondary"):
                st.session_state.planner_step = max(0, step - 1)
                st.rerun()
        with c2:
            # If Step 1 (funding) is Medicaid, send to off-ramp
            wants_medicaid_offramp = (key == "funding_confidence" and care_context["flags"].get("funding_confidence") == "On Medicaid")
            next_disabled = False if key == "chronic_conditions" else care_context["flags"].get(key) is None
            if st.button("Next", disabled=next_disabled, type="primary"):
                if wants_medicaid_offramp:
                    st.session_state.route = "medicaid_offramp"
                    st.rerun()
                else:
                    st.session_state.planner_step = step + 1
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Why we ask (below nav)
        _q_info_below(bullets)
        return

    # After last answer
    _derive_after_answers()
    _render_recommendation()


# --- Backward-compat public API shim ---
# Some deployments import `render` from guided_care_plan.engine (see app.py).
# Ensure it's present and delegates to run_flow() if not already defined.
try:
    render  # type: ignore  # noqa: F401
except NameError:  # pragma: no cover
    def render():
        return run_flow()
