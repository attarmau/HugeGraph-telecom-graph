graph.addVertex(T.label, 'person', 'id', 'person_1', 'name', 'Alice', 'phone', '9781-1234')
graph.addVertex(T.label, 'person', 'id', 'person_2', 'name', 'Bob', 'phone', '9455-6789')
graph.addVertex(T.label, 'person', 'id', 'person_3', 'name', 'Catherine', 'phone', '9123-4567')

graph.addVertex(T.label, 'location', 'id', 'loc_1', 'city', 'Singapore', 'block', 'Clementi')
graph.addVertex(T.label, 'location', 'id', 'loc_2', 'city', 'Singapore', 'block', 'Orchard')

graph.addVertex(T.label, 'call_event',
    'id', 'person_1',
    'target_id', 'person_2',
    'timestamp', '2025-05-05T08:00:00',
    'duration', 120,
    'location_id', 'loc_1')

graph.addVertex(T.label, 'call_event',
    'id', 'person_2',
    'target_id', 'person_3',
    'timestamp', '2025-05-06T10:30:00',
    'duration', 90,
    'location_id', 'loc_2')

g.V().has('person', 'id', 'person_1')
 .as('a')
 .V().has('person', 'id', 'person_2')
 .addE('called').from('a')
 .property('timestamp', '2025-05-05T08:00:00')
 .property('duration', 120)
 .iterate()

g.V().has('person', 'id', 'person_2')
 .as('a')
 .V().has('person', 'id', 'person_3')
 .addE('called').from('a')
 .property('timestamp', '2025-05-06T10:30:00')
 .property('duration', 90)
 .iterate()

g.V().has('call_event', 'id', 'person_1')
 .has('target_id', 'person_2')
 .has('timestamp', '2025-05-05T08:00:00')
 .as('e')
 .V().has('location', 'id', 'loc_1')
 .addE('made_at').from('e')
 .iterate()

g.V().has('call_event', 'id', 'person_2')
 .has('target_id', 'person_3')
 .has('timestamp', '2025-05-06T10:30:00')
 .as('e')
 .V().has('location', 'id', 'loc_2')
 .addE('made_at').from('e')
 .iterate()
