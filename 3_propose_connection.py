import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import json
from datetime import datetime

st.set_page_config(page_title="Propose Connection", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Graph Data", ttl=0)

nodes = df["Name"].values


# --- Title ---
st.title("Propose Connection!")
with st.container(key='connection_description', border=True):
    st.subheader("Fill out this proposal form to add new connections to the map!")
    st.write("1. Provide the name of the target nodes (the arrows will point toward these).")
    st.write("2. Provide the name of the causal or source nodes (the arrows will point away from these).")
    st.write("3. Finally, provide evidence for your proposal! This should be some argumentation or explanation, followed by a link to a source.")
    st.write("Hit submit, and wait for the confirmation message before leaving the page.")
@st.fragment()
def connect_proposal_portal():
    target = None
    connect = None
    evidence = None

    target = st.multiselect("What impact(s) are being caused by others? (the **target** node)", nodes)
    if len(target) == 1:
        connect = st.multiselect("What are the causes of this impact? (the **source** node)", nodes)
    elif len(target) > 1:
        connect = st.selectbox("What is the cause of these impacts? (the **source** node)", nodes)

    if connect is not None:
        target_json = json.dumps(target)
        connect_json = json.dumps(connect)
        evidence = st.text_input("Please provide argumentation for your impact, with evidence.")
        group_id = st.text_input("What is your GroupID?")
        if st.button("Submit"):
            if not evidence or not connect:
                st.write("At least one field is empty! Please complete the form")
            elif not group_id:
                st.write("Please add your GroupID!")
            else:
                submission_time = datetime.now().strftime("%A, %B %d, %Y, at %H:%M:%S")
                new_row = pd.DataFrame(data={"Target": target_json, "Cause": connect_json, "Evidence": evidence,
                                             "Submission Time": submission_time, "Status": "Review", "GroupID": group_id}, index=[0])

                df = conn.read(worksheet="Proposed Connections", ttl=0)
                df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Proposed Connections", data=df)
                st.dataframe(df)
                st.write("Successful Submission, await review!")

connect_proposal_portal()