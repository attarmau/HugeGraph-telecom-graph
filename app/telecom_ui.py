import streamlit as st
import requests
import networkx as nx
from pyvis.network import Network
import os

HUGEGRAPH_URL = "http://hugegraph-server:8080"

st.set_page_config(layout="wide")
st.title("📞 Telecom Call Graph Explorer")

phone = st.text_input("Enter a phone number to explore call history (e.g., 123):")

def get_call_graph(phone_number):
    query = {
        "gremlin": f"""
        g.V().has('person','phone','{phone_number}')
        .as('caller')
        .outE('call').as('call_edge')
        .inV().as('callee')
        .select('caller','call_edge','callee')
        """
    }
    resp = requests.post(f"{HUGEGRAPH_URL}/graphs/hugegraph/gremlin", json=query)
    return resp.json()

if st.button("Query & Visualize"):
    result = get_call_graph(phone)
    elements = result.get("result", {}).get("data", [])
    
    G = nx.MultiDiGraph()

    for item in elements:
        caller = item["caller"]["properties"]["name"]
        callee = item["callee"]["properties"]["name"]
        call_props = item["call_edge"]["properties"]
        duration = call_props.get("duration", "?")
        timestamp = call_props.get("timestamp", "?")
        edge_label = f"{timestamp}, {duration} min"

        G.add_node(caller)
        G.add_node(callee)
        G.add_edge(caller, callee, label=edge_label)

    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)
    net.show_buttons(filter_=['physics'])
    net.save_graph("assets/graph.html")

    st.success("Graph generated below 👇")
    with open("assets/graph.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=650, scrolling=True)
