MATCH (dIN:ns0__Data_Power)<-[:hasData|ns0__hasWorkorder|ns1__hasFile|ns1__hasJson|ns1__hasSeries]-(a)<-[:ns0__hasJoint|ns0__hasArm|ns0__hasBelt|ns0__hasRobot|ns0__hasLine]-(l)
WHERE (a:ns0__Robot OR a:ns0__Robot_ACME OR a:ns0__Robot_Wayne OR a:ns0__Robot_Humanitech OR a:ns0__Belt OR a:ns0__Robot_Arm OR a:ns0__Robot_Tool OR a:ns0__Robot_Joint OR a:ns0__Machine) AND (l:ns0__Line OR l:ns0__Factory)
MERGE (l)-[:hasData]->(dp:ns0__Data_Power_Agg)<-[:ns1__hasOutputData]-(f:ns0__Function_Agg)-[:ns1__hasInputData]->(dIN)
RETURN count(*)