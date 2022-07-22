//Returns title and other information of Product  title, text, reviewDate, reviewer, and name optionally return product having rating2, rating3, rating4 and language=en order by descending order of review date

MATCH (n:ns0__Product {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer7/Product285'})<-[:ns0__reviewFor]-(Y:ns4__Review),
(Y:ns4__Review)-[:ns4__reviewer]-(P:ns3__Person)
RETURN Y.ns1_title, Y.ns1_text, Y.uri, Y.ns0__reviewDate, P.uri, P.ns3__name, Y.ns0__rating1, Y.ns0__rating2, Y.ns0__rating3, Y.ns0__rating4
LIMIT 20

