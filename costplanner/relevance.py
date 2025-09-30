from core.state import AppState

def map_drawers(app: AppState) -> dict:
    return {"in_home": {"visibility": "show", "weight": 90},
            "assisted_living": {"visibility": "show", "weight": 60},
            "memory_care": {"visibility": "deemphasize", "weight": 40},
            "home_mods": {"visibility": "hide", "weight": 0}}
