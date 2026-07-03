import streamlit as st
import pandas as pd

# --- Title ---
st.title("My Streamlit App")

# --- Widget area (below the title) ---
widget_container = st.container()
with widget_container:
    st.subheader("Widget")
    # Replace this with whatever widget you actually want
    # (a chart, a slider, a dataframe, etc.)
    value = st.slider("Example widget", 0, 100, 50)
    st.write(f"Current value: {value}")

st.divider()

# --- Two buttons that open two different pages ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Propose Node", use_container_width=True):
        st.switch_page("2_propose_node.py")

with col2:
    if st.button("Propose Connection", use_container_width=True):
        st.switch_page("3_propose_connection.py")