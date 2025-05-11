from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graph_queries import get_telecom_graph_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/graph-data")
def graph_data():
    return get_telecom_graph_data()
