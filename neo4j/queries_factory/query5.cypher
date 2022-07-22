MATCH (r)-[:ns1__hasOutput]->(b:ns0__Belt)-[:ns1__hasInput]->(r1)-[:ns0__hasWorkorder]->(w:ns0__Workorder) 
WHERE (r:ns0__Robot OR r:ns0__Robot_ACME OR r:ns0__Robot_Wayne OR r:ns0__Robot_Humanitech) AND r.uri = "http://www.ibm.com/factory.owl#factory0_line_1_robot_0" AND (r1:ns0__Robot OR r1:ns0__Robot_ACME OR r1:ns0__Robot_Wayne OR r1:ns0__Robot_Humanitech) 
RETURN r1.uri, w.ns0__open