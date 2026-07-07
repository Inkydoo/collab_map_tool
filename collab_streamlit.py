import streamlit as st
import pandas

st.set_page_config(page_title="My App", layout="wide")



with st.sidebar:
    if not st.user.is_logged_in:
        st.button("Log in with Google", on_click=st.login, args=("google",))
    elif st.user.is_logged_in:
        st.button("Logout", on_click=st.logout)



if st.user.is_logged_in:
    pages = {
                "Navigate Pages": [
                    st.Page("1_network_display.py", title="Home"),
                    st.Page("2_propose_node.py", title="Propose a Node"),
                    st.Page("3_propose_connection.py", title="Propose a Connection"),
                ],
                "Review Proposals": [
                    st.Page("4_review_proposals.py", title="Review"),
                ]
            }
else:
    pages = {
        "Navigate Pages": [
            st.Page("1_network_display.py", title="Home"),
            st.Page("2_propose_node.py", title="Propose a Node"),
            st.Page("3_propose_connection.py", title="Propose a Connection"),
        ]
    }
pg = st.navigation(pages)
pg.run()



