import streamlit as st
import random

# Lock fonts and styles early
STYLES = """
<style>
:root{
  --brand:#2563eb;        /* accessible indigo */
  --brand-ink:#ffffff;
  --ink:#0f172a;
  --muted:#475569;
  --chip:#eef2ff;
  --chip-b:#dbeafe;
  --chip-ink:#1e3a8a;
  --card:#ffffff;
  --radius:14px;
}

/* Layout: give the main column room and avoid header clipping */
.block-container{
  max-width:1360px;
  padding-top:calc(3.5rem + env(safe-area-inset-top));
}
header[data-testid="stHeader"]{ background:transparent; }
footer{ visibility:hidden; }

/* Type scale */
p,.stMarkdown{ font-size:18px!important; line-height:1.65; color:var(--ink)!important; }
h1{ font-size:44px; margin:0 0 0 .25rem; color:var(--ink); letter-spacing:-.02em; }
h2{ font-size:32px!important; line-height:1.3; margin:.75rem 0 .35rem 0; color:var(--ink); }
h3{ font-size:20px; margin:.5rem 0 .25rem 0; color:var(--ink); }
small,.stCaption{ font-size:15px!important; color:var(--muted); }

/* Card look: style any Streamlit block that contains .card-hook */
.block-container > div:has(.card-hook){
  background:var(--card);
  border:1px solid #eef0f6;
  border-radius:var(--radius);
  padding:20px 22px;
  box-shadow:0 6px 18px rgba(13,23,63,.06);
  margin:4px 0 22px 0;
}

/* Radio prompt + options sizing */
[data-testid="stRadio"] [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] > div,
[data-testid="stWidgetLabel"] p{
  font-size:20px!important; font-weight:600; color:#111827;
  margin:.25rem 0 .35rem 0; display:block;
}
.stRadio > div > label span,
[data-testid="stRadio"] div[role="radiogroup"] > div > label span{
  font-size:20px!important;
}
.stRadio > div > label,
[data-testid="stRadio"] div[role="radiogroup"] > div > label{
  line-height:1.5; margin:4px 0; display:flex; align-items:center;
}

/* Buttons inline, accessible contrast */
.stButton{ display:inline-block; margin-right:12px; }
.stButton > button{
  background:var(--brand)!important; color:var(--brand-ink)!important;
  border:1px solid #cbd5e1!important; border-radius:10px;
  padding:12px 18px; font-size:18px;
}
.stButton > button:hover{ filter:brightness(.95); }
.stButton > button:disabled{ opacity:.55; }

/* Progress chips (sidebar) */
.progress-bar{ display:flex; gap:6px; flex-wrap:wrap; }
.progress-chip{
  font-size:13px; padding:6px 10px; border-radius:999px;
  background:var(--chip); color:var(--chip-ink); border:1px solid var(--chip-b);
}
.progress-chip.active{ background:var(--brand); color:#fff; border-color:var(--brand); }
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# Session state setup
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "audience_type": None,
        "people": [],
        "care_flags": {},
        "derived_flags": {},
    }

care_context = st.session_state.care_context

def _nav_row(next_label, next_disabled, next_action, back_label, back_disabled, back_action, key_prefix):
    """Render Next/Back horizontally aligned using columns with unique keys."""
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button(back_label, disabled=back_disabled, key=f"{key_prefix}_back"):
            back_action()
    with c2:
        if st.button(next_label, disabled=next_disabled, key=f"{key_prefix}_next"):
            next_action()

def render_audiencing():
    with st.container():
        st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)
        st.markdown("<h2>Step 1: Who are you planning for?</h2>", unsafe_allow_html=True)
        audience_options = {
            "1": "Planning for one person",
            "2": "Planning for two people",
            "3": "Planning as a professional"
        }
        audience_options_list = list(audience_options.values())
        audience_type = st.radio("", audience_options_list, key="audience_type_select")
        if audience_type:
            care_context["audience_type"] = audience_type
            care_context["professional_role"] = None
            care_context["relation"] = None
            if audience_type == "Planning as a professional":
                professional_sub_options = {
                    "1": "Discharge planner",
                    "2": "Making a referral"
                }
                professional_sub_options_list = list(professional_sub_options.values())
                sub_type = st.radio("", professional_sub_options_list, key="professional_sub_type")
                if sub_type:
                    care_context["professional_role"] = sub_type
            st.session_state.care_context = care_context
            st.write(f"Planning for: {care_context.get('audience_type', 'not specified yet')} as {care_context.get('professional_role', 'self')}")
        _nav_row("Next", not audience_type, lambda: st.session_state.update(audiencing_step=2) or st.rerun(), "Go Back", True, lambda: None, "audiencing_1")

    if st.session_state.audiencing_step == 2:
        with st.container():
            st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)
            st.markdown("<h2>Step 2: Tell us who's getting this care</h2>", unsafe_allow_html=True)
            if care_context["audience_type"] == "Planning for one person":
                name = st.text_input("", key="person_name")
                relation_options = {
                    "1": "Myself",
                    "2": "Parent",
                    "3": "Spouse",
                    "4": "Other family member",
                    "5": "Friend"
                }
                relation_options_list = list(relation_options.values())
                relation = st.radio("", relation_options_list, key="relation_select")
                if name and relation:
                    care_context["people"] = [name]
                    care_context["relation"] = relation
                    st.session_state.care_context = care_context
                    st.write(f"Okay—we’re building this for {name}, who is your {relation.lower()}.")
            elif care_context["audience_type"] == "Planning for two people":
                name1 = st.text_input("", key="person_name1")
                relation1_options = {
                    "1": "Myself",
                    "2": "Parent",
                    "3": "Spouse",
                    "4": "Other family member",
                    "5": "Friend"
                }
                relation1_options_list = list(relation1_options.values())
                relation1 = st.radio("", relation1_options_list, key="relation1_select")
                name2 = st.text_input("", key="person_name2")
                relation2_options = {
                    "1": "Parent",
                    "2": "Spouse",
                    "3": "Other family member",
                    "4": "Friend"
                }
                relation2_options_list = list(relation2_options.values())
                relation2 = st.radio("", relation2_options_list, key="relation2_select")
                if name1 and name2 and relation1 and relation2:
                    care_context["people"] = [name1, name2]
                    care_context["relation"] = f"{relation1.lower()} and {relation2.lower()}"
                    st.session_state.care_context = care_context
                    st.write(f"Okay—we’re building this for {name1} and {name2}, who are your {care_context['relation']}.")
            elif care_context["audience_type"] == "Planning as a professional":
                client_name = st.text_input("", key="client_name")
                if client_name:
                    care_context["people"] = [client_name]
                else:
                    care_context["people"] = ["Client"]
                st.session_state.care_context = care_context
                st.write(f"Okay—we’re building this for {', '.join(care_context['people'])} as {care_context.get('professional_role')}.")
            _nav_row("Proceed to Guided Care Plan", not (care_context.get("audience_type") and care_context.get("people") and care_context.get("relation")), 
                     lambda: st.session_state.update(step="planner", audiencing_step=1) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(audiencing_step=1) or st.rerun(), "audiencing_2")

def render_planner():
    with st.container():
        st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)
        if "planner_step" not in st.session_state:
            st.session_state.planner_step = 1

        # Step 1: Funding
        if st.session_state.planner_step == 1:
            st.markdown("<h2>Step 1: How do you feel about your finances?</h2>", unsafe_allow_html=True)
            st.write("Let’s start with something personal.")
            funding_options = {
                "1": "Not worried—I can afford any care I need",
                "2": "Somewhat worried—I’d need to budget carefully",
                "3": "Very worried—cost is a big concern for me",
                "4": "I am on Medicaid"
            }
            funding_options_list = list(funding_options.values())
            funding_confidence = st.radio("", funding_options_list, key="funding_confidence_select")
            if funding_confidence == "I am on Medicaid":
                st.write("That’s great—we can help you find Medicaid-friendly options. Interested?")
                if st.button("Yes, Show Me", key="medicaid_options"):
                    st.session_state.step = "tools"
                    st.rerun()
            elif funding_confidence:
                care_context["care_flags"]["funding_confidence"] = funding_confidence
                st.session_state.care_context = care_context
                st.write(f"I hear you—it sounds like you feel {care_context['care_flags']['funding_confidence'].lower()}. That’s a good starting point.")
            _nav_row("Next", not funding_confidence or funding_confidence == "I am on Medicaid", 
                     lambda: st.session_state.update(planner_step=2) or st.rerun(), 
                     "Go Back", True, lambda: None, "planner_1")

        # Step 2: Cognition
        elif st.session_state.planner_step == 2:
            st.markdown("<h2>Step 2: How’s your memory and thinking been lately?</h2>", unsafe_allow_html=True)
            st.write("Now, let’s talk about your memory and focus.")
            cognition_options = {
                "1": "My memory feels sharp—no real issues",
                "2": "Occasional lapses—like forgetting what I was saying",
                "3": "Noticeable problems—like missing meds or appointments",
                "4": "Serious confusion—like losing track of time, place, or familiar faces"
            }
            cognition_options_list = list(cognition_options.values())
            cognition = st.radio("", cognition_options_list, key="cognition_select")
            if cognition:
                care_context["care_flags"]["cognitive_function"] = cognition
                st.session_state.care_context = care_context
                if "lapses" in cognition.lower() or "problems" in cognition.lower() or "confusion" in cognition.lower():
                    st.write(f"Thanks for sharing that. When those {cognition.split('—')[0].lower()} happen, is there someone around to help?")
                else:
                    st.write(f"That’s reassuring to hear. You’re doing great with {cognition.lower()}.")
            _nav_row("Next", not cognition, lambda: st.session_state.update(planner_step=3) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(planner_step=1) or st.rerun(), "planner_2")

        # Step 3: Caregiver Support
        elif st.session_state.planner_step == 3:
            st.markdown("<h2>Step 3: Who helps you with daily needs?</h2>", unsafe_allow_html=True)
            st.write("It’s good to know who’s there for you.")
            cog = care_context["care_flags"].get("cognitive_function", "")
            funding = care_context["care_flags"].get("funding_confidence", "")
            if "lapses" in cog.lower() or "problems" in cog.lower() or "confusion" in cog.lower():
                if "Not worried—I can afford any care I need" in funding:
                    st.write(f"With your financial security and {cog.lower()}, would having 24/7 caregivers at home be an option?")
                else:
                    st.write(f"Since you mentioned {cog.lower()}, who steps in when memory gets tricky?")
            else:
                st.write("How often does someone help with daily needs?")
            caregiver_options = {
                "1": "Someone’s with me all the time",
                "2": "Support most days",
                "3": "Someone checks in occasionally",
                "4": "No regular support"
            }
            caregiver_options_list = list(caregiver_options.values())
            caregiver = st.radio("", caregiver_options_list, key="caregiver_select")
            if caregiver:
                care_context["care_flags"]["caregiver_support"] = caregiver
                st.session_state.care_context = care_context
                if "No regular support" in caregiver:
                    st.write("That can feel isolating. Would you like help finding someone to check in?")
                else:
                    st.write(f"That sounds comforting—{caregiver.lower()} is a solid support.")
            _nav_row("Next", not caregiver, lambda: st.session_state.update(planner_step=4) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(planner_step=2) or st.rerun(), "planner_3")

        # Step 4: Medication Management
        elif st.session_state.planner_step == 4:
            st.markdown("<h2>Step 4: How do you manage your medications?</h2>", unsafe_allow_html=True)
            st.write("Let’s talk about your daily meds.")
            takes_meds = st.radio("", ["No", "Yes"], index=0, key="takes_meds_select")
            if takes_meds == "Yes":
                cog = care_context["care_flags"].get("cognitive_function", "")
                if "lapses" in cog.lower() or "problems" in cog.lower() or "confusion" in cog.lower():
                    st.write(f"With {cog.lower()}, how do you feel about keeping up with your meds?")
                else:
                    st.write("You’re on meds—how confident are you managing them?")
                med_options = {
                    "1": "I manage them rock-solid",
                    "2": "I’m pretty sure, with reminders",
                    "3": "I need help sometimes",
                    "4": "I can’t count on myself"
                }
                med_options_list = list(med_options.values())
                med_confidence = st.radio("", med_options_list, key="med_confidence_select")
                if med_confidence:
                    care_context["care_flags"]["med_adherence"] = med_confidence
                    st.session_state.care_context = care_context
                    if "need help" in med_confidence.lower() or "can’t count" in med_confidence.lower():
                        st.write("That’s okay—we can find ways to make it easier. Want to explore options?")
                    else:
                        st.write(f"Good to know—you’re handling {med_confidence.lower()} well.")
            _nav_row("Next", takes_meds != "No" and not med_confidence, lambda: st.session_state.update(planner_step=5) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(planner_step=3) or st.rerun(), "planner_4")

        # Step 5: Daily Independence
        elif st.session_state.planner_step == 5:
            st.markdown("<h2>Step 5: How much support do you need daily?</h2>", unsafe_allow_html=True)
            st.write("Let’s talk about your day-to-day routine.")
            independence_options = {
                "1": "I’m fully independent and handle all tasks on my own",
                "2": "I occasionally need reminders or light assistance",
                "3": "I need help with some of these tasks regularly",
                "4": "I rely on someone else for most daily tasks"
            }
            independence_options_list = list(independence_options.values())
            independence = st.radio("", independence_options_list, key="independence_select")
            if independence:
                care_context["care_flags"]["independence_level"] = independence
                st.session_state.care_context = care_context
                if "need help" in independence.lower() or "rely" in independence.lower():
                    st.write("That’s normal—want to talk about what help looks like for you?")
                else:
                    st.write(f"Nice—you’re doing great with {independence.lower()}.")
            _nav_row("Next", not independence, lambda: st.session_state.update(planner_step=6) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(planner_step=4) or st.rerun(), "planner_5")

        # Step 6: Mobility
        elif st.session_state.planner_step == 6:
            st.markdown("<h2>Step 6: How’s your mobility these days?</h2>", unsafe_allow_html=True)
            st.write("How’s getting around been for you lately?")
            mobility_options = {
                "1": "I walk easily without any support",
                "2": "I use a cane or walker for longer distances",
                "3": "I need assistance for most movement around the home",
                "4": "I am mostly immobile or need a wheelchair"
            }
            mobility_options_list = list(mobility_options.values())
            mobility = st.radio("", mobility_options_list, key="mobility_select")
            if mobility:
                care_context["care_flags"]["mobility_issue"] = mobility != mobility_options_list[0]
                if mobility != mobility_options_list[0]:
                    care_context["derived_flags"]["inferred_mobility_aid"] = mobility
                st.session_state.care_context = care_context
                if "assistance" in mobility.lower() or "immobile" in mobility.lower():
                    st.write("That can be a challenge. Is there anything making it harder at home?")
                else:
                    st.write(f"Great—you’re moving well with {mobility.lower()}.")
            _nav_row("Next", not mobility, lambda: st.session_state.update(planner_step=7) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(planner_step=5) or st.rerun(), "planner_6")

        # Step 7: Your World
        elif st.session_state.planner_step == 7:
            with st.container():
                st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)
                if "world_step" not in st.session_state:
                    st.session_state.world_step = 1
                container = st.empty()

                if st.session_state.world_step == 1:
                    with container.container():
                        st.markdown("<h2>Step 7: How connected are you at home?</h2>", unsafe_allow_html=True)
                        social = st.radio("", ["Daily visits or calls", "Weekly check-ins", "Monthly calls", "Mostly alone"], key="social_select")
                        if social:
                            care_context["care_flags"]["social_connection"] = social
                            st.session_state.care_context = care_context
                            if "mostly alone" in social.lower():
                                st.write("That can feel isolating. Do family or neighbors check in at all?")
                            else:
                                st.write(f"That’s nice—{social.lower()} keeps things connected.")
                            if st.button("→", key="next_world_1"):
                                st.session_state.world_step = 2
                                st.rerun()

                elif st.session_state.world_step == 2:
                    with container.container():
                        st.markdown("<h2>Step 7: How easy is it to get out?</h2>", unsafe_allow_html=True)
                        geography = st.radio("", ["Easy—I can walk or drive", "Needs a ride, but manageable", "Pretty hard without help", "Impossible alone"], key="geography_select")
                        if geography:
                            care_context["care_flags"]["geographic_access"] = geography
                            st.session_state.care_context = care_context
                            if "hard" in geography.lower() or "impossible" in geography.lower():
                                st.write("That sounds tough. Is transportation the main hurdle?")
                            else:
                                st.write(f"Good to know—{geography.lower()} works for you.")
                            if st.button("→", key="next_world_2"):
                                st.session_state.world_step = 3
                                st.rerun()

                elif st.session_state.world_step == 3:
                    with container.container():
                        st.markdown("<h2>Step 7: How safe do you feel at home?</h2>", unsafe_allow_html=True)
                        safety = st.radio("", ["Very safe—I have everything I need", "Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"], key="safety_select")
                        if safety:
                            care_context["care_flags"]["falls_risk"] = safety in ["Mostly safe, but a few concerns", "Sometimes I feel unsafe", "Often feel at risk"]
                            st.session_state.care_context = care_context
                            if "unsafe" in safety.lower() or "concerns" in safety.lower():
                                st.write("That’s worth a closer look. Anything specific, like stairs or lighting?")
                            else:
                                st.write(f"Glad to hear—{safety.lower()} sounds reassuring.")
                            if st.button("→", key="next_world_3"):
                                st.session_state.world_step = 4
                                st.rerun()

                elif st.session_state.world_step == 4:
                    with container.container():
                        st.markdown("<h2>Step 7: Have you had any falls lately?</h2>", unsafe_allow_html=True)
                        fall_history = st.radio("", ["Yes", "No", "Unsure"], key="fall_history_select")
                        if fall_history:
                            care_context["derived_flags"]["recent_fall"] = fall_history == "Yes"
                            st.session_state.care_context = care_context
                            if fall_history == "Yes":
                                st.write("Thanks for letting me know. Was it a one-time thing or something recurring?")
                            else:
                                st.write(f"Good—{fall_history.lower()} is a positive sign.")
                            if st.button("→", key="next_world_4"):
                                st.session_state.world_step = 5
                                st.rerun()

                elif st.session_state.world_step == 5:
                    with container.container():
                        st.markdown("<h2>Step 7: Any ongoing health issues?</h2>", unsafe_allow_html=True)
                        condition_options = ["Diabetes", "Hypertension", "Dementia", "Parkinson's", "COPD", "CHF", "Arthritis", "Stroke"]
                        conditions = st.multiselect("", condition_options, key="chronic_conditions_select")
                        if conditions:
                            care_context["care_flags"]["chronic_conditions"] = conditions
                            st.session_state.care_context = care_context
                            if len(conditions) > 1:
                                st.write(f"Got it—you’re managing {', '.join(conditions[:-1]) + ' and ' + conditions[-1]}. That’s a lot—any giving you trouble?")
                            else:
                                st.write(f"Noted—{', '.join(conditions)} is on our radar. How’s that been for you?")
                        _nav_row("Next", not conditions, lambda: st.session_state.update(planner_step=8) or st.rerun(), 
                                 "Go Back", False, lambda: st.session_state.update(world_step=4) or st.rerun(), "world_5")

        # Step 8: Home Preference
        elif st.session_state.planner_step == 8:
            st.markdown("<h2>Step 8: How much does staying home matter to you?</h2>", unsafe_allow_html=True)
            st.write("Lastly, how do you feel about staying in your current home?")
            goal_options = {
                "1": "Not important—I’m open to other options",
                "2": "Somewhat important—I’d prefer to stay but could move",
                "3": "Very important—I strongly want to stay home"
            }
            goal_options_list = list(goal_options.values())
            goal = st.radio("", goal_options_list, key="goal_select")
            if goal:
                care_context["care_flags"]["living_goal"] = goal
                st.session_state.care_context = care_context
                if "important" in goal.lower():
                    st.write("I get it—home’s special. What makes it so important to you?")
                else:
                    st.write(f"That’s flexible—{goal.lower()} gives us room to explore.")
            _nav_row("Get Recommendation", not goal, lambda: st.session_state.update(planner_step=9) or st.rerun(), 
                     "Go Back", False, lambda: st.session_state.update(planner_step=7) or st.rerun(), "planner_8")

        # Step 9: Recommendation
        elif st.session_state.planner_step == 9:
            st.markdown("<h2>Step 9: What’s our recommendation?</h2>", unsafe_allow_html=True)
            st.write("Based on your answers, here’s our suggestion.")
            flags = []
            # Financial
            funding = care_context["care_flags"].get("funding_confidence", "")
            if funding in ["Very worried—cost is a big concern for me", "Somewhat worried—I’d need to budget carefully"]:
                flags.append("needs_financial_assistance")
            elif funding == "Not worried—I can afford any care I need":
                flags.append("can_afford_care")

            # Cognition
            cog = care_context["care_flags"].get("cognitive_function", "")
            conditions = care_context["care_flags"].get("chronic_conditions", [])
            if "Serious confusion" in cog or "Dementia" in conditions or "Parkinson's" in conditions:
                flags.append("severe_cognitive_risk")
            elif "Noticeable problems" in cog:
                flags.append("moderate_cognitive_decline")
            elif "Occasional lapses" in cog:
                flags.append("mild_cognitive_decline")

            # Caregiver Support
            support = care_context["care_flags"].get("caregiver_support", "")
            if "No regular support" in support:
                flags.append("no_support")
            elif "Someone checks in occasionally" in support:
                flags.append("limited_support")
            elif "Support most days" in support or "Someone’s with me all the time" in support:
                flags.append("adequate_support")

            # Medication Adherence
            med_adherence = care_context["care_flags"].get("med_adherence", "No")
            if med_adherence in ["I need help sometimes", "I can’t count on myself"]:
                flags.append("med_adherence_risk")

            # Independence
            indep = care_context["care_flags"].get("independence_level", "")
            if "I rely on someone else for most daily tasks" in indep:
                flags.append("high_dependence")
            elif "I need help with some of these tasks regularly" in indep:
                flags.append("moderate_dependence")

            # Mobility
            mobility = care_context["derived_flags"].get("inferred_mobility_aid", "")
            if "I need assistance for most movement around the home" in mobility or "I am mostly immobile or need a wheelchair" in mobility:
                flags.append("high_mobility_dependence")
            elif "I use a cane or walker for longer distances" in mobility:
                flags.append("moderate_mobility")

            # Social Connection
            social = care_context["care_flags"].get("social_connection", "")
            if "Mostly alone" in social:
                flags.append("high_risk")
            elif "Monthly calls" in social:
                flags.append("moderate_risk")

            # Geography & Access
            geo = care_context["care_flags"].get("geographic_access", "")
            if "Pretty hard without help" in geo or "Impossible alone" in geo:
                flags.append("very_low_access")

            # Home Safety
            safety = care_context["care_flags"].get("falls_risk", False)
            if safety:
                flags.append("moderate_safety_concern")

            # Fall History
            if care_context["derived_flags"].get("recent_fall", False):
                flags.append("high_safety_concern")

            # Chronic Conditions
            conditions = care_context["care_flags"].get("chronic_conditions", [])
            if "CHF" in conditions or "COPD" in conditions:
                if "high_mobility_dependence" in flags or "high_safety_concern" in flags:
                    flags.append("chronic_health_risk")

            # Score Calculation
            score = 0
            if "severe_cognitive_risk" in flags and "adequate_support" in flags:
                score += 10
            elif "severe_cognitive_risk" in flags:
                score += 15
            if "moderate_cognitive_decline" in flags:
                score += 5
            if "mild_cognitive_decline" in flags:
                score += 3
            if "high_dependence" in flags or "high_mobility_dependence" in flags:
                score += 10
            if "moderate_dependence" in flags or "moderate_mobility" in flags:
                score += 5
            if "no_support" in flags:
                score += 7
            if "limited_support" in flags:
                pass  # No penalty for borderline support
            if "adequate_support" in flags:
                score -= 5
            if "high_risk" in flags:
                score += 6
            if "moderate_risk" in flags:
                score += 3
            if "med_adherence_risk" in flags:
                score += 6
            if "very_low_access" in flags:
                score += 4
            if "moderate_safety_concern" in flags:
                score += 5
            if "high_safety_concern" in flags:
                score += 8
            if "chronic_health_risk" in flags:
                score += 7

            # Recommendation Logic
            if ("severe_cognitive_risk" in flags and "no_support" in flags) or score >= 25:
                recommendation = "Memory Care"
                issues = [f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns', 'dealing with severe memory issues']) if 'severe_cognitive_risk' in flags else ''}",
                          f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else ''}",
                          f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else ''}"]
                issues = [i for i in issues if i]
                st.write("**Care Recommendation: Memory Care**")
                message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, with {', '.join(issues[:-1]) + (' and ' if len(issues) > 1 else '') + issues[-1] if issues else 'significant challenges'}, Memory Care is the safest choice. If you have 24/7 skilled care at home, aging in place could work—let’s explore that."
            elif score >= 15:
                recommendation = "Assisted Living"
                issues = [f"{random.choice(['needing daily help with tasks', 'relying on assistance for daily activities']) if 'high_dependence' in flags else random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                          f"{random.choice(['needing a lot of help to get around', 'relying on assistance for mobility']) if 'high_mobility_dependence' in flags else random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                          f"{random.choice(['having no one around to help', 'lacking regular support']) if 'no_support' in flags else random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                          f"{random.choice(['facing serious memory challenges', 'having significant cognitive concerns']) if 'severe_cognitive_risk' in flags else random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                          f"{random.choice(['facing safety risks at home', 'having major safety concerns']) if 'high_safety_concern' in flags else random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
                issues = [i for i in issues if i][:3]  # Top 3 issues
                st.write("**Care Recommendation: Assisted Living**")
                preference = {
                    "Very important—I strongly want to stay home": "Since staying home is important to you, let’s see how we can make that work with extra support.",
                    "Somewhat important—I’d prefer to stay but could move": "You’d prefer to stay home, so let’s explore ways to make that possible.",
                    "Not important—I’m open to other options": "You’re open to options, so let’s look at assisted living communities that feel like home."
                }.get(care_context["care_flags"].get("living_goal", ""), "If you’re unsure, let’s talk through the options together.")
                message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, we see you’re navigating challenges like {', '.join(issues[:-1]) + (' and ' if len(issues) > 1 else '') + issues[-1] if issues else 'various needs'}. Assisted Living would offer the support and safety you need. {preference}"
            elif score >= 8:
                recommendation = "In-Home Care with Support"
                issues = [f"{random.choice(['needing some help with tasks', 'requiring occasional assistance']) if 'moderate_dependence' in flags else ''}",
                          f"{random.choice(['needing some mobility help', 'using aids for longer distances']) if 'moderate_mobility' in flags else ''}",
                          f"{random.choice(['having no one around infrequently', 'lacking support occasionally']) if 'limited_support' in flags else ''}",
                          f"{random.choice(['occasional lapses', 'noticeable problems']) if 'moderate_cognitive_decline' in flags else ''}",
                          f"{random.choice(['having some safety concerns', 'feeling somewhat unsafe']) if 'moderate_safety_concern' in flags else ''}"]
                issues = [i for i in issues if i][:3]  # Top 3 issues
                st.write("**Care Recommendation: In-Home Care with Support**")
                preference = {
                    "Very important—I strongly want to stay home": "Since staying home is important to you, let’s see how we can make that work with extra support.",
                    "Somewhat important—I’d prefer to stay but could move": "You’d prefer to stay home, so let’s explore ways to make that possible.",
                    "Not important—I’m open to other options": "You’re open to options, so let’s look at assisted living communities that feel like home."
                }.get(care_context["care_flags"].get("living_goal", ""), "If you’re unsure, let’s talk through the options together.")
                message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, we see you’re navigating challenges like {', '.join(issues[:-1]) + (' and ' if len(issues) > 1 else '') + issues[-1] if issues else 'mild needs'}. In-Home Care with Support would offer the help you need. {preference}"
            else:
                recommendation = "No Care Needed at This Time"
                st.write("**Care Recommendation: No Care Needed at This Time**")
                message = f"{random.choice(['We\'re here for you', 'We understand this is a big step', 'It\'s good you\'re looking into this', 'We\'re glad you\'re taking this step', 'Let\'s find the best fit for you'])} {care_context['people'][0] if care_context['people'] else 'friend'}, it looks like you\'re managing well for now."
            st.write(message)

        if st.button("Restart", key="planner_restart"):
            st.session_state.planner_step = 1
            st.session_state.care_context = {"audience_type": None, "people": [], "care_flags": {}, "derived_flags": {}}
            st.rerun()

def render_step(step):
    if step == "intro":
        with st.container():
            st.markdown("<div class='card-hook'></div>", unsafe_allow_html=True)
            st.title("Senior Navigator")
            st.write("Welcome! Start by exploring your care options.")
            if st.button("Get Started"):
                st.session_state.step = "audiencing"
                st.session_state.audiencing_step = 1
                st.rerun()
    elif step == "audiencing":
        render_audiencing()
    elif step == "planner":
        render_planner()
    else:
        st.error("Unknown step: " + step)
