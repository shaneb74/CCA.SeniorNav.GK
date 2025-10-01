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
    from .recommendation import build_display_model  # thin wrapper over v2 engine

    _guided_header()
    st.subheader("Recommendation")

    care_context = st.session_state.care_context
    dm = build_display_model(care_context)

    # Primary line (preserve existing visual hierarchy)
    st.write(f"**Recommended:** {dm.care_type}")

    # Conversational explanation (uses existing typography; no new styles)
    if dm.blurbs:
        st.markdown('<div class="scn-why-wrap">', unsafe_allow_html=True)
        for b in dm.blurbs:
            st.write(b)
        st.markdown('</div>', unsafe_allow_html=True)

    # Top concise reasons (bulleted list, consistent with current UI)
    if dm.top_reasons:
        st.write("**Why we’re pointing this way:**")
        for r in dm.top_reasons:
            st.write(f"- {r}")

    # Lightweight callouts (kept minimal to avoid visual churn)
    callouts = []
    if dm.flags.get("polypharmacy_flag"):
        callouts.append("We noticed medication complexity alongside fall or cognition risks.")
    if dm.flags.get("high_safety_concern"):
        callouts.append("Home safety and mobility indicators suggest supervised settings.")
    if dm.flags.get("limited_support"):
        callouts.append("Support coverage looks limited; structured staff support may help.")
    if callouts:
        for c in callouts[:2]:
            st.info(c)

    # QA block remains as-is (dev mode)
    if st.session_state.get("qa_mode"):
        st.markdown("---")
        st.subheader("QA Data")
        st.json(st.session_state.get("care_context", {}))

