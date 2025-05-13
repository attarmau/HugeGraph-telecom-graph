from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/graph")
def get_graph_data():
    hugegraph_url = "http://hugegraph:8080"  # Docker service name
    graph_name = "hugegraph"

    try:
        # Get all vertices
        vertices_res = requests.get(f"{hugegraph_url}/graphs/{graph_name}/graph/vertices")
        vertices = vertices_res.json().get("vertices", [])

        # Get all edges
        edges_res = requests.get(f"{hugegraph_url}/graphs/{graph_name}/graph/edges")
        edges = edges_res.json().get("edges", [])

        # Format for D3.js
        nodes = [
            {
                "id": v["id"],
                "label": v["label"],
                **v["properties"]
            } for v in vertices
        ]
        links = [
            {
                "source": e["outV"],
                "target": e["inV"],
                "label": e["label"],
                **e["properties"]
            } for e in edges
        ]

        return {"nodes": nodes, "links": links}

    except Exception as e:
        return {"error": str(e)}
