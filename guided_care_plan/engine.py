"""
Guided Care Plan flow (engine)
------------------------------

Responsibilities:
- Orchestrates the multi-step questionnaire (step 0..N)
- Stores answers into st.session_state.care_context
- Computes normalized / derived flags used by later planners
- Renders a light-weight recommendation preview

Notes:
- Step 0's welcome hero is rendered in app.py (on purpose) to keep this module
  concerned only with the assessment flow and data/flags.
- The Back/Next controls are placed inside a custom <div class="scn-nav-inline">
  so CSS can keep them side-by-side on desktop AND mobile (until ~420px).
"""

from __future__ import annotations
import streamlit as st

# =============================================================================
# Utilities & helpers
# =============================================================================

def _ensure_bootstrap() -> None:
    """Initialize session scaffolding if missing."""
    if "planner_step" not in st.session_state:
        st.session_state.planner_step = 0
    if "care_context" not in st.session_state:
        st.session_state.care_context = {
            "flags": {},              # single-choice answers
            "chronic_conditions": [], # multi-select list
            "derived": {},            # computed flags
        }

def _ctx() -> dict:
    """Shorthand accessor."""
    return st.session_state.care_context

def _flags() -> dict:
    return _ctx().setdefault("flags", {})

def _derived() -> dict:
    return _ctx().setdefault("derived", {})

def _q_header(title: str) -> None:
    """Consistent question header (bold, used across steps)."""
    st.markdown(f"**{title}**")

def _q_info_below(bullets: list[str] | None) -> None:
    """
    Compact 'Why we ask' block placed BELOW the nav buttons for ergonomics.
    """
    if not bullets:
        return
    st.markdown('<div class="scn-why-wrap">', unsafe_allow_html=True)
    with st.expander("Why we ask"):
        for i, b in enumerate(bullets, start=1):
            st.markdown(f"{i}. {b}")
    st.markdown('</div>', unsafe_allow_html=True)

def _guided_header() -> None:
    """Section label shown for steps 1..N and recommendations."""
    st.markdown("### Guided Care Plan")

def _name_or_default() -> tuple[str, str]:
    """
    Person A's display name + possessive form. Fallback to generic phrasing.
    """
    ctx = _ctx()
    n = ctx.get("person_a_name") or "the person you're planning for"
    possessive = n + "'" if n.endswith("s") else n + "'s"
    return n, possessive


# =============================================================================
# Questionnaire (stems, options, short info)
# Order defines step numbers (1..len(QUESTIONS)).
# =============================================================================

# NOTE: Copy here reflects the latest accepted wording.
QUESTIONS: list[tuple[str, str, list[str], list[str] | None]] = [
    (
        "funding_confidence",
        "How would you describe your financial situation when it comes to paying for care?",
        ["Very confident", "Somewhat confident", "Not confident", "On Medicaid"],
        [
            "Very confident means cost won't limit choices.",
            "Somewhat confident means choices are possible with budgeting.",
            "Not confident means cost will strongly shape options.",
            "On Medicaid routes to Medicaid resources.",
        ],
    ),
    (
        "cognition_level",
        "How would you rate your memory and thinking in daily life?",
        ["Sharp", "Sometimes forgetful", "Frequent memory issues", "Serious confusion"],
        ["We'll pair this with medications and safety to gauge supervision needs."],
    ),
    (
        "adl_dependency",
        "How well can you manage everyday activities like bathing, dressing, or preparing meals on your own?",
        ["Independent", "Occasional reminders", "Help with some tasks", "Rely on help for most tasks"],
        [
            "ADLs (activities of daily living) include bathing, dressing, meals, and chores.",
            "This helps us understand how much daily support is needed.",
        ],
    ),
    (
        "meds_complexity",
        "Do you take medications, and how manageable is the routine?",
        ["None", "A few, easy to manage", "Several, harder to manage", "Not sure"],
        ["This helps us understand missed-med risk when combined with cognition."],
    ),
    (
        "caregiver_support_level",
        "How much regular support do you have from a caregiver or family member?",
        [
            "I have support most of the time",
            "I have support a few days a week",
            "I have support occasionally",
            "I don’t have regular support",
        ],
        [
            "This shows whether consistent caregiver help is available.",
            "Strong support can offset higher daily needs.",
        ],
    ),
    (
        "mobility",
        "How do you usually get around?",
        ["I walk easily", "I use a cane", "I use a walker", "I use a wheelchair"],
        ["We mean typical movement at home and outside."],
    ),
    (
        "social_isolation",
        "How often do you connect with friends, family, or activities?",
        ["Frequent contact", "Occasional contact", "Rarely see others", "Often alone"],
        None,
    ),
    (
        "geographic_access",
        "How accessible are services like pharmacies, grocery stores, and doctors from your home?",
        ["Very easy", "Moderate", "Difficult", "Very difficult"],
        ["This helps plan logistics and support for errands, meds, and visits."],
    ),
    (
        "chronic_conditions",
        "Do you have any ongoing health conditions? Select all that apply.",
        ["Diabetes", "Hypertension", "Dementia", "Parkinson's", "Stroke", "CHF", "COPD", "Arthritis"],
        ["Select all that apply. Dementia strongly influences recommendations."],
    ),
    (
        "home_setup_safety",
        "How safe and manageable is your home for daily living as you age?",
        ["Well-prepared", "Mostly safe", "Needs modifications", "Not suitable"],
        [
            "Think stairs, bathrooms, lighting, grab bars, and trip hazards. "
            "We'll suggest an in-home safety assessment if needed."
        ],
    ),
    (
        "recent_fall",
        "Has there been a fall in the last 6 months?",
        ["Yes", "No", "Not sure"],
        ["Recent falls increase the need for supervision or home changes."],
    ),
    (
        "move_willingness",
        "If care is recommended, how open are you to changing where care happens?",
        [
            "I prefer to stay home",
            "I'd rather stay home but open if needed",
            "I'm comfortable either way",
            "I'm comfortable moving",
        ],
        ["This helps us frame recommendations. It doesn't override safety."],
    ),
]

