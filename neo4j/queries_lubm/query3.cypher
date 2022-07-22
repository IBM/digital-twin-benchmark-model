//Returns the publications of AssistantProfessor0 of Department0 in University0

MATCH (x:Publication)-[:publicationAuthor]->( {uri:"http://www.Department0.University0.edu/AssistantProfessor0"}) 
RETURN x 
LIMIT 1000
