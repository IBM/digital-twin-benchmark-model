#!/bin/bash
SIZES=(2000 5000 10000 20000 50000 100000)
for DATASET_SIZE in ${SIZES[@]}; do
  #DATASET_SIZE=50000 # number of products in the dataset. There is around 350 triples generated by product.
  PARALLELISM=16
  VERSION="7.2.2"
  #if [ ! -f "../bsbm-tools/explore-${DATASET_SIZE}.ttl" ]; then
    cd ../bsbm-tools
    rm -rf td_data
    ./generate -fc -pc ${DATASET_SIZE} -s ttl -fn "explore-${DATASET_SIZE}" -ud -ufn "explore-update-${DATASET_SIZE}"
    mv td_data td_data-${DATASET_SIZE}
    cd ../virtuoso
  #fi

  rm -rf db
  mkdir -p db/toLoad
  cp "../bsbm-tools/explore-${DATASET_SIZE}.ttl" "db/toLoad/dataset.ttl"
  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep 300

  curl -X POST "http://localhost:8890/sparql" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept:application/sparql-results+json" \
    --data-urlencode 'format=json' \
    --data-urlencode 'query=SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o }' > "graph.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"

  cd ../bsbm-tools
  rm -rf td_data
  cp td_data-${DATASET_SIZE} td_data
  ./testdriver -mt ${PARALLELISM} -ucf usecases/explore/sparql.txt -o "../virtuoso/bsbm.explore.virtuoso.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.xml" 'http://localhost:8890/sparql'
  # ./testdriver -mt ${PARALLELISM} -ucf usecases/exploreAndUpdate/sparql.txt -o "../virtuoso/bsbm.exploreAndUpdate.virtuoso.${DATASET_SIZE}.${PARALLELISM}.${PARALLELISM}.${VERSION}.xml" 'http://localhost:8890/sparql?graph-uri=urn:graph:test' -u 'http://dba:dba@localhost:8890/sparql-auth?graph-uri=urn:graph:test' -udataset "explore-update-${DATASET_SIZE}.nt"
  # ./testdriver -mt ${PARALLELISM} -ucf usecases/businessIntelligence/sparql.txt -o "../virtuoso/bsbm.businessIntelligence.virtuoso.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.xml" 'http://localhost:8890/sparql?graph-uri=urn:graph:test'
  cd ../virtuoso

  docker stats --no-stream > "stats.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"
  docker-compose logs > "docker.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"
  docker-compose stop
  docker-compose rm -f

  rm -rf db
done