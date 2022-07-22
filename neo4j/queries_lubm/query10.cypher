//Return all students who've taken course GraduateCourse0

MATCH ( {uri: "http://www.Department0.University0.edu/GraduateCourse0"})<-[:takesCourse]-(x) 
WHERE (x:UndergraduateStudent OR x:GraduateStudent)
RETURN x
LIMIT 1000
