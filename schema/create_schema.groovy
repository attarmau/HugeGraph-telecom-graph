// ==== Property Keys ====
schema.propertyKey("id").asText().ifNotExist().create()
schema.propertyKey("target_id").asText().ifNotExist().create() // Property for the callee on call_event
schema.propertyKey("name").asText().ifNotExist().create()
schema.propertyKey("phone").asText().ifNotExist().create()
schema.propertyKey("timestamp").asText().ifNotExist().create()
schema.propertyKey("duration").asInt().ifNotExist().create()
schema.propertyKey("city").asText().ifNotExist().create()
schema.propertyKey("block").asText().ifNotExist().create()
// schema.propertyKey("location_id").asText().ifNotExist().create() // No longer primary, just a property if needed, or use "id" for location PK

// ==== Vertex Labels ====

// Person vertex (caller or callee)
schema.vertexLabel("person")
      .properties("id", "name", "phone")
      .primaryKeys("id") // Stays the same, this is correct
      .ifNotExist().create()

// Location vertex (place where call happened)
schema.vertexLabel("location")
      .properties("id", "city", "block") // Use "id" as the PK property name
      .primaryKeys("id")                 // Use "id" as the PK
      .ifNotExist().create()

// Call event vertex (timestamped communication)
schema.vertexLabel("call_event")
      // "id" will be like "call_person_1_person_2_2025-05-01-080000"
      .properties("id", "target_id", "timestamp", "duration", "location_id") // "location_id" here is the foreign key string
      .primaryKeys("id") // Simplified to use the unique ID string you generate
      .ifNotExist().create()

// ==== Edge Labels ====

// Person initiated a call_event
schema.edgeLabel("initiated_call")
      .sourceLabel("person")
      .targetLabel("call_event")
      // No properties needed here if they are on call_event
      .ifNotExist().create()

// call_event was directed to a person (callee)
schema.edgeLabel("was_for") // Or "has_recipient", "targets_person", etc.
      .sourceLabel("call_event")
      .targetLabel("person")
      .ifNotExist().create()

// Where the call was made (call_event to location)
schema.edgeLabel("made_at")
      .sourceLabel("call_event")
      .targetLabel("location")
      .ifNotExist().create()

// ==== Indexes (optional but recommended) ====
schema.indexLabel("personByPhone").onV("person").by("phone").ifNotExist().create()
schema.indexLabel("callByTimestamp").onV("call_event").by("timestamp").ifNotExist().create()
