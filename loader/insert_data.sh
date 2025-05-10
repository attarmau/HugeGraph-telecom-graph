GRAPH_URL="http://localhost:8080/graphs/hugegraph"

echo "🔹 Inserting persons..."
tail -n +2 person.csv | while IFS=',' read -r id name phone; do
  curl -s -X POST "$GRAPH_URL/graph/vertices" -H "Content-Type: application/json" -d "{
    \"label\": \"person\",
    \"properties\": {
      \"id\": \"$id\",
      \"name\": \"$name\",
      \"phone\": \"$phone\"
    }
  }"
done

echo "🔹 Inserting locations..."
tail -n +2 location.csv | while IFS=',' read -r id city block; do
  curl -s -X POST "$GRAPH_URL/graph/vertices" -H "Content-Type: application/json" -d "{
    \"label\": \"location\",
    \"properties\": {
      \"id\": \"$id\",
      \"city\": \"$city\",
      \"block\": \"$block\"
    }
  }"
done

echo "🔹 Inserting call events + edges..."
tail -n +2 call.csv | while IFS=',' read -r caller_id target_id timestamp duration location_id; do
  # Generate unique call_event_id
  call_event_id="${caller_id}_${target_id}_${timestamp}"

  curl -s -X POST "$GRAPH_URL/graph/vertices" -H "Content-Type: application/json" -d "{
    \"label\": \"call_event\",
    \"properties\": {
      \"id\": \"$call_event_id\",
      \"target_id\": \"$target_id\",
      \"timestamp\": \"$timestamp\",
      \"duration\": $duration,
      \"location_id\": \"$location_id\"
    }
  }"

  curl -s -X POST "$GRAPH_URL/graph/edges" -H "Content-Type: application/json" -d "{
    \"label\": \"called\",
    \"outV\": \"$caller_id\",
    \"outVLabel\": \"person\",
    \"inV\": \"$target_id\",
    \"inVLabel\": \"person\",
    \"properties\": {
      \"timestamp\": \"$timestamp\",
      \"duration\": $duration
    }
  }"

  curl -s -X POST "$GRAPH_URL/graph/edges" -H "Content-Type: application/json" -d "{
    \"label\": \"made_at\",
    \"outV\": \"$call_event_id\",
    \"outVLabel\": \"call_event\",
    \"inV\": \"$location_id\",
    \"inVLabel\": \"location\"
  }"
done

echo "✅ Done inserting data!"
