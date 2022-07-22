//Returns label, comment, productFeatures and other product properties of Products having comment, same producer and publisher and productFeature

MATCH (n:ns0__Product {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer7/Product285'}), 
(n:ns0__Product)-[:ns0__producer]->(p1:ns0__Producer), 
(n:ns0__Product)-[:ns1__publisher]->(p1:ns0__Producer), 
(n:ns0__Product)-[:ns0__productFeature]->(pf1:ns0__ProductFeature) 
RETURN n.rdfs__label, n.rdfs__comment, p1.rdfs__label, n.ns0__productPropertyTextual1, n.ns0__productPropertyTextual2, n.ns0__productPropertyTextual3, n.ns0__productPropertyTextual4, n.ns0__productPropertyTextual5,
p1.ns0__productPropertyNumeric1, p1.ns0__productPropertyNumeric2, p1.ns0__productPropertyNumeric4, pf1.rdfs__label
LIMIT 25
