//Returns top 5 products and their labels having productFeature where conditions mentioned in the query satisfy and product not same as product ProductXYZ 

MATCH (product:ns2__ProductType1)-[:ns0__productFeature]-(pf1:ns0__ProductFeature), (orig:ns0__Product {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer7/Product285'})-[:ns0__productFeature]-(pf1:ns0__ProductFeature)
WHERE NOT NOT(product.uri = 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromProducer7/Product285')
  AND product.ns0__productPropertyNumeric1 < orig.ns0__productPropertyNumeric1 + 120 
  AND product.ns0__productPropertyNumeric1 > orig.ns0__productPropertyNumeric1 - 120  
  AND product.ns0__productPropertyNumeric2 < orig.ns0__productPropertyNumeric2 + 170  
  AND product.ns0__productPropertyNumeric2 > orig.ns0__productPropertyNumeric2 - 170 
RETURN  DISTINCT  product.rdfs__label
ORDER BY product.rdfs__label 
LIMIT 5
