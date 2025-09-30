from core.state import AppState

DEFAULTS = {"in_home", "assisted_living", "compare"}

def ensure_defaults(app: AppState) -> AppState:
    if not app.cost_inputs.scenarios:
        app.cost_inputs.scenarios.update(DEFAULTS)
    return app
