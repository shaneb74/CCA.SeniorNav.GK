import streamlit as st

# ----- Design tweaks kept minimal here; app.py owns the design system -----

def _nav_row(next_label, next_disabled, next_cb, back_label="Go Back", back_disabled=False, back_cb=None, testid="nav"):
    c1, c2 = st.columns([1,1])
    with c1:
        if st.button(back_label, disabled=back_disabled):
            if back_cb: back_cb()
    with c2:
        if st.button(next_label, disabled=next_disabled, type="primary"):
            if next_cb: next_cb()

def render_audiencing():
    if "audiencing_step" not in st.session_state:
        st.session_state.audiencing_step = 1
    care_context = st.session_state.setdefault("care_context", {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}})

    step = st.session_state.audiencing_step

    # Step 1: Who are you planning for?
    if step == 1:
        st.markdown("<h2>Step 1: Who are you planning for?</h2>", unsafe_allow_html=True)
        audience_options = ["Planning for one person", "Planning for two people", "Planning as a professional"]
        choice = st.radio("", audience_options, key="audience_type_select")
        if choice:
            care_context["audience_type"] = choice
        _nav_row("Next", not choice, lambda: st.session_state.update(audiencing_step=2) or st.rerun(), "Go Back", True, None, "aud_1")

    # Step 2: Relationship (only if not professional)
    elif step == 2:
        st.markdown("<h2>Step 2: What’s your relationship?</h2>", unsafe_allow_html=True)
        if care_context.get("audience_type") == "Planning as a professional":
            _nav_row("Start Planner", False, lambda: st.session_state.update(step="planner", planner_step=1) or st.rerun(),
                     "Go Back", False, lambda: st.session_state.update(audiencing_step=1) or st.rerun(), "aud_2")
        else:
            relation = st.radio("", ["Self", "Spouse/Partner", "Parent/Parent-in-law", "Other"], key="relation_select")
            if relation:
                care_context["relation"] = relation
            _nav_row("Start Planner", not relation, lambda: st.session_state.update(step="planner", planner_step=1) or st.rerun(),
                     "← Back", False, lambda: st.session_state.update(audiencing_step=1) or st.rerun(), "aud_2")

def render_planner():
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 1
    care_context = st.session_state.setdefault("care_context", {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}})
    step = st.session_state.planner_step

    # 1. Funding
    if step == 1:
        st.markdown("<h2>Step 1: How do you feel about your finances?</h2>", unsafe_allow_html=True)
        funding = st.radio("", [
            "Not worried—I can afford any care I need",
            "Somewhat worried—I’d need to budget carefully",
            "Very worried—cost is a big concern for me",
            "I am on Medicaid"
        ], key="funding_confidence_select")
        if funding:
            care_context["care_flags"]["funding_confidence"] = funding
        _nav_row("Next", not funding or funding == "I am on Medicaid",
                 lambda: st.session_state.update(planner_step=2) or st.rerun(),
                 "Go Back", False, lambda: st.session_state.update(step="audiencing", audiencing_step=1) or st.rerun(), "planner_1")

    # 2. Cognition
    elif step == 2:
        st.markdown("<h2>Step 2: How’s your memory and thinking?</h2>", unsafe_allow_html=True)
        cognition = st.radio("", [
            "Sharp—no real issues",
            "Occasional lapses",
            "Noticeable problems (miss meds/appointments)",
            "Serious confusion"
        ], key="cognition_select")
        if cognition:
            care_context["care_flags"]["cognition_level"] = cognition
        _nav_row("Next", not cognition, lambda: st.session_state.update(planner_step=3) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=1) or st.rerun(), "planner_2")

    # 3. Caregiver
    elif step == 3:
        st.markdown("<h2>Step 3: How much help do you have day-to-day?</h2>", unsafe_allow_html=True)
        caregiver = st.radio("", ["Minimal", "Some support", "Heavy/constant"], key="caregiver_load_select")
        if caregiver:
            care_context["care_flags"]["caregiver_load"] = caregiver
        _nav_row("Next", not caregiver, lambda: st.session_state.update(planner_step=4) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=2) or st.rerun(), "planner_3")

    # 4. Meds
    elif step == 4:
        st.markdown("<h2>Step 4: Medications</h2>", unsafe_allow_html=True)
        meds = st.radio("", ["Few/simple", "Several/complex", "Not sure"], key="meds_complexity_select")
        if meds:
            care_context["care_flags"]["meds_complexity"] = meds
        _nav_row("Next", not meds, lambda: st.session_state.update(planner_step=5) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=3) or st.rerun(), "planner_4")

    # 5. Independence
    elif step == 5:
        st.markdown("<h2>Step 5: Daily independence</h2>", unsafe_allow_html=True)
        independence = st.radio("", ["Independent", "Needs some help", "Needs a lot of help"], key="adl_need_select")
        if independence:
            care_context["care_flags"]["adl_need"] = independence
        _nav_row("Next", not independence, lambda: st.session_state.update(planner_step=6) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=4) or st.rerun(), "planner_5")

    # 6. Mobility
    elif step == 6:
        st.markdown("<h2>Step 6: Mobility</h2>", unsafe_allow_html=True)
        mobility = st.radio("", ["Steady", "Some difficulty", "Frequent falls or unsteady"], key="mobility_select")
        if mobility:
            care_context["care_flags"]["mobility"] = mobility
        _nav_row("Next", not mobility, lambda: st.session_state.update(planner_step=7) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=5) or st.rerun(), "planner_6")

    # 7. Your World (safety at home + recent fall)
    elif step == 7:
        st.markdown("<h2>Step 7: Your world</h2>", unsafe_allow_html=True)
        safety = st.radio("How safe do you feel at home?", ["Very safe", "Some concerns", "Often feel at risk"], key="safety_select")
        if safety:
            care_context["care_flags"]["home_safety"] = safety
        st.markdown("<small>Have you had a fall lately?</small>", unsafe_allow_html=True)
        fall_history = st.radio("", ["Yes", "No", "Unsure"], key="fall_history_select")
        if fall_history:
            care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
        _nav_row("Next", not safety or not fall_history, lambda: st.session_state.update(planner_step=8) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=6) or st.rerun(), "planner_7")

    # 8. Home Preference
    elif step == 8:
        st.markdown("<h2>Step 8: Home preference</h2>", unsafe_allow_html=True)
        preference = st.radio("", ["Prefer to stay home", "Open to assisted living if advised", "Memory care if needed"], key="home_pref_select")
        if preference:
            care_context["care_flags"]["home_preference"] = preference
        _nav_row("See Recommendation", not preference, lambda: st.session_state.update(planner_step=9) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=7) or st.rerun(), "planner_8")

    # 9. Recommendation (placeholder UI; your existing logic can compute based on flags)
    elif step == 9:
        st.markdown("<h2>Recommendation</h2>", unsafe_allow_html=True)
        st.write("This screen should use your existing recommendation logic. The flags collected are in `st.session_state.care_context`.")
        st.code(str(st.session_state.care_context), language="python")
        _nav_row("Start Over", False, lambda: st.session_state.update(step="audiencing", audiencing_step=1, planner_step=1) or st.rerun(),
                 "← Back", False, lambda: st.session_state.update(planner_step=8) or st.rerun(), "planner_9")

def render_step(mode: str):
    if mode == "audiencing":
        render_audiencing()
    else:
        render_planner()
