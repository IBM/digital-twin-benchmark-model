MATCH (X:ns0__Offer {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromVendor1/Offer3'})
OPTIONAL MATCH(X:ns0__Offer)-[:ns0__product]-(P:ns0__Product), 
(X:ns0__Offer)-[:ns1__publisher]-(Z) 
RETURN X, Z, P