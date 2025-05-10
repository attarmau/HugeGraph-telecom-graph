#!/bin/bash

API="http://localhost:8080/graphs/hugegraph/schema"
HEADERS="-H Content-Type:application/json"

echo "🔧 Creating PropertyKeys..."
curl -X POST $API/propertykeys $HEADERS -d '{"name": "id", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "target_id", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "name", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "phone", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "timestamp", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "duration", "data_type": "INT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "city", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "block", "data_type": "TEXT", "cardinality": "SINGLE"}'
curl -X POST $API/propertykeys $HEADERS -d '{"name": "location_id", "data_type": "TEXT", "cardinality": "SINGLE"}'

echo "🧩 Creating VertexLabels..."
curl -X POST $API/vertexlabels $HEADERS -d '{
  "name": "person",
  "properties": ["id", "name", "phone"],
  "primary_keys": ["id"]
}'

curl -X POST $API/vertexlabels $HEADERS -d '{
  "name": "call_event",
  "properties": ["id", "target_id", "timestamp", "duration", "location_id"],
  "primary_keys": ["id", "target_id", "timestamp"]
}'

curl -X POST $API/vertexlabels $HEADERS -d '{
  "name": "location",
  "properties": ["id", "city", "block"],
  "primary_keys": ["id"]
}'

echo "🔗 Creating EdgeLabels..."
curl -X POST $API/edgelabels $HEADERS -d '{
  "name": "called",
  "source_label": "person",
  "target_label": "person",
  "properties": ["timestamp", "duration"],
  "multiplicity": "MULTI"
}'

curl -X POST $API/edgelabels $HEADERS -d '{
  "name": "made_at",
  "source_label": "call_event",
  "target_label": "location",
  "multiplicity": "ONE2ONE"
}'

echo "📦 Creating IndexLabels..."
curl -X POST $API/indexlabels $HEADERS -d '{
  "name": "personByPhone",
  "base_type": "VERTEX_LABEL",
  "base_value": "person",
  "index_type": "SECONDARY",
  "fields": ["phone"]
}'

curl -X POST $API/indexlabels $HEADERS -d '{
  "name": "callByTimestamp",
  "base_type": "VERTEX_LABEL",
  "base_value": "call_event",
  "index_type": "SECONDARY",
  "fields": ["timestamp"]
}'

echo "✅ Done setting up HugeGraph schema!"
