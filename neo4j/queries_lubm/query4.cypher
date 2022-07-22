//Returns a Professor having name Y1, email Y2 and telephone Y3, and who works for Department0 of University0.

MATCH (x)-[:worksFor]->( {uri: "http://www.Department0.University0.edu"})
WHERE x:AssociateProfessor OR x:AssistantProfessor OR x:FullProfessor
RETURN x, x.name, x.telephone, x.emailAddress
LIMIT 1000
