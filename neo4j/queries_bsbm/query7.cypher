//Return product label, price, vendor title, review title, rating 1, rating 2 where country in list ['India','Argentina']  optionally match other products satisfying conditions in optional match clause.

MATCH (n:ns0__Product {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer7/Product285'})
OPTIONAL MATCH(X:ns0__Offer)-[:ns0__product]-(n:ns0__Product), 
(X:ns0__Offer)-[:ns1__publisher]-(Z), 
(Y:ns4__Review)-[:ns0__reviewFor]-(n:ns0__Product),
(Y:ns4__Review)-[:ns4__reviewer]-(P:ns3__Person)  
WHERE  X.ns0__validTo >= "2008-01-01T00:00:00"
RETURN n.uri, n.rdfs__label, X.ns0__validFrom, X.uri, Y.ns1_title, Y.ns0__reviewDate, Y.uri, P.ns3__name, Z.uri, Z.rdfs__label, Y.ns0__rating1, Y.ns0__rating2
