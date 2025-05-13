import requests
import json

BASE_URL = "http://localhost:8080/graphs/telecom"

def insert_person(person_id, name):
    url = f"{BASE_URL}/graph/vertices"
    data = {
        "label": "person",
        "properties": {
            "person_id": person_id,
            "name": name
        }
    }
    response = requests.post(url, json=data)
    return response.json()

def insert_location(loc_id, name, block):
    url = f"{BASE_URL}/graph/vertices"
    data = {
        "label": "location",
        "properties": {
            "location_id": loc_id,
            "name": name,
            "block": block
        }
    }
    response = requests.post(url, json=data)
    return response.json()

def insert_call_edge(caller_id, callee_id, time, duration):
    url = f"{BASE_URL}/graph/edges"
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
    response = requests.post(url, json=data)
    return response.json()
