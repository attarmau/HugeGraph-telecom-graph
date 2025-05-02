schema.propertyKey("name").asText().ifNotExist().create()
schema.propertyKey("phone").asText().ifNotExist().create()
schema.propertyKey("timestamp").asText().ifNotExist().create()
schema.propertyKey("duration").asInt().ifNotExist().create()
schema.propertyKey("city").asText().ifNotExist().create()
schema.propertyKey("block").asText().ifNotExist().create()

schema.vertexLabel("person").properties("name", "phone").primaryKeys("phone").ifNotExist().create()
schema.vertexLabel("call").properties("timestamp", "duration").ifNotExist().create()
schema.vertexLabel("location").properties("city", "block").primaryKeys("city", "block").ifNotExist().create()

schema.edgeLabel("call").sourceLabel("person").targetLabel("person")
      .properties("timestamp", "duration").multiplicity("MULTI").ifNotExist().create()

schema.edgeLabel("made_at").sourceLabel("call").targetLabel("location")
      .multiplicity("ONE2ONE").ifNotExist().create()
