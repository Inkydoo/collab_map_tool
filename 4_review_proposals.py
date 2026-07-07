import pandas as pd
import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Review Proposal", layout="wide")

if not st.user.is_logged_in:
    st.stop()

conn = st.connection("gsheets", type=GSheetsConnection)
all_proposal_nodes = conn.read(worksheet="Proposed Nodes", ttl=0)
proposal_nodes = all_proposal_nodes[(all_proposal_nodes["Status"]=="Review")]
all_proposal_connections = conn.read(worksheet="Proposed Connections", ttl=0)
proposal_connections = all_proposal_connections[(all_proposal_connections["Status"]=="Review")]
node_count = len(proposal_nodes)
connections_count = len(proposal_connections)

if 'node_buttons' not in st.session_state:
    st.session_state["node_buttons"] = 0
if 'connections_buttons' not in st.session_state:
    st.session_state["connections_buttons"] = 0


def accept_node(proposal):
    df = conn.read(worksheet="Graph Data", ttl=0)
    df = pd.concat([df, proposal])
    conn.update(worksheet="Graph Data", data=df)
    st.session_state["node_buttons"] = 0


def accept_connections(proposal):
    df = conn.read(worksheet="Graph Data", ttl=0)
    rows = df[(df["Name"].isin(json.loads(proposal["Target"].iloc[0])))]
    for idx, row in rows.iterrows():
        old_value = set(json.loads(row["Connection"]))
        old_value.update(json.loads(proposal["Cause"].iloc[0]))
        new_value = list(old_value)
        df.at[idx, "Connection"] = json.dumps(new_value)

    conn.update(worksheet="Graph Data", data=df)
    st.session_state["connection_buttons"] = 0


def increment_buttons_node():
    st.session_state["node_buttons"] += 1


def decrement_buttons_node():
    st.session_state["node_buttons"] -= 1


def increment_buttons_connections():
    st.session_state["connections_buttons"] += 1


def decrement_buttons_connections():
    st.session_state["connections_buttons"] -= 1


st.header("Here you can review the proposed nodes")
st.write("Accept or Reject nodes")
st.divider()

# ------------------------ Nodes to review section -----------------------------


col1, col2 = st.columns(2)
with col1:
    if st.session_state["node_buttons"] > 0:
        st.button("⏪", on_click=decrement_buttons_node)
with col2:
    if (st.session_state["node_buttons"] + 1) < node_count:
        st.button("⏩", on_click=increment_buttons_node)

st.write(st.session_state["node_buttons"])
st.divider()
st.dataframe(proposal_nodes)
if len(proposal_nodes) > 0:
    node_name = proposal_nodes.iat[st.session_state["node_buttons"], 0]
    node_type = proposal_nodes.iat[st.session_state["node_buttons"], 1]
    node_connections = proposal_nodes.iat[st.session_state["node_buttons"], 2]
    node_evidence = proposal_nodes.iat[st.session_state["node_buttons"], 3]
    node_submission_time = proposal_nodes.iat[st.session_state["node_buttons"], 4]

    st.header("Name of Impact:")
    st.write(node_name)
    st.header("Type of Impact:")
    st.write(node_type)
    st.header("Causes of Impact:")
    st.write(node_connections)
    st.header("Evidence Provided:")
    st.write(node_evidence)
    node_decision = st.selectbox("Accept or Reject?", ["Accept", "Reject"], key="decision_node")
    if node_decision == "Accept":
        if st.button("Submit", key="node_yes"):
            accept_node(proposal_nodes.iloc[[st.session_state["node_buttons"]]])
            all_proposal_nodes.loc[all_proposal_nodes["Submission Time"] == node_submission_time, "Status"] = "Accepted"
            conn.update(worksheet="Proposed Nodes", data=all_proposal_nodes)
            st.rerun()

    if node_decision == "Reject":
        if st.button("Submit", key="node_no"):
            all_proposal_nodes.loc[all_proposal_nodes["Submission Time"] == node_submission_time, "Status"] = "Rejected"
            conn.update(worksheet="Proposed Nodes", data=all_proposal_nodes)
            st.session_state["node_buttons"] = 0
            st.rerun()

else:
    st.write("There are no submitted proposals right now, come back later!")
st.divider()

# ------------------------ Connections to review section -----------------------------
st.title("Review Connections")

col1, col2 = st.columns(2)
with col1:
    if st.session_state["connections_buttons"] > 0:
        st.button("⏪", key='connect_left', on_click=decrement_buttons_connections)
with col2:
    if (st.session_state["connections_buttons"] + 1) < connections_count:
        st.button("⏩", key='connect_right', on_click=increment_buttons_connections)

st.write(st.session_state["connections_buttons"])
st.divider()
st.dataframe(proposal_connections)
if len(proposal_connections) > 0:
    connections_target = proposal_connections.iat[st.session_state["connections_buttons"], 0]
    connections_cause = proposal_connections.iat[st.session_state["connections_buttons"], 1]
    connections_evidence = proposal_connections.iat[st.session_state["connections_buttons"], 2]
    connections_submission_time = proposal_connections.iat[st.session_state["connections_buttons"], 3]

    st.header("Name of Target:")
    st.write(connections_target)
    st.header("Causes of Impact:")
    st.write(connections_cause)
    st.header("Evidence Provided:")
    st.write(connections_evidence)
    connections_decision = st.selectbox("Accept or Reject?", ["Accept", "Reject"], key='connection_review')
    if connections_decision == "Accept":
        if st.button("Submit", key='connect_yes'):
            accept_connections(proposal_connections.iloc[[st.session_state["connections_buttons"]]])
            all_proposal_connections.loc[all_proposal_connections["Submission Time"] == connections_submission_time, "Status"] = "Accepted"
            conn.update(worksheet="Proposed Connections", data=all_proposal_connections)
            st.rerun()

    if connections_decision == "Reject":
        if st.button("Submit", key='connect_no'):
            all_proposal_connections.loc[all_proposal_connections["Submission Time"] == connections_submission_time, "Status"] = "Rejected"
            conn.update(worksheet="Proposed Connections", data=all_proposal_connections)
            st.session_state["connection_buttons"] = 0
            st.rerun()


else:
    st.write("There are no submitted proposals right now, come back later!")
