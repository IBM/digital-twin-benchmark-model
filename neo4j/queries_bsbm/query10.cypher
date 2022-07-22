// Returns top 10 offers having vendor, price and deliveryDays where vendor.county= %CountryXYZ%, 
//offer.product = %ProductXYZ% and offer.date= %currentDate%. Order results by price.

MATCH (n:ns0__Product {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer7/Product285'})
OPTIONAL MATCH(X:ns0__Offer)-[:ns0__product]-(n:ns0__Product), 
(X:ns0__Offer)-[:ns1__publisher]-(Z) 
WHERE  X.ns0__deliveryDays < 6 AND Z.rdfs__comment =~ ".*book.*"
RETURN X.uri
ORDER BY X.ns0__price
LIMIT 10
