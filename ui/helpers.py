import streamlit as st

def order_answer_map(amap: dict[str, str]) -> tuple[list[str], list[str]]:
    if not isinstance(amap, dict) or not amap:
        st.error(f"order_answer_map received invalid input: {amap}")
        return [], []
    keys = list(amap.keys())
    if not keys:
        st.warning("No keys found in amap, returning empty lists")
        return [], []
    if not all(isinstance(k, str) for k in keys):
        st.error(f"Invalid keys in amap: {keys}")
        return [], []
    if not all(isinstance(amap.get(k), str) for k in keys):
        st.error(f"Invalid values in amap: {amap}")
        return [], []
    try:
        if all(_is_intlike(k) for k in keys):
            ordered_keys = [str(k) for k in sorted(int(str(k)) for k in keys)]
        else:
            ordered_keys = [str(k) for k in keys]
        labels = [amap[k] for k in ordered_keys]
        if not labels:
            st.warning(f"No valid labels generated from {amap}")
        return ordered_keys, labels
    except Exception as e:
        st.error(f"Error in order_answer_map: {e}")
        return [], []

def _is_intlike(x) -> bool:
    try:
        int(str(x))
        return True
    except (ValueError, TypeError):
        return False

def radio_from_answer_map(label, amap, *, key, help_text=None, default_key=None, show_debug=False) -> str | None:
    keys, labels = order_answer_map(amap)
    if not labels:
        st.warning(f"No valid options for radio: {label} with amap {amap}")
        return default_key
    idx = 0 if default_key is None or str(default_key) not in keys else keys.index(str(default_key))
    if idx >= len(labels):
        st.warning(f"Index {idx} out of range for {len(labels)} labels, falling back to 0")
        idx = 0
    if show_debug:
        st.write(f"Debug: labels={labels}, keys={keys}, default_key={default_key}, idx_calc={idx}")
        st.write(f"Attempting st.radio with label={label}, labels={labels}, idx={idx}, key={key}")
    try:
        sel_label = st.radio(label, labels, index=idx, key=key)
        if show_debug:
            st.write(f"st.radio returned: {sel_label}")
        return keys[labels.index(sel_label)] if sel_label in labels else default_key
    except (ValueError, TypeError) as e:
        if show_debug:
            st.error(f"st.radio failed with error: {e}, labels={labels}, idx={idx}")
        return default_key
