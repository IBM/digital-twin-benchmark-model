// Return top 10 product and their labels having ProductFeature1 and ProductFeature2 where productPropertyNumeric1 >x
// MATCH(product:ns2__ProductType1)-[:ns0__productFeature]-(pf1:ns0__ProductFeature}),(product:ns2__ProductType1)-[:ns0__productFeature]-(pf2:ns0__ProductFeature}) 

MATCH (pf1:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature85'})<-[:ns0__productFeature]-(product:ns2__ProductType1),(pf2:ns0__ProductFeature {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/ProductFeature1256'})<-[:ns0__productFeature]-(product:ns2__ProductType1) 
WHERE product.ns0__productPropertyNumeric1>100
RETURN  DISTINCT  product, pf1, pf2
ORDER BY product
LIMIT 10