//Returns all students who've taken a course taught by Associate Professsor of Department0 of University0

MATCH (:AssociateProfessor {uri: "http://www.Department0.University0.edu/AssociateProfessor0"})-[:teacherOf]->(y)<-[:takesCourse]-(x)
WHERE (x:UndergraduateStudent OR x:GraduateStudent) AND (y:Course OR y:GraduateCourse)
RETURN x, y
LIMIT 1000
