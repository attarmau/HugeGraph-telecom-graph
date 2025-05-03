// Connect to default _system database
const db = require("@arangodb").db;
const graph_module = require("@arangodb/general-graph");

const GRAPH_NAME = "telecom_graph";

// 1. Create Vertex Collections
const vertexCollections = ["person", "call_event", "location"];
vertexCollections.forEach((vc) => {
  if (!db._collection(vc)) {
    db._createDocumentCollection(vc);
  }
});

// 2. Create Edge Collections
const edgeDefinitions = [
  {
    collection: "called",
    from: ["person"],
    to: ["person"],
  },
  {
    collection: "made_at",
    from: ["call_event"],
    to: ["location"],
  },
];

// Create edge collections if not exist
edgeDefinitions.forEach((edge) => {
  if (!db._collection(edge.collection)) {
    db._createEdgeCollection(edge.collection);
  }
});

// 3. Create Graph
if (!graph_module._exists(GRAPH_NAME)) {
  graph_module._create(
    GRAPH_NAME,
    edgeDefinitions,
    []
  );
}
