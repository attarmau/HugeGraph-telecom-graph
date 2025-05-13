import requests

HUGEGRAPH_URL = "http://localhost:8080"
GRAPH = "hugegraph"
SCHEMA_URL = f"{HUGEGRAPH_URL}/graphs/{GRAPH}/schema"
HEADERS = {"Content-Type": "application/json"}
DEFAULT_CARDINALITY = "SINGLE"

def post_request(url, data):
    try:
        response = requests.post(url, json=data, headers=HEADERS)
        response.raise_for_status()  # Raise HTTPError for bad responses
        print(f"Success: {url} - {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error with request to {url}: {e}")
        return None

def create_vertex_label(label, properties, primary_keys):
    url = f"{SCHEMA_URL}/vertexlabels"
    data = {
        "name": label,
        "properties": properties,
        "primary_keys": primary_keys
    }
    post_request(url, data)

# Function to create a property key
def create_property_key(name, data_type, cardinality=DEFAULT_CARDINALITY):
    url = f"{SCHEMA_URL}/propertykeys"
    data = {
        "name": name,
        "data_type": data_type,
        "cardinality": cardinality
    }
    post_request(url, data)

def create_edge_label(name, source_label, target_label, properties=[]):
    url = f"{SCHEMA_URL}/edgelabels"
    data = {
        "name": name,
        "source_label": source_label,
        "target_label": target_label,
        "properties": properties,
        "frequency": DEFAULT_CARDINALITY
    }
    post_request(url, data)

property_keys = [
    ("name", "TEXT"),
    ("location_name", "TEXT"),
    ("timestamp", "TEXT"),
    ("duration", "INT"),
    ("call_id", "TEXT")
]

for name, dtype in property_keys:
    create_property_key(name, dtype)

create_vertex_label("person", ["name"], ["name"])
create_vertex_label("location", ["location_name"], ["location_name"])
create_vertex_label("call_event", ["call_id", "timestamp", "duration"], ["call_id"])

create_edge_label("called", "person", "person")
create_edge_label("made_at", "call_event", "location")
create_edge_label("from_caller", "call_event", "person")
create_edge_label("to_target", "call_event", "person")
