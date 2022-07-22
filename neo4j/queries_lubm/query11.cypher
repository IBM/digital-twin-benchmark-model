//Return all Research Groups which are sub-organization of University0

MATCH (a:University {uri: "http://www.University0.edu"})<-[:subOrganizationOf*]-(x:ResearchGroup)
RETURN x
LIMIT 1000
