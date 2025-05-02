#!/bin/bash
set -e

echo "⌛ Waiting for HugeGraph server to be ready..."
until curl -s http://hugegraph-server:8080/graphs; do
  sleep 2
done

echo "✅ HugeGraph is up. Creating graph schema..."
curl -XPOST http://hugegraph-server:8080/graphs/telecomgraph -H "Content-Type: application/json"

curl -XPOST http://hugegraph-server:8080/graphs/telecomgraph/gremlin \
  -H "Content-Type: application/json" \
  -d "{\"gremlin\": \"$(cat /init/create_schema.groovy | tr '\n' ' ')\"}"

echo "✅ Schema created. Loading data..."
curl -XPOST http://hugegraph-server:8080/graphs/telecomgraph/graph/load \
  -H "Content-Type: application/json" \
  -d "@/init/telecom_graph_data.json"

echo "✅ Data loading complete."
