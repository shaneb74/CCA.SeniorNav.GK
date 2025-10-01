
from dataclasses import dataclass
from typing import Literal

AppliesTo = Literal["household", "A", "B", "split"]

@dataclass(frozen=True)
class ModuleDef:
    id: str
    title: str
    subtitle: str
    icon: str  # emoji or name; decorative only
    applies_to: AppliesTo
    selectable: bool = True
    order: int = 100

CATALOG: list[ModuleDef] = [
    ModuleDef("income", "Income", "Per person & household", "💵", "split", order=10),
    ModuleDef("benefits", "Benefits", "VA, Medicaid, LTC", "🎖️", "split", order=20),
    ModuleDef("home", "Home Decision", "Keep / Sell / Reverse", "🏠", "household", order=30),
    ModuleDef("home_mods", "Home Mods", "Safety improvements", "🛠️", "household", order=40),
    ModuleDef("care_inhome", "In-Home Care", "Hours/day & adders", "👩‍⚕️", "split", order=50),
    ModuleDef("care_al_mc", "AL / MC", "Level + adders", "🏥", "split", order=60),
    ModuleDef("assets", "Assets", "Cash, equity, annuities", "💼", "household", order=70),
    ModuleDef("other_costs", "Other Monthly", "Meds, premiums, misc", "🧾", "household", order=80),
    ModuleDef("review", "Smart Review", "Expert suggestions", "🧠", "household", selectable=False, order=190),
    ModuleDef("export", "Exports", "PDF / CSV", "📄", "household", selectable=False, order=200),
]
