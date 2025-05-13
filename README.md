# link-analysis

```
hugegraph-telecom-graph/
├── backend/
│   ├── app.py                  
│   ├── graph_queries.py
│   ├── config.py       
│   └── Dockerfile               
├── frontend/
│   ├── index.html              
│   ├── graph.js                
│   ├── style.css            
│   └── utils.js   # pending              
├── loader/                                
│   ├── telecom_graph_data.json
│   ├── insert_data.sh       
│   ├── person.csv                         
│   ├── location.csv                       
│   └── call.csv                           
├── queries/
│   └── example_queries.txt
├── setup_schema.sh
├── requirement.txt
├── docker-compose.yaml
├── README.md                   
└── architecture.png # pending     
      
```

To start, please first clone the entire project. After that, follow the instructions below.
# Start all services
```
docker compose up --build
```
# Create Schema
```
cd hugegraph-telecom-graph
```
```
python3 setup_schema.py
```
By doing so, HugeGraph has your full schema set up:
* Property keys
* Vertex labels (person, call_event, location)
* Edge labels (called, made_at)
* Indexes (personByPhone, callByTimestamp)

# Insert dummy data
```
python3 insert_data.py
```
Check the backend /graph endpoint response:
```
curl http://localhost:8000/graph
```
