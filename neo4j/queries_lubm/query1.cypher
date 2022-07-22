//Returns all Graduate students who have taken course GraduateCourse0

MATCH (x:GraduateStudent)-[:takesCourse]->({uri: "http://www.Department0.University0.edu/GraduateCourse0"}) 
RETURN x 
LIMIT 1000
