//Returns alumnus of University0

MATCH (University {uri: "http://www.University0.edu"})<-[:undergraduateDegreeFrom|:mastersDegreeFrom|:doctoralDegreeFrom]-(x)
WHERE x:AssociateProfessor OR x:AssistantProfessor OR x:FullProfessor OR x:Lecturer OR x:UndergraduateStudent OR x:GraduateStudent
RETURN x
LIMIT 1000
