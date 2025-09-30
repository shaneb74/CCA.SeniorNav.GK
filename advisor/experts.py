from dataclasses import dataclass

@dataclass
class Expert:
    id: str
    title: str
    fee: str | None
    primary: bool = False
    blurb: str = ""

EXPERTS = [
    Expert("senior_advisor", "Senior Living Advisor", None, True,
           "Included. Guidance on in-home, assisted living, and memory care."),
    Expert("physician", "Physician Second Opinion", "Fee",
           False, "Independent clinical review when decisions are complex."),
    Expert("medicare", "Medicare Plan Review", None,
           False, "Check your coverage, especially if moving or dual-eligible."),
]
