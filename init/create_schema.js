// Connect to default _system database
const db = require("@arangodb").db;
const graph_module = require("@arangodb/general-graph");

const GRAPH_NAME = "telecom_graph";

// 1. Create Vertex Collections
const vertexCollections = ["person", "call_event", "location"];
vertexCollections.forEach((vc) => {
  if (!db._collection(vc)) {
    db._createDocumentCollection(vc);
    print(`Created vertex collection: ${vc}`);
  } else {
    print(`Vertex collection already exists: ${vc}`);
  }
});

// 2. Create Edge Collections
const edgeCollections = ["called", "made_at"];
edgeCollections.forEach((ec) => {
  if (!db._collection(ec)) {
    db._createEdgeCollection(ec);
    print(`Created edge collection: ${ec}`);
  } else {
    print(`Edge collection already exists: ${ec}`);
  }
});

// 3. Define Edge Relations for the Graph
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

// 4. Create the Graph
if (!graph_module._exists(GRAPH_NAME)) {
  graph_module._create(
    GRAPH_NAME,
    edgeDefinitions,
    []
  );
  print(`Graph '${GRAPH_NAME}' created.`);
} else {
  print(`Graph '${GRAPH_NAME}' already exists.`);
}
