'use strict';

const db = require('@arangodb').db;
const fs = require('fs');
const path = '/import/data_json';

// Load helper function
function loadJSON(file) {
  const content = fs.read(`${path}/${file}`);
  return JSON.parse(content);
}

// Insert documents into a collection
function insertDocuments(collectionName, documents) {
  const collection = db._collection(collectionName);
  if (!collection) {
    throw new Error(`Collection ${collectionName} does not exist`);
  }

  documents.forEach(doc => {
    try {
      collection.insert(doc);
    } catch (e) {
      print(`Error inserting into ${collectionName}:`, JSON.stringify(doc), e.message);
    }
  });
}

// Load and insert vertices
const personDocs = loadJSON('person.json');
insertDocuments('person', personDocs);

const locationDocs = loadJSON('location.json');
insertDocuments('location', locationDocs);

const callEventDocs = loadJSON('call_event.json');
insertDocuments('call_event', callEventDocs);

// Load and insert edges
const calledEdges = loadJSON('called.json');
insertDocuments('called', calledEdges);

const madeAtEdges = loadJSON('made_at.json');
insertDocuments('made_at', madeAtEdges);

print("✅ Data loading complete.");
