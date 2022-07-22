MATCH (r)-[:ns0__hasWorkorder]->(w:ns0__Workorder) 
WHERE (w.ns0__open = 'True') AND (r:ns0__Robot OR r:ns0__Robot_ACME OR r:ns0__Robot_Wayne OR r:ns0__Robot_Humanitech)
RETURN r,w LIMIT 1000