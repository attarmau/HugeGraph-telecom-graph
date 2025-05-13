import uuid
import json

# Function to generate a UUID for each vertex
def generate_uuid():
    return str(uuid.uuid4())

# Example person data
people = [
    {"name": "Alice", "phone": "9781-1234"},
    {"name": "Bob", "phone": "8769-1234"},
    {"name": "Jocab", "phone": "8762-1234"},
    {"name": "Tiffany", "phone": "9873-1234"},
    {"name": "Peter", "phone": "9898-1234"},
    {"name": "Sally", "phone": "8749-1239"},
    {"name": "Wendy", "phone": "9823-1234"},
    {"name": "Tammy", "phone": "9812-2345"},
    {"name": "John", "phone": "9823-1234"},
    {"name": "Julian", "phone": "9872-1235"},
]

# Example locations
locations = [
    {"city": "Clementi", "block": "Blk 345"},
    {"city": "Tampines", "block": "Blk 234"},
]

# Example call data
calls = [
    {"caller": "person_1", "target": "person_2", "timestamp": "2025-05-01-080000", "duration": 2, "location": "location_101"},
    {"caller": "person_1", "target": "person_3", "timestamp": "2025-05-02-081000", "duration": 4, "location": "location_101"},
]

# Inserting people vertices
for person in people:
    person_id = generate_uuid()  # UUID for person
    person_vertex = {
        "id": person_id,
        "label": "person",
        "type": "vertex",
        "properties": {
            "name": person["name"],
            "phone": person["phone"]
        }
    }
    print(f"Insert vertex person: {json.dumps(person_vertex)}")

# Inserting location vertices
for location in locations:
    location_id = generate_uuid()  # UUID for location
    location_vertex = {
        "id": location_id,
        "label": "location",
        "type": "vertex",
        "properties": {
            "city": location["city"],
            "block": location["block"]
        }
    }
    print(f"Insert vertex location: {json.dumps(location_vertex)}")

# Inserting edges with UUIDs for edge IDs
for call in calls:
    call_id = generate_uuid()  # UUID for call_event
    call_event_vertex = {
        "id": call_id,
        "label": "call_event",
        "type": "vertex",
        "properties": {
            "timestamp": call["timestamp"],
            "duration": call["duration"],
            "caller": call["caller"],
            "target": call["target"],
            "location_id": call["location"]
        }
    }
    print(f"Insert vertex call_event: {json.dumps(call_event_vertex)}")

    # Use UUIDs for edge IDs instead of manual construction
    from_caller_edge = {
        "id": generate_uuid(),
        "label": "from_caller",
        "type": "edge",
        "inV": call['target'],
        "outV": call['caller']
    }
    to_target_edge = {
        "id": generate_uuid(),
        "label": "to_target",
        "type": "edge",
        "inV": call['caller'],
        "outV": call['target']
    }
    print(f"Insert edge from_caller: {json.dumps(from_caller_edge)}")
    print(f"Insert edge to_target: {json.dumps(to_target_edge)}")
