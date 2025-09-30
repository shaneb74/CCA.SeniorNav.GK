from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

@dataclass
class Flags:
    funding_confidence: Optional[str] = None
    cognition_level: Optional[str] = None
    adl_dependency: Optional[str] = None
    meds_complexity: Optional[str] = None
    caregiver_support_level: Optional[str] = None
    mobility: Optional[str] = None
    social_isolation: Optional[str] = None
    geographic_access: Optional[str] = None
    home_setup_safety: Optional[str] = None
    recent_fall: Optional[str] = None
    move_willingness: Optional[str] = None
    adl_bucket: Optional[str] = None
    caregiver_bucket: Optional[str] = None
    move_willingness_value: Optional[str] = None
    home_setup_safety_value: Optional[str] = None
    recent_fall_bool: Optional[bool] = None

@dataclass
class Derived:
    fall_risk: str = "low"
    home_mod_priority: Optional[str] = None
    placement_resistance: Optional[str] = None
    care_level: Optional[str] = None
    notes: List[str] = field(default_factory=list)

@dataclass
class Person:
    name: str = ""
    chronic_conditions: List[str] = field(default_factory=list)
    mobility_devices: List[str] = field(default_factory=list)
    flags: Flags = field(default_factory=Flags)
    derived: Derived = field(default_factory=Derived)

@dataclass
class CostInputs:
    detail_mode: str = "simple"
    user_intent: str = "planner"
    scenarios: Set[str] = field(default_factory=set)
    keep_home: str = "keep"
    region: str = ""
    overrides: Dict = field(default_factory=dict)

@dataclass
class CostOutputs:
    primary_path: Optional[str] = None
    sections: Dict = field(default_factory=dict)
    nudges: List[Dict] = field(default_factory=list)
    decision_log: Dict = field(default_factory=dict)

@dataclass
class AppState:
    schema_version: str = "2025-09-30"
    mode: str = "one_person"
    people: List[Person] = field(default_factory=lambda: [Person()])
    qa_mode: bool = False
    cost_inputs: CostInputs = field(default_factory=CostInputs)
    cost_outputs: CostOutputs = field(default_factory=CostOutputs)