# Convenience: indices we reference directly
IDX_CHRONIC = 8  # "chronic_conditions" position in QUESTIONS


# =============================================================================
# Derived flags & normalization
# =============================================================================

def _normalize_home_setup() -> None:
    """
    Map home_setup_safety to both a user-friendly description and a stable
    internal value that downstream logic can reason about.
    Also raises the prep checklist trigger and priority.
    """
    fl = _flags()
    dv = _derived()
    safety = fl.get("home_setup_safety")

    if safety == "Well-prepared":
        dv["prep_checklist_trigger"] = False
        dv["home_mod_priority"] = "low"
        fl["home_setup_safety_value"] = "ready"
    elif safety == "Mostly safe":
        dv["prep_checklist_trigger"] = True
        dv["home_mod_priority"] = "medium"
        fl["home_setup_safety_value"] = "minor_improvements"
    elif safety == "Needs modifications":
        dv["prep_checklist_trigger"] = True
        dv["home_mod_priority"] = "high"
        fl["home_setup_safety_value"] = "major_mods"
    elif safety == "Not suitable":
        dv["prep_checklist_trigger"] = True
        dv["home_mod_priority"] = "critical"
        fl["home_setup_safety_value"] = "unsuitable"
    else:
        # Unanswered / unknown: leave derived values untouched
        pass

def _normalize_recent_fall() -> None:
    """Normalize the recent fall answer into boolean/enum helpers."""
    fl = _flags()
    rf = fl.get("recent_fall")

    if rf == "Yes":
        fl["recent_fall_bool"] = True
        fl["recent_fall_window"] = "0_6mo"
    elif rf == "No":
        fl["recent_fall_bool"] = False
        fl["recent_fall_window"] = None
    elif rf == "Not sure":
        fl["recent_fall_bool"] = "unknown"
        fl["recent_fall_window"] = None

def _compute_fall_risk() -> None:
    """
    Simple fall-risk heuristic combining recent falls, mobility, and home setup.
    """
    fl = _flags()
    dv = _derived()
    risk = False

    if fl.get("recent_fall_bool") is True:
        risk = True
    if fl.get("mobility") in {"I use a walker", "I use a wheelchair"}:
        risk = True
    if fl.get("home_setup_safety_value") in {"minor_improvements", "major_mods", "unsuitable"}:
        risk = True

    dv["fall_risk"] = "high" if risk else "low"

def _derive_after_answers() -> None:
    """
    Called after last question (and also safe to call at the recommendation step).
    """
    _normalize_home_setup()
    _normalize_recent_fall()
    _compute_fall_risk()


# =============================================================================
# Recommendation sketch (preview)
# =============================================================================

