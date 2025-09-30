import json
import streamlit as st
from dataclasses import asdict
from .state import AppState

KEY = "_app_state_json"

def load_state() -> AppState:
    if KEY in st.session_state:
        try:
            _ = json.loads(st.session_state[KEY])
            return AppState()
        except Exception:
            return AppState()
    state = AppState()
    st.session_state[KEY] = to_json(state)
    return state

def save_state(state: AppState) -> None:
    st.session_state[KEY] = to_json(state)

def to_json(state: AppState) -> str:
    return json.dumps(asdict(state))
