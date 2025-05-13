import os

HUGEGRAPH_HOST = os.getenv("HUGEGRAPH_HOST", "http://server:8080")
GRAPH_NAME = os.getenv("GRAPH_NAME", "hugegraph")
HUGEGRAPH_API_BASE = f"{HUGEGRAPH_HOST}/graphs/{GRAPH_NAME}"
REQUEST_TIMEOUT = 10  # seconds
ENABLE_DEBUG_LOGS = True
