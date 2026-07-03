import streamlit as st
import pandas

st.set_page_config(page_title="My App", layout="wide")


pages = {
    "Add to the Graph": [
        st.Page("1_network_display.py", title="Home"),
        st.Page("2_propose_node.py", title="Propose a Node"),
        st.Page("3_propose_connection.py", title="Propose a Connection"),
    ]}
pg = st.navigation(pages)
pg.run()

# --- Sidebar ---
with st.sidebar:
    st.header("Sidebar")
    st.write("Navigate to different pages here.")
