
import streamlit as st
from typing import List
# session utils: try to use your existing one; fallback to simple dict
try:
    from core.utils.session import get_session, save_session  # type: ignore
except Exception:
    def get_session():
        if "case" not in st.session_state:
            st.session_state["case"] = {}
        return st.session_state["case"]
    def save_session(obj):
        st.session_state["case"] = obj

from core.modules.catalog import CATALOG
from core.modules.selection import recommend_modules

st.set_page_config(page_title="Cost Planner (Guided)", layout="centered")
st.title("Cost Planner (Guided)")

ss = get_session()
assessments = ss.get("assessment_snapshot", {})
intent = ss.get("cost_intent", ss.get("intent", "tinker"))
mode = ss.get("cost_mode", ss.get("mode", "household"))

prechecked, badges = recommend_modules(assessments, mode=mode, intent=intent)
selected = set(ss.get("cost_module_selection", prechecked))

st.caption("We pre-selected modules based on the Care Plan. Add or remove any you want to include.")

# simple tile with built-in components (no custom CSS)
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

cols_per_row = 2
catalog = sorted(CATALOG, key=lambda m: m.order)
for i in range(0, len(catalog), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, mod in enumerate(catalog[i:i+cols_per_row]):
        with cols[j]:
            is_checked = mod.id in selected
            val = tile(mod, is_checked)
            if val: selected.add(mod.id)
            else: selected.discard(mod.id)

st.divider()
left, right = st.columns([1,1])
with left:
    if st.button("Visit All"):
        selected = {m.id for m in catalog if m.selectable}
with right:
    if st.button("Reset to Recommended"):
        selected = set(prechecked)

# persist
ss["cost_module_selection"] = list(selected)
save_session(ss)

info, go = st.columns([1,1])
with info:
    st.info(f"{len(selected)} module(s) selected.")
with go:
    if st.button("Continue"):
        # Try a few common Cost Planner paths; else show a friendly note.
        candidates: List[str] = [
            "pages/02_Cost_Planner.py",
            "app/pages/02_Cost_Planner.py",
            "pages/Cost_Planner.py",
            "app/pages/Cost_Planner.py",
        ]
        switched = False
        for p in candidates:
            try:
                st.switch_page(p)
                switched = True
                break
            except Exception:
                continue
        if not switched:
            st.warning("Could not auto-open your Cost Planner page. "
                       "Use your existing navigation to open the Cost Planner — "
                       "your module selections are saved.")
