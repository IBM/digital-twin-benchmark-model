//Returns reviewer of ReviewXYZ

MATCH(r:ns4__Review {uri: 'http://www4.wiwiss.fu-berlin.de/bizer/bsbm/v01/instances/dataFromRatingSite1/Review8'})-[:ns4__reviewer]-(p:ns3__Person)
RETURN p.uri
