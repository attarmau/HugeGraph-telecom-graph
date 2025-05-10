# link-analysis

```
hugegraph-telecom-graph/
├── backend/
│   ├── app.py                  
│   ├── graph_queries.py        
│   └── config.py               
├── frontend/
│   ├── index.html              
│   ├── graph.js                
│   ├── style.css               
│   └── utils.js                
├── schema/
│   ├── created_schema.groovy           
│   └── sample_data.groovy      
├── loader/                                
│   ├── telecom_graph_data.json
│   ├── insert_data.sh       
│   ├── person.csv                         
│   ├── location.csv                       
│   └── call.csv                           
├── queries/
│   └── example_queries.txt     
├── README.md                   
└── architecture.png      
      
```

To start, please first clone the entire project. After that, follow the instructions below
```
cd hugegraph-telecom-graph
```
```
chmod +x setup_schema.sh     # (only once)
./setup_schema.sh
```
By doing so, HugeGraph has your full schema set up:
* Property keys
* Vertex labels (person, call_event, location)
* Edge labels (called, made_at)
* Indexes (personByPhone, callByTimestamp)
