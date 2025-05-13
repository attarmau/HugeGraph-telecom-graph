import csv
import requests
import uuid  

HUGEGRAPH_URL = "http://localhost:8080"
GRAPH = "hugegraph"

def insert_vertex(label, properties):
    payload = {
        "label": label,
        "properties": properties
    }
    res = requests.post(f"{HUGEGRAPH_URL}/graphs/{GRAPH}/graph/vertices", json=payload)
    print(f"📌 Insert vertex {label}: {res.status_code} - {res.text}")

def insert_edge(label, outV, outVLabel, inV, inVLabel, properties):
    payload = {
        "label": label,
        "outV": outV,
        "outVLabel": outVLabel,
        "inV": inV,
        "inVLabel": inVLabel,
        "properties": properties
    }
    res = requests.post(f"{HUGEGRAPH_URL}/graphs/{GRAPH}/graph/edges", json=payload)
    print(f"🔗 Insert edge {label}: {res.status_code} - {res.text}")

def load_persons():
    with open('person.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insert_vertex("person", {
                "id": row["id"],
                "name": row["name"],
                "phone": row["phone"]
            })

def load_locations():
    with open('location.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insert_vertex("location", {
                "id": row["id"],
                "city": row["city"],
                "block": row["block"]
            })

def load_calls():
    with open('call.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            call_id = str(uuid.uuid4())

            insert_vertex("call_event", {
                "id": call_id,
                "target_id": row["target_id"],
                "timestamp": row["timestamp"],
                "duration": int(row["duration"]),
                "location_id": row["location_id"]
            })

            insert_edge("called", row["id"], "person", row["target_id"], "person", {
                "timestamp": row["timestamp"],
                "duration": int(row["duration"])
            })

            insert_edge("made_at", call_id, "call_event", row["location_id"], "location", {})
            insert_edge("from_caller", call_id, "call_event", row["id"], "person", {})
            insert_edge("to_target", call_id, "call_event", row["target_id"], "person", {})

def main():
    print("🚀 Start loading data...")
    load_persons()
    load_locations()
    load_calls()
    print("✅ Data loading completed!")

if __name__ == "__main__":
    main()
