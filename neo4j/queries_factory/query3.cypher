MATCH (f:ns0__Factory)-[:ns0__hasJoint|ns0__hasArm|ns0__hasBelt|ns0__hasRobot|ns0__hasLine*1..10]->(r) 
WHERE (r:ns0__Robot OR r:ns0__Robot_ACME OR r:ns0__Robot_Wayne OR r:ns0__Robot_Humanitech)
RETURN f,r LIMIT 1000