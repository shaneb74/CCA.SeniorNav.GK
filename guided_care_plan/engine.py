import streamlit as st
from .questions import QUESTIONS

def _ensure_state():
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 0
    if "care_context" not in st.session_state:
        st.session_state.care_context = {"flags": {}, "derived": {}}

def _q_title(title: str):
    st.markdown(f"<div class='q-title'>{title}</div>", unsafe_allow_html=True)

def _info_below(bullets):
    # spacer so the expander never crowds Back/Next
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    if not bullets:
        return
    with st.expander("Why we ask"):
        for i, b in enumerate(bullets, start=1):
            st.markdown(f"{i}. {b}")

def _audience_screen():
    # Header + paragraph share the same centered wrapper, both left-aligned
    st.markdown(
        """
        <div class='intro-wrap'>
          <h2>Welcome to Senior Care Navigator</h2>
          <p>We make navigating senior care simple. Answer a few quick questions and we’ll connect you with the best options, backed by expert guidance — always free for families.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='q-prompt'>Who are you planning care for today?</div>", unsafe_allow_html=True)

    care = st.session_state.care_context
    who = st.radio("", ["One person", "Two people", "Professional"], index=0, key="audience_choice")
    care["audience_type"] = who

    if who == "One person":
        care["person_a_name"] = st.text_input("What's their name?", key="name_a")
        care["person_b_name"] = None
    elif who == "Two people":
        c1, c2 = st.columns(2)
        with c1:
            care["person_a_name"] = st.text_input("First person's name", key="name_a")
        with c2:
            care["person_b_name"] = st.text_input("Second person's name", key="name_b")
    else:
        qty = st.radio("How many people are you helping?", ["One", "Two"], horizontal=True, index=0, key="pro_qty")
        care["person_a_name"] = st.text_input("Person A name", key="name_a")
        care["person_b_name"] = st.text_input("Person B name (optional)", key="name_b") if qty == "Two" else None

    if st.button("Next", type="primary"):
        st.session_state.planner_step = 1
        st.rerun()

def _derive_flags():
    ctx = st.session_state.care_context
    flags = ctx.get("flags", {})
    derived = ctx.setdefault("derived", {})

    safety = flags.get("home_setup_safety")
    if safety == "Well-prepared":
        derived["home_mod_priority"] = "low"
    elif safety == "Mostly safe":
        derived["home_mod_priority"] = "medium"
    elif safety == "Needs modifications":
        derived["home_mod_priority"] = "high"
    elif safety == "Not suitable":
        derived["home_mod_priority"] = "critical"

    acc = st.session_state.care_context.get("flags", {}).get("geographic_access")
    if acc == "Very easy":
        st.session_state.care_context["derived"]["access_bucket"] = "very_easy"
    elif acc == "Fairly easy":
        st.session_state.care_context["derived"]["access_bucket"] = "moderate"
    elif acc == "Somewhat difficult":
        st.session_state.care_context["derived"]["access_bucket"] = "difficult"
    elif acc == "Very difficult":
        st.session_state.care_context["derived"]["access_bucket"] = "severe"

    rf = flags.get("recent_fall")
    if rf == "Yes":
        derived["recent_fall_bool"] = True
    elif rf == "No":
        derived["recent_fall_bool"] = False
    else:
        derived["recent_fall_bool"] = "unknown"

def _recommendation():
    st.subheader("Recommendation (preview)")
    ctx = st.session_state.care_context
    st.json({
        "flags": ctx.get("flags", {}),
        "derived": ctx.get("derived", {}),
        "chronic_conditions": ctx.get("chronic_conditions", []),
    })

def run_flow():
    _ensure_state()
    step = st.session_state.planner_step
    care = st.session_state.care_context

    if step == 0:
        _audience_screen()
        return

    if 1 <= step <= len(QUESTIONS):
        key, prompt, options, bullets = QUESTIONS[step - 1]
        _q_title(f"Step {step}: {prompt}")

        if key == "chronic_conditions":
            selected = st.multiselect("Select all that apply", options, key="chronic_conditions")
            care["chronic_conditions"] = list(selected)
        else:
            sel = st.radio("", options, key=f"q_{key}", index=None)
            if sel is not None:
                care["flags"][key] = sel

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Back", type="secondary"):
                st.session_state.planner_step = max(0, step - 1)
                st.rerun()
        with c2:
            disabled = False if key == "chronic_conditions" else care["flags"].get(key) is None
            if st.button("Next", type="primary", disabled=disabled):
                st.session_state.planner_step = step + 1
                st.rerun()

        _info_below(bullets)
        return

    _derive_flags()
    _recommendation()
