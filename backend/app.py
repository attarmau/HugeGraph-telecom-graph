from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

# HugeGraph REST endpoint
BASE_URL = "http://localhost:8080/graphs/hugegraph"


### 🧍 Person Insertion
class Person(BaseModel):
    person_id: str
    name: str

@app.post("/insert-person")
def insert_person(person: Person):
    url = f"{BASE_URL}/graph/vertices"
    data = {
        "label": "person",
        "properties": {
            "person_id": person.person_id,
            "name": person.name
        }
    }
    response = requests.post(url, json=data)
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail=response.text)
    return {"message": "Person inserted", "data": response.json()}


### 📍 Location Insertion
class Location(BaseModel):
    location_id: str
    name: str
    block: Optional[str] = None

@app.post("/insert-location")
def insert_location(location: Location):
    url = f"{BASE_URL}/graph/vertices"
    data = {
        "label": "location",
        "properties": {
            "location_id": location.location_id,
            "name": location.name,
            "block": location.block
        }
    }
    response = requests.post(url, json=data)
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail=response.text)
    return {"message": "Location inserted", "data": response.json()}


### 📞 Call Edge Insertion
class Call(BaseModel):
    caller_id: str
    callee_id: str
    time: str  # e.g. "2025-05-01T08:00:00"
    duration: int

@app.post("/insert-call")
def insert_call(call: Call):
    url = f"{BASE_URL}/graph/edges"
    data = {
        "label": "call",
        "outV": call.caller_id,
        "outVLabel": "person",
        "inV": call.callee_id,
        "inVLabel": "person",
        "properties": {
            "time": call.time,
            "duration": call.duration
        }
    }
    response = requests.post(url, json=data)
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail=response.text)
    return {"message": "Call edge inserted", "data": response.json()}
