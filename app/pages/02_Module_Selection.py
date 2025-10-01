
import streamlit as st
from core.utils.session import get_session, save_session
from core.modules.catalog import CATALOG
from core.modules.selection import recommend_modules

st.set_page_config(page_title="Select Cost Modules", layout="centered")
st.title("Choose Your Cost Modules")

ss = get_session()
assessments = ss.get("assessment_snapshot", {})
intent = ss.get("cost_intent", ss.get("intent", "tinker"))
mode = ss.get("cost_mode", ss.get("mode", "household"))

# Compute recommendations
prechecked, badges = recommend_modules(assessments, mode=mode, intent=intent)

# User selections live in session for downstream Cost page
selected = set(ss.get("cost_module_selection", prechecked))

st.caption("Based on your Care Plan, we pre‑selected a few modules. "
           "Add or remove any you want to include in your estimate.")

# Render tiles in a simple, styling‑agnostic grid (no custom CSS).
cols_per_row = 2
catalog = sorted(CATALOG, key=lambda m: m.order)

def tile(module, checked: bool):
    with st.container(border=True):
        top = st.columns([1,5])
        with top[0]:
            st.markdown(module.icon)
        with top[1]:
            st.subheader(module.title)
            st.caption(module.subtitle)
        if module.id in badges:
            st.markdown(f"**{badges[module.id]}**")
        if module.selectable:
            new_val = st.checkbox("Include", value=checked, key=f"ck_{module.id}")
        else:
            st.caption("Auto")
            new_val = checked
    return new_val

# Grid
for i in range(0, len(catalog), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, mod in enumerate(catalog[i:i+cols_per_row]):
        with cols[j]:
            is_checked = mod.id in selected
            val = tile(mod, is_checked)
            if val:
                selected.add(mod.id)
            else:
                selected.discard(mod.id)

# Actions
st.divider()
left, right = st.columns([1,1])
with left:
    if st.button("Visit All"):
        # Include every selectable module
        selected = {m.id for m in catalog if m.selectable}
with right:
    if st.button("Reset to Recommended"):
        selected = set(prechecked)

# Persist and continue
ss["cost_module_selection"] = list(selected)
save_session(ss)

st.write("")  # spacing
go_cols = st.columns([1,1])
with go_cols[0]:
    st.info(f"{len(selected)} module(s) selected.")
with go_cols[1]:
    if st.button("Continue"):
        # Hand off to your existing Cost Planner page
        # We avoid importing it or changing styling; we just navigate.
        st.switch_page("pages/02_Cost_Planner.py")
