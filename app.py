import streamlit as st
from guided_care_plan import engine

# ------------------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Senior Care Navigator",
    page_icon="🧭",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

# ------------------------------------------------------------------------------
# Global CSS
# ------------------------------------------------------------------------------
STYLES = """
<style>
:root {
  --brand:#0B5CD8;
  --brand-ink:#ffffff;
  --ink:#0f172a;
  --muted:#475569;
  --chip:#E6EEFF;
  --chip-b:#C7D2FE;
  --chip-ink:#1E3A8A;
  --card:#ffffff;
  --radius:14px;
  --light-brand:#6BA8FF;
}

/* Page wrapper */
.block-container {
  max-width:1360px;
  padding-top:0 !important;
}
header[data-testid="stHeader"] { background:transparent; }
footer { visibility:hidden; }

/* Typography */
p, .stMarkdown { font-size:18px !important; line-height:1.6 !important; }

/* Question chips */
.stRadio > div { gap:12px !important; }
.stRadio label {
  background:var(--chip);
  border:1px solid var(--chip-b);
  border-radius:var(--radius);
  padding:0.75rem 1.25rem !important;
  font-weight:500 !important;
  color:var(--chip-ink) !important;
  flex:1 1 0;
  text-align:center;
}
.stRadio label:hover { background:var(--light-brand); color:var(--brand-ink) !important; }
.stRadio div[role='radiogroup'] { display:flex; flex-wrap:wrap; gap:12px; }

/* Back/Next row: force horizontal */
.scn-nav-inline{
  display:flex !important;
  flex-wrap:nowrap !important;
  gap:12px !important;
  align-items:center !important;
  justify-content:flex-start !important;
  margin:.5rem 0 0.25rem 0 !important;
}
.scn-nav-inline > div.stButton{
  display:flex !important;
  flex:1 1 0 !important;
  min-width:0 !important;
}
.scn-nav-inline > div.stButton > button{
  width:100% !important;
}
@media (max-width:420px){
  .scn-nav-inline{
    flex-wrap:wrap !important;
  }
  .scn-nav-inline > div.stButton{
    flex:1 1 100% !important;
  }
}
</style>
"""
st.markdown(STYLES, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Hero section (Step 0)
# ------------------------------------------------------------------------------
def render_hero():
    st.markdown("# Senior Care Navigator")
    st.write(
        "We make navigating senior care simple. Answer a few quick questions "
        "and we’ll connect you with the best options, backed by expert guidance — "
        "always free for families."
    )

# ------------------------------------------------------------------------------
# App entrypoint
# ------------------------------------------------------------------------------
if st.session_state.get("planner_step", 0) == 0:
    render_hero()

engine.render()
