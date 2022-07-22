//Returns Students who've taken course of their faculty advisor.

MATCH (x)-[:advisor]->(z)-[:teacherOf]->(y)<-[:takesCourse]-(x)
WHERE (x:UndergraduateStudent OR x:GraduateStudent) AND (y:Course OR y:GraduateCourse) AND (z:Lecturer OR z:AssociateProfessor OR z:AssistantProfessor OR z:FullProfessor)
RETURN x, y, z
LIMIT 1000
