
from __future__ import annotations
from typing import Dict, Any, List, Tuple
from .catalog import CATALOG

# Public contract:
# recommend_modules(assessments, mode, intent) -> (prechecked_ids, recommended_badges)
#
# - assessments: dict like {"A": {"recommendation": "in_home", "answers": {...}}, "B": {...}}
# - mode: "household" | "split"
# - intent: "tinker" | "planner"

def _any_reco(assessments: Dict[str, Dict[str, Any]], target: str) -> bool:
    return any(s.get("recommendation") in target.split("|") for s in assessments.values())

def recommend_modules(assessments: Dict[str, Dict[str, Any]] | None,
                      mode: str = "household",
                      intent: str = "tinker") -> Tuple[List[str], Dict[str, str]]:
    pre: List[str] = []
    badges: Dict[str, str] = {}

    # Always include core building blocks
    pre.extend(["income", "assets"])

    if assessments:
        ih = _any_reco(assessments, "in_home")
        almc = _any_reco(assessments, "assisted_living|memory_care")

        if ih:
            for mid in ("benefits", "home_mods", "care_inhome"):
                if mid not in pre: pre.append(mid)
                badges[mid] = "Recommended"

        if almc:
            for mid in ("home", "benefits", "care_al_mc"):
                if mid not in pre: pre.append(mid)
                badges[mid] = "Recommended"

    # Planner mode prefers comprehensive; Tinker keeps it light
    if intent == "planner":
        for mid in ("other_costs",):
            if mid not in pre: pre.append(mid)

    # De-dup while preserving order
    seen = set()
    pre = [m for m in pre if not (m in seen or seen.add(m))]
    return pre, badges
