import streamlit as st
import json
from streamlit_agraph import agraph, Node, Edge, Config

with open('json_data.json') as json_file:
    data = json.load(json_file)

st.title("Knowledge graphs")
st.markdown("A toy to help explore the connections which we will start to generate as we create more content.")
st.markdown("The green square 'knowledge summary' nodes are permanent. Red triangles are topics. Everything else gets a teal circle.")

# Options default to Topic 2 and Part

options = st.sidebar.multiselect(
     'Select node types',
     ["Content","Topic 1", "Topic 2", "Content type", "Act", "Part", "Chapter", "Section", "Linked knowledge"],
     ["Topic 2", "Part"])

nodeTypes = ["Knowledge summary"] # Always include knowledge summary - these are the nodes that everything else links to
nodeTypes = nodeTypes + options

selectData = {}
selectData["nodes"]= [item for item in data["nodes"] if item['type'] in nodeTypes]
selectData["nodeIDs"] = [item["id"] for item in data["nodes"] if item['type'] in nodeTypes] # Convenince, surface IDs for working out which edges to add.
selectData["edges"] = []

for item in data["edges"]: 
    if (item["source"] in selectData["nodeIDs"]) and (item["target"] in selectData["nodeIDs"]):
        selectData["edges"].append(item)

nodes = []
edges = []

# Style nodes by type

KSnodes = [Node(id=i["id"], label=i["label"], size=300, color="#DBEBC2", symbolType="square") for i in selectData["nodes"] if i["type"] == "Knowledge summary"]
TopicNodes = [Node(id=i["id"], label=i["label"], size=200, color="#F7A7A6", symbolType="diamond") for i in selectData["nodes"] if i["type"] == "Topic 2"]
OtherNodes = [Node(id=i["id"], label=i["label"], size=200) for i in selectData["nodes"] if (i["type"] != "Knowledge summary" and i["type"] != "Topic 2")]

nodes = KSnodes + TopicNodes + OtherNodes

edges = [Edge(source=i["source"], target=i["target"], type="CURVE_SMOOTH") for i in selectData["edges"]]

config = Config(
                directed=True,
                nodeHighlightBehavior=True, 
                highlightColor="#F7A7A6", # or "blue"
                collapsible=True,
                node={'labelProperty':'label'},
                link={'labelProperty': 'label', 'renderLabel': True}
                # **kwargs e.g. node_size=1000 or node_color="blue"
                ) 

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

# Look at the options in init.py https://github.com/ChrisDelClea/streamlit-agraph/blob/master/streamlit_agraph/__init__.py
