from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from graph_queries import insert_person, insert_location, insert_call_edge

app = FastAPI()


### 🧍 Person Insertion
class Person(BaseModel):
    person_id: str
    name: str

@app.post("/insert-person")
def add_person(person: Person):
    try:
        result = insert_person(person.person_id, person.name)
        return {"message": "Person inserted", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### Location Insertion
class Location(BaseModel):
    location_id: str
    name: str
    block: Optional[str] = None

@app.post("/insert-location")
def add_location(location: Location):
    try:
        result = insert_location(location.location_id, location.name, location.block)
        return {"message": "Location inserted", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### Call Edge Insertion
class Call(BaseModel):
    caller_id: str
    callee_id: str
    time: str  # e.g. "2025-05-01T08:00:00"
    duration: int

@app.post("/insert-call")
def add_call(call: Call):
    try:
        result = insert_call_edge(call.caller_id, call.callee_id, call.time, call.duration)
        return {"message": "Call edge inserted", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
