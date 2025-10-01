from dataclasses import dataclass
from typing import Dict, List, Any

# Import the uploaded v2 engine's API
from gcp_recommendation_engine_v2 import recommend_from_answers

@dataclass
class DisplayModel:
    care_type: str
    top_reasons: List[str]
    blurbs: List[str]
    flags: Dict[str, Any]

def _coalesce_answers(care_context: Dict[str, Any]) -> Dict[str, Any]:
    flags = care_context.get("flags", {})
    return {
        "funding_confidence": flags.get("funding_confidence"),
        "cognition_level": flags.get("cognition_level"),
        "adl_dependency": flags.get("adl_dependency"),
        "medication_complexity": flags.get("medication_complexity"),
        "caregiver_support_level": flags.get("caregiver_support_level"),
        "mobility": flags.get("mobility"),
        "social_isolation": flags.get("social_isolation"),
        "geographic_access": flags.get("geographic_access"),
        "home_setup_safety": flags.get("home_setup_safety"),
        "recent_fall": flags.get("recent_fall"),
        "move_willingness": flags.get("move_willingness"),
        "chronic_conditions": care_context.get("chronic_conditions", []),
    }

def build_display_model(care_context: Dict[str, Any]) -> DisplayModel:
    answers = _coalesce_answers(care_context)
    rec = recommend_from_answers(answers)

    care_type = rec.care_type
    top_reasons = list(getattr(rec.trace, "top_reasons", []) or [])[:3]
    blurbs = list(getattr(rec.trace, "blurbs", []) or [])[:3]
    flags = dict(getattr(rec.trace, "flags", {}) or {})

    return DisplayModel(
        care_type=care_type,
        top_reasons=top_reasons,
        blurbs=blurbs,
        flags=flags,
    )
