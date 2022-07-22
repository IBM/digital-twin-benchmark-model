//Find products matching two different set of features
//After union of two queries return 10 results after skipping first 10
//Query 1: Return products and their labels having ProductFeature1 and ProductFeature2 where productPropertyNumeric1 > x
//Query 2: Return products and their labels having ProductFeature1 and ProductFeature3 where productPropertyNumeric2 > y

MATCH (pf1:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature85'})<-[:ns0__productFeature]-(product:ns2__ProductType1),(pf2:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1256'})<-[:ns0__productFeature]-(product:ns2__ProductType1) 
WHERE product.ns0__productPropertyNumeric1>100
RETURN  DISTINCT  product.rdfs__label
UNION
MATCH (pf1:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature85'})<-[:ns0__productFeature]-(product:ns2__ProductType1),(pf2:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature7212'})<-[:ns0__productFeature]-(product:ns2__ProductType1)
WHERE product.ns0__productPropertyNumeric1>100
RETURN  DISTINCT  product.rdfs__label
ORDER BY product.rdfs__label 
LIMIT 10
