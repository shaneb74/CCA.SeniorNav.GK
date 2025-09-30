from core.state import AppState

def compute(app: AppState) -> AppState:
    if app.people and app.people[0].derived.care_level:
        app.cost_outputs.primary_path = app.people[0].derived.care_level
    else:
        app.cost_outputs.primary_path = "in_home"
    app.cost_outputs.sections = {}
    app.cost_outputs.nudges = []
    app.cost_outputs.decision_log = {"engine": "stub"}
    return app
