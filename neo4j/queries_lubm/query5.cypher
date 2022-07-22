//Returns all members of Department0 of University0

MATCH (x)-[:memberOf|:worksFor|:headOf]->(:Department {uri: "http://www.Department0.University0.edu"})
WHERE x:AssociateProfessor OR x:AssistantProfessor OR x:FullProfessor OR x:Lecturer OR x:UndergraduateStudent OR x:GraduateStudent
RETURN x
LIMIT 1000