def _render_recommendation() -> None:
    """
    Lightweight recommendation preview, intended for immediate feedback and QA.
    Full planner uses these same flags later.
    """
    _guided_header()
    st.subheader("Recommendation")

    fl, dv = _flags(), _derived()
    ctx = _ctx()
    chronic = set(ctx.get("chronic_conditions", []))

    cognition = fl.get("cognition_level")
    home_safety_val = fl.get("home_setup_safety_value")
    fall_risk = dv.get("fall_risk", "low")

    # Default stance is to try to keep someone at home with supports,
    # unless strong indicators point to higher supervision.
    recommendation = "In-Home Care (with supports)"
    reasons: list[str] = []

    if "Dementia" in chronic or cognition == "Serious confusion":
        recommendation = "Memory Care"
        reasons.append("Memory changes suggest 24/7 supervision")
    elif fall_risk == "high" or home_safety_val in {"major_mods", "unsuitable"}:
        recommendation = "Assisted Living (consider)"
        reasons.append("Safety and mobility needs indicate regular supervision")

    st.write(f"**Recommended:** {recommendation}")
    if reasons:
        st.write("**Why:**")
        for r in reasons[:3]:
            st.write(f"- {r}")

    if st.session_state.get("qa_mode"):
        st.markdown("**Engine preview (flags & derived):**")
        st.json({"flags": fl, "chronic_conditions": list(chronic), "derived": dv})

    if st.button("Start over", type="secondary"):
        st.session_state.planner_step = 0
        st.rerun()


# =============================================================================
# Main flow
# =============================================================================

def render() -> None:
    """Public entrypoint from app.py."""
    _ensure_bootstrap()
    _run_flow()

def _render_step0_audiencing() -> None:
    """
    Step 0: audience & names. The welcome hero is rendered in app.py.
    """
    ctx = _ctx()

    st.subheader("Who are you planning care for today?")
    audience = st.radio(
        "",
        ["One person", "Two people", "Professional"],
        horizontal=True,
        key="audience_type",
        index=0,
    )

    # Name capture by mode
    if audience == "One person":
        ctx["person_a_name"] = st.text_input(
            "What's their name?", value=ctx.get("person_a_name", "")
        )
        ctx["person_b_name"] = None

    elif audience == "Two people":
        ctx["person_a_name"] = st.text_input(
            "First person's name", value=ctx.get("person_a_name", "")
        )
        ctx["person_b_name"] = st.text_input(
            "Second person's name", value=ctx.get("person_b_name", "")
        )

    else:  # Professional
        who = st.radio("How many people are you helping?", ["One", "Two"], horizontal=True, index=0, key="prof_count")
        ctx["person_a_name"] = st.text_input(
            "Person A name", value=ctx.get("person_a_name", "")
        )
        ctx["person_b_name"] = (
            st.text_input("Person B name (if applicable)", value=ctx.get("person_b_name", ""))
            if who == "Two" else None
        )

    # Nav row (horizontal via CSS)
    st.markdown('<div class="scn-nav-inline">', unsafe_allow_html=True)
    next_clicked = st.button("Next", type="primary", key="next_0")
    st.markdown('</div>', unsafe_allow_html=True)

    if next_clicked:
        st.session_state.planner_step = 1
        st.rerun()

def _render_step_q(idx: int) -> None:
    """
    Render a single assessment step.
    """
    ctx, fl = _ctx(), _flags()
    key, prompt, options, bullets = QUESTIONS[idx]

    _guided_header()
    _q_header(f"Step {idx + 1}: {prompt}")

    # Multiselect (only the chronic conditions step)
    if key == "chronic_conditions":
        current = ctx.get("chronic_conditions", [])
        sel = st.multiselect(
            "Select all that apply",
            QUESTIONS[IDX_CHRONIC][2],
            default=current,
            key="cc_multi",
        )
        ctx["chronic_conditions"] = list(sel)
    else:
        # Radio with explicit key so Back/Next reruns don't lose state
        sel = st.radio(
            "",
            options,
            index=None,               # require selection to enable Next
            key=f"q_{key}",
        )
        if sel is not None:
            fl[key] = sel

    # Nav row (horizontal via CSS)
    st.markdown('<div class="scn-nav-inline">', unsafe_allow_html=True)
    back_clicked = st.button("Back", type="secondary", key=f"back_{idx+1}")
    next_disabled = False if key == "chronic_conditions" else fl.get(key) is None
    next_clicked = st.button("Next", type="primary", disabled=next_disabled, key=f"next_{idx+1}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle nav
    if back_clicked:
        st.session_state.planner_step = max(0, idx)  # go back one screen
        st.rerun()
    if next_clicked:
        st.session_state.planner_step = idx + 2      # advance to next step
        st.rerun()

    # Info block placed BELOW the nav controls (mobile-friendly)
    _q_info_below(bullets)

def _run_flow() -> None:
    """
    Flow controller:
    - step == 0     -> audience / names
    - 1..N          -> questions
    - end+1         -> normalization + recommendation
    """
    step = st.session_state.planner_step
    total_steps = len(QUESTIONS)

    # Step 0: audience
    if step == 0:
        _render_step0_audiencing()
        return

    # Steps 1..N
    if 1 <= step <= total_steps:
        _render_step_q(step - 1)
        return

    # After last answer
    _derive_after_answers()
    _render_recommendation()
