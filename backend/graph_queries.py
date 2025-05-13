import requests
import json
from config import HUGEGRAPH_API_BASE, REQUEST_TIMEOUT

def insert_person(person_id, name):
    url = f"{HUGEGRAPH_API_BASE}/graph/vertices"
    data = {
        "label": "person",
        "properties": {
            "person_id": person_id,
            "name": name
        }
    }
    response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
    return response.json()

def insert_location(loc_id, name, block):
    url = f"{HUGEGRAPH_API_BASE}/graph/vertices"
    data = {
        "label": "location",
        "properties": {
            "location_id": loc_id,
            "name": name,
            "block": block
        }
    }
    response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
    return response.json()

def insert_call_edge(caller_id, callee_id, time, duration):
    url = f"{HUGEGRAPH_API_BASE}/graph/edges"
    data = {
        "label": "call",
        "outV": caller_id,
        "outVLabel": "person",
        "inV": callee_id,
        "inVLabel": "person",
        "properties": {
            "time": time,
            "duration": duration
        }
    }
    response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
    return response.json()
