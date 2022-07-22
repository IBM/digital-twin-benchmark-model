//Return chairman, department wise for University0 

MATCH (a:University {uri: "http://www.University0.edu"})<-[:subOrganizationOf]-(y:Department)<-[:headOf]-(x)
WHERE x:AssociateProfessor OR x:AssistantProfessor OR x:FullProfessor
RETURN x
LIMIT 1000
