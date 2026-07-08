import pandas as pd
import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="Propose Node", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Graph Data", ttl=0)

nodes = df["Name"].values
types = ["Infrastructure","Disaster Risk", "Social", "Economic", "Inequality", "Human Rights", "Food Systems", "Energy Systems", "Health", "Misc."]
# --- Title ---
st.title("Propose an Impact or Vulnerability")
with st.container(key='node_description', border=True):
    st.subheader("Fill out this proposal form to add a new impact or vulnerability to the map!")
    st.write("1. First provide the name of the node, and then list what nodes have caused this one.")
    st.write("2. Explain what type of impact it is. This will change the color and icon on the map.")
    st.write("3. Finally, provide evidence for your proposal! This should be some argumentation or explanation, followed by a link to a source.")
    st.write("Hit submit, and wait for the confirmation message before leaving the page.")

@st.fragment()
def node_proposal_portal():
    name = st.text_input("What **impact** or **vulnerability** would you like to propose?")
    connect = st.multiselect("What are the causes of this impact?", nodes)
    connect_json = json.dumps(connect)
    node_type = st.selectbox("What type of impact is this?", types)
    evidence = st.text_input("Please provide argumentation for your impact, with evidence.")
    group_id = st.text_input("What is your GroupID?")
    if st.button("Submit"):
        if not name or not connect or not node_type or not evidence:
            st.write("At least one field is missing, please complete the form")
        elif name in list(nodes):
            st.write("This impact already exists! No duplicate names")
        elif not group_id:
            st.write("You must include your Group ID!")
        else:
            submission_time = datetime.now().strftime("%A, %B %d, %Y, at %H:%M:%S")
            new_row = pd.DataFrame(data={"Name": name, "Type": node_type, "Connection": connect_json,"Evidence": evidence, "Submission Time": submission_time, "Status": "Review", "GroupID": group_id}, index=[0])

            df = conn.read(worksheet="Proposed Nodes", ttl=0)
            df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Proposed Nodes", data=df)
            st.dataframe(df)
            st.write("Successful Submission, await review!")

node_proposal_portal()