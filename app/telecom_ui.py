import streamlit as st
import requests
import networkx as nx
from pyvis.network import Network
import os

ARANGO_URL = "http://arangodb:8529"
DB_NAME = "telecom"
GRAPH_NAME = "telecom_graph"
USERNAME = "root"
PASSWORD = os.getenv("ARANGO_ROOT_PASSWORD", "openSesame")  # fallback

st.set_page_config(layout="wide")
st.title("📞 Telecom Call Graph Explorer")

phone = st.text_input("Enter a phone number to explore call history (e.g., 123):")

def get_call_graph(phone_number):
    # AQL query to find calls made by a person with a given phone number
    query = {
        "query": f"""
            FOR caller IN person
                FILTER caller._key == @phone
                FOR call IN OUTBOUND caller called
                    LET callee = DOCUMENT(call._to)
                    RETURN {{
                        caller: caller.name,
                        callee: callee.name,
                        timestamp: call.timestamp,
                        duration: call.duration
                    }}
        """,
        "bindVars": {"phone": phone_number}
    }

    response = requests.post(
        f"{ARANGO_URL}/_db/{DB_NAME}/_api/cursor",
        auth=(USERNAME, PASSWORD),
        json=query
    )
    return response.json()

if st.button("Query & Visualize"):
    result = get_call_graph(phone)
    elements = result.get("result", [])
    
    G = nx.MultiDiGraph()

    for item in elements:
        caller = item["caller"]
        callee = item["callee"]
        duration = item.get("duration", "?")
        timestamp = item.get("timestamp", "?")
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
