MATCH(r) 
WHERE (r:ns0__Robot OR r:ns0__Robot_ACME OR r:ns0__Robot_Wayne OR r:ns0__Robot_Humanitech) AND r.uri = "http://www.ibm.com/factory.owl#factory0_line_1_robot_0"
RETURN r