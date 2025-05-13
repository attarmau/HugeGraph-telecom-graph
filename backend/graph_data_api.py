from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import os

router = APIRouter()

HUGEGRAPH_URL = os.getenv("HUGEGRAPH_URL", "http://localhost:8080/graphs/hugegraph")

@router.get("/graph-data")
def get_graph_data():
    nodes = []
    links = []
    node_ids = set()

    res_vertices = requests.get(f"{HUGEGRAPH_URL}/graph/vertices")
    for v in res_vertices.json().get("vertices", []):
        v_id = v["id"]
        label = v["label"]
        props = v.get("properties", {})
        name = props.get("name", props.get("block", f"{label}_{v_id}"))
        if v_id not in node_ids:
            nodes.append({
                "id": v_id,
                "name": name,
                "label": label,
                "group": {"person": 1, "location": 2, "call_event": 3}.get(label, 4)
            })
            node_ids.add(v_id)

    res_edges = requests.get(f"{HUGEGRAPH_URL}/graph/edges")
    for e in res_edges.json().get("edges", []):
        links.append({
            "source": e["outV"],
            "target": e["inV"],
            "value": 1,
            "label": e["label"]
        })

    return JSONResponse(content={"nodes": nodes, "links": links})
