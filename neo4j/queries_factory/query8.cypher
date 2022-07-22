MATCH (d:ns0__Data_State)<-[:hasData|:ns0__hasWorkorder|ns1__hasFile|ns1__hasJson|ns1__hasSeries]-(a) 
WHERE (a:ns0__Robot OR a:ns0__Robot_ACME OR a:ns0__Robot_Wayne OR a:ns0__Robot_Humanitech OR a:ns0__Belt OR a:ns0__Robot_Arm OR a:ns0__Robot_Tool OR a:ns0__Robot_Joint OR a:ns0__Machine)
RETURN properties(a),properties(d) LIMIT 1000