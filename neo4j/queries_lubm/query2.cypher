//Returns Graduate Students of a Department in a University 

MATCH (x:GraduateStudent)-[:memberOf]->(z:Department)-[:subOrganizationOf]->(y:University)<-[:undergraduateDegreeFrom]-(x)
RETURN x, y, z
LIMIT 1000
