import streamlit as st
import requests
import networkx as nx
from pyvis.network import Network
import os

HUGEGRAPH_URL = "http://hugegraph-server:8080"

st.set_page_config(layout="wide")
st.title("📞 Telecom Call Graph Explorer")

phone = st.text_input("Enter a phone number to explore call history (e.g., 9781-1234):")

def get_call_graph(phone_number):
    query = {
        "gremlin": f"""
        g.V().has('person','phone','{phone_number}').as('caller')
        .outE('called').as('call_edge')
        .inV().as('callee')
        .inE('called').outV().as('call_event')
        .out('made_at').as('location')
        .select('caller', 'callee', 'call_edge', 'call_event', 'location')
        .by(valueMap(true))
        """
    }
    resp = requests.post(f"{HUGEGRAPH_URL}/graphs/hugegraph/gremlin", json=query)
    return resp.json()

if st.button("Query & Visualize"):
    result = get_call_graph(phone)
    elements = result.get("result", {}).get("data", [])
    
    if not elements:
        st.warning("No call records found for this number.")
    else:
        G = nx.MultiDiGraph()

        for item in elements:
            caller_name = item["caller"]["name"][0]
            callee_name = item["callee"]["name"][0]

            duration = item["call_edge"]["duration"]
            timestamp = item["call_edge"]["timestamp"]

            city = item["location"]["city"][0]
            block = item["location"]["block"][0]
            location_info = f"{city} - {block}"

            edge_label = f"{timestamp}, {duration} min\n📍{location_info}"

            G.add_node(caller_name)
            G.add_node(callee_name)
            G.add_edge(caller_name, callee_name, label=edge_label)

        net = Network(height="600px", width="100%", directed=True)
        net.from_nx(G)
        net.show_buttons(filter_=['physics'])
        
        if not os.path.exists("assets"):
            os.makedirs("assets")

        net.save_graph("assets/graph.html")

        st.success("Graph generated below 👇")
        with open("assets/graph.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=650, scrolling=True)
