#!/bin/bash

set -euo pipefail

URL="http://localhost:8080/graphs/hugegraph/graph"

insert_vertex() {
  local response
  response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$1" "$URL/vertices")
  body=$(echo "$response" | head -n1)
  code=$(echo "$response" | tail -n1)
  if [[ "$code" -ne 201 ]]; then
    echo "❌ Failed to insert vertex: $1"
    echo "Response: $body"
    exit 1
  fi
}

insert_edge() {
  local response
  response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$1" "$URL/edges")
  body=$(echo "$response" | head -n1)
  code=$(echo "$response" | tail -n1)
  if [[ "$code" -ne 201 ]]; then # HugeGraph uses 201 for successful edge creation too
    echo "❌ Failed to insert edge: $1"
    echo "Response: $body"
    exit 1
  fi
}

echo "🔹 Inserting persons..."
insert_vertex '{"label":"person","properties":{"id":"person_1","name":"Alice","phone":"9781-1234"}}'
insert_vertex '{"label":"person","properties":{"id":"person_2","name":"Bob","phone":"8769-1234"}}'
insert_vertex '{"label":"person","properties":{"id":"person_3","name":"John","phone":"9823-1234"}}'
insert_vertex '{"label":"person","properties":{"id":"person_4","name":"Tiffany","phone":"9873-1234"}}'
insert_vertex '{"label":"person","properties":{"id":"person_5","name":"Peter","phone":"9898-1234"}}'

echo "🔹 Inserting locations..."
insert_vertex '{"label":"location","properties":{"id":"location_101","city":"Clementi","block":"Blk 345"}}'
insert_vertex '{"label":"location","properties":{"id":"location_102","city":"Bedok","block":"Blk 123"}}'

echo "🔹 Inserting call events + edges..."

call_data=(
  "person_1 person_2 2025-05-01-080000 2 location_101"
  "person_1 person_3 2025-05-02-081000 4 location_101"
  "person_1 person_4 2025-05-03-081100 2 location_101"
  "person_2 person_1 2025-05-03-082000 3 location_102"
  "person_3 person_5 2025-05-04-083000 5 location_102"
)

for call in "${call_data[@]}"; do
  read -r caller callee timestamp duration location_pk <<< "$call" 
  call_id="call_${caller}_${callee}_${timestamp}"

  echo "📞 Creating call: $caller → $callee @ $timestamp ($duration min) at $location_pk"

  insert_vertex "$(cat <<EOF
{
  "label": "call_event",
  "properties": {
    "id": "$call_id",
    "target_id": "$callee",     انرژی
    "timestamp": "$timestamp",
    "duration": $duration,
    "location_id": "$location_pk" 
  }
}
EOF
)"

  insert_edge "$(cat <<EOF
{
  "label": "initiated_call", 
  "outV": "$caller",
  "outVLabel": "person",
  "inV": "$call_id", 
  "inVLabel": "call_event",
  "properties": {}
}
EOF
)"

  # Edge: CallEvent --was_for--> Person (callee)
  insert_edge "$(cat <<EOF
{
  "label": "was_for", 
  "outV": "$call_id",
  "outVLabel": "call_event",
  "inV": "$callee",
  "inVLabel": "person",
  "properties": {}
}
EOF
)"

  # Edge: CallEvent --made_at--> Location
  insert_edge "$(cat <<EOF
{
  "label": "made_at",
  "outV": "$call_id",
  "outVLabel": "call_event",
  "inV": "$location_pk", 
  "inVLabel": "location",
  "properties": {}
}
EOF
)"
done

echo "✅ Done inserting data!"
