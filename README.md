# link-analysis

```
hugegraph-telecom-visualizer/
├── backend/
│   ├── app.py                  # FastAPI or Flask API
│   ├── graph_queries.py        # Gremlin/HugeGraph logic
│   └── config.py               # HugeGraph client config
├── frontend/
│   ├── index.html              # Main entry point with D3
│   ├── graph.js                # D3.js force-directed graph logic
│   ├── style.css               # Styling for UI
│   └── utils.js                # Helpers (e.g. API calls)
├── schema/
│   ├── schema.groovy           # HugeGraph schema definition
│   └── sample_data.groovy      # Insert sample vertices and edges
├── queries/
│   └── example_queries.txt     # Sample Gremlin/HugeGraph queries
├── README.md                   # Documentation
└── architecture.png            # (Optional) system overview diagram
```
