import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_agraph as ag
import pandas as pd
import json
import base64

# --- Title ---
st.title("Collaborative Risk Mapping: Impacts and Vulnerabilities of El Niño")
st.subheader("WOMENVAI x UCL Humanitarian Institute; July 9th, 2026")
st.divider()
with st.container(border=True, key='intro'):
    st.subheader("Introduction")
    st.write("El Niño is a reoccurring weather phenomena with drastic impact for life, society, and our governance. "
             "Increased global temperatures and variation in local weather across the world poses serious risks, "
             "some more obvious than others.")
    st.write("During this workshop, we seek to explore the breadth of impacts and vulnerabilities created by El Niño "
             "conditions, and to map them into a comprehensive and comprehensible scheme. Participants will "
             "collaborate to qualitatively map the wide-range of direct and indirect/cascading impacts of a major "
             "climatic event. The mapping produced takes the form of a graphical network, which will be created using "
             "the individual contributions from all groups of participants. The goals of this workshop are divided "
             "into two categories. First, to use the combined wisdom of many students to create a useful and "
             "meaningful mapping of impacts and vulnerabilities. Second, to develop a repeatable and reusable "
             "methodology for mapping specific impacts in a complex risk landscape.")

st.divider()
st.caption("The current network:")

# Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Graph Data", ttl=0)


# --- Define Types ---

def local_image_to_data_uri(path):
    with open(path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    ext = path.split(".")[-1]  # e.g. "png", "svg"
    return f"data:image/{ext};base64,{encoded}"


type_dict = {"Physical": ["#ffcc00", "icons/physical.png"],
             "Social": ["#3399cc", "icons/social.png"],
             "Economic": ["#669900", "icons/economic.png"],
             "Inequality": ["#6fb1a0", "icons/inequality.png"],
             "Human Rights": ["#990066", "icons/humanrights.png"],
             "Food Systems": ["#99cc33", "icons/food.png"],
             "Energy Systems": ["#ff6600", "icons/energy.png"],
             "Misc.": ["#ff9900", "icons/misc.png"],
             "Source": ["color", "icons/source.png"]}

# --- Widget area (below the title) ---
nodes = []
edges = []

nodes.append(ag.Node(id="El Niño", label="El Niño", size=30, shape="circularImage",
                     image=local_image_to_data_uri("icons/physical.png"), imagePadding=5))

for row in range(len(df)):
    node_name = df.iat[row, 0]
    node_type = df.iat[row, 1]
    nodes.append(ag.Node(id=node_name, label=node_name, color=type_dict[node_type][0], shape="circularImage",
                         image=local_image_to_data_uri(type_dict[node_type][1]), imagePadding=7, size=25))

    connections = json.loads(df.iat[row, 2])
    for connect in connections:
        edges.append(ag.Edge(source=connect, target=node_name))


@st.fragment()
def display_graph():
        config = ag.Config(width=1200,
                           height=600,
                           directed=True,
                           physics=True,
                           hierarchical=False,
                           )

        ag.agraph(nodes=nodes, edges=edges, config=config)


widget_container = st.container(border=True, key='network')
with widget_container:
    display_graph()
    if st.button("Refresh", key='refresh_network'):
        st.rerun()

st.divider()
with st.container(key='intro2', border=True):
    st.subheader("Add to the Map!")
    st.write("Beyond what has been currently identified, there are certainly more cascading and compounding risks. "
             "Using the two buttons below, you can propose new additions to the map! Consider new impacts or "
             "vulnerabilities (the 'nodes') or how they cause and influence each other (the 'connections'). After "
             "submitting a proposed addition to the map, a review will check your work, and then add it!")
    # --- Two buttons that open two different pages ---
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Propose Node", use_container_width=True):
            st.switch_page("2_propose_node.py")

    with col2:
        if st.button("Propose Connection", use_container_width=True):
            st.switch_page("3_propose_connection.py")

st.divider()
with st.container(key="intro3", border=True):
    st.subheader("Start Your Research")
    st.write("The exercise topic of this workshop is the incoming El Niño-Southern Oscillation phenomenon, occurring "
             "this year and in near-future years (WMO, 2026). Participants are given the first-order climate effects "
             "(increased/decreased rainfall, greater weather variation, temporary global warming) and seek to "
             "identify the widest possible range of cascading impacts, and vulnerable groups, across all possible "
             "sectors.  This exercise is qualitative, in that participants are not expected to focus on the "
             "intensity, frequency, or likelihood of each impact, but rather just on the connection to other impacts "
             "and vulnerabilities.")
    st.write("To get you started on your work, we have included a few useful sources to aid your research on the "
             "impacts and vulnerabilities of El Niño. This is not a complete collection of resources, "
             "and we encourage you to continue your research online!")
    st.divider()
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("Useful websites summarizing the many immediate impacts")
        st.markdown("- [NOAA El Niño Impacts](https://www.pmel.noaa.gov/elnino/impacts-of-el-nino)")
        st.markdown("- [FAO Information on El Niño Impacts (Food & Famine)](https://www.fao.org/el-nino/en)")
        st.markdown("- [Wellcome Trust: El Niño and Health]("
                    "https://www.preventionweb.net/news/explained-how-el-nino-impacts-health)")
        st.markdown("- [NASA El Niño and Crop Yields](https://science.nasa.gov/earth/earth-observatory/el-nino"
                    "-forecast-to-contribute-to-food-insecurity-152005/)")
        st.markdown("- [El Niño and Disasters](https://shelterbox.org/disasters-explained/el-nino/)")

    with col4:
        st.markdown("Articles and summaries of the impacts of El Niño and climate change")
        st.markdown("- [El Niño Storylines and Plausible Climate Futures for the Indo-Pacific]("
                    "https://www.climatecentre.org/wp-content/uploads/Climate-Centre-El-Nino-Storylines-Indo-Pacific-region.pdf)")
        st.markdown("- [Climate extremes and socioeconomic impact of El Niño and La Niña events]("
                    "https://www.sciencedirect.com/science/article/pii/S2211464525001423#sec5)")
        st.markdown("- [Socioeconomic Impacts of Climate Change]("
                    "https://www.science.org/doi/full/10.1126/science.aad9837?casa_token=mFNchKksPfkAAAAA"
                    "%3ADXHPXePhEChiplAG3WddbF4YjoA8tY-0sAha-Bg-86BiE44rA4NHHBQxYJQIjU6VyNpFcms5BnNmPPY)")
        st.markdown("- [Gender and climate change](https://wires.onlinelibrary.wiley.com/doi/full/10.1002/wcc.451)")
        st.markdown("- [Climate change and Social Inequality]("
                    "https://bhekisisa.org/wp-content/uploads/2023/09/wp152_2017.pdf)")



st.write("Learn more about the organizations hosting this event below!")
col5, col6 = st.columns(2)
with col5:
    st.subheader("WOMENVAI")
    st.image("icons/womenvai_logo.png",width=300, caption='Click to learn more!', link='https://womenvai.org/')
with col6:
    st.subheader("UCL Humanitarian Institute")
    st.image("icons/ucl_humanitarian.png", width=300, caption='Click to learn more!', link='https://www.ucl.ac.uk/humanitarian/')