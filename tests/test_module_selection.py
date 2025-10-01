
from core.modules.selection import recommend_modules

def test_recommend_inhome():
    a = {"A": {"recommendation": "in_home"}}
    pre, badges = recommend_modules(a, mode="household", intent="tinker")
    assert "care_inhome" in pre and "benefits" in pre and "home_mods" in pre
    assert badges.get("care_inhome") == "Recommended"

def test_recommend_al():
    a = {"A": {"recommendation": "assisted_living"}}
    pre, badges = recommend_modules(a, mode="split", intent="planner")
    assert "home" in pre and "benefits" in pre and "care_al_mc" in pre
    # planner adds other_costs
    assert "other_costs" in pre
