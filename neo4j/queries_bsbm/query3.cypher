//Return top 10 products having productFeature1, optionally return products having ProductFeature2, PropertyNumeric1 > x, PropertyNumeric3 <y, and where product label does not exists. 

MATCH (pf1:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature85'})<-[:ns0__productFeature]-(product:ns2__ProductType1)
OPTIONAL MATCH (pf2:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1256'})<-[:ns0__productFeature]-(product:ns2__ProductType1)
WHERE product.ns0__productPropertyNumeric1>100 AND product.ns0__productPropertyNumeric3<1000
RETURN  DISTINCT  product.rdfs__label
ORDER BY product.rdfs__label 
LIMIT 10
