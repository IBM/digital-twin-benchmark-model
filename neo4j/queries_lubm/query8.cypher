//Returns Students and their email addresses department wise for Univesity0

MATCH (:University {uri: "http://www.University0.edu"})<-[:subOrganizationOf]-(y:Department)<-[:memberOf]-(x)
WHERE x:UndergraduateStudent OR x:GraduateStudent
RETURN x, x.emailAddress, y
LIMIT 1000
