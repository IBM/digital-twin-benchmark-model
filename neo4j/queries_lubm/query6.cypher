//Returns all students

MATCH (x)
WHERE x:UndergraduateStudent OR x:GraduateStudent
RETURN x
LIMIT 1000
