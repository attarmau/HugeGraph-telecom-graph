// Property Keys
schema.propertyKey("id").asText().ifNotExist().create()             // UUID or text-safe
schema.propertyKey("target_id").asText().ifNotExist().create()
schema.propertyKey("name").asText().ifNotExist().create()
schema.propertyKey("phone").asText().ifNotExist().create()
schema.propertyKey("timestamp").asText().ifNotExist().create()
schema.propertyKey("duration").asInt().ifNotExist().create()
schema.propertyKey("city").asText().ifNotExist().create()
schema.propertyKey("block").asText().ifNotExist().create()
schema.propertyKey("location_id").asText().ifNotExist().create()

// Vertex Labels
schema.vertexLabel("person")
      .properties("id", "name", "phone")
      .primaryKeys("id")  // or "phone" if more reliable
      .ifNotExist().create()

schema.vertexLabel("call_event")
      .properties("id", "target_id", "timestamp", "duration", "location_id")
      .primaryKeys("id", "target_id", "timestamp")
      .ifNotExist().create()

schema.vertexLabel("location")
      .properties("id", "city", "block")
      .primaryKeys("id")
      .ifNotExist().create()

// Edge Labels
schema.edgeLabel("called")
      .sourceLabel("person")
      .targetLabel("person")
      .properties("timestamp", "duration")
      .multiplicity("MULTI")
      .ifNotExist().create()

schema.edgeLabel("made_at")
      .sourceLabel("call_event")
      .targetLabel("location")
      .multiplicity("ONE2ONE")
      .ifNotExist().create()

// Indexes (for efficient lookups)
schema.indexLabel("personByPhone")
      .onV("person")
      .by("phone")
      .ifNotExist().create()

schema.indexLabel("callByTimestamp")
      .onV("call_event")
      .by("timestamp")
      .ifNotExist().create()
