#!/bin/bash
SIZES=(100)
for DATASET_SIZE in ${SIZES[@]}; do
  echo "DATASIZE $DATASET_SIZE"
  VERSION="9.10.0"
  if [ ! -f "../factory_${DATASET_SIZE}.ttl" ]; then
    cd ..
    python dt_model_generator.py -f "${DATASET_SIZE}"
    bzip2 "factory_${DATASET_SIZE}.kitt"
    cd virtuoso
  fi

  let SLP=$DATASET_SIZE*1+30
  echo "Sleep $SLP"

  rm -rf db
  mkdir -p db/toLoad
  cp "../factory_${DATASET_SIZE}.ttl" "db/toLoad/dataset.ttl"
  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep "$SLP"

#  curl --digest --user dba:dba --verbose --url "http://localhost:8890/sparql-graph-crud-auth?graph-uri=urn:graph:update:test:put" -T "../factory_${DATASET_SIZE}.ttl"

  docker exec -it virtuoso_bsbm-virtuoso-benchmark_1 isql-v -U dba -P dba exec="rdfs_rule_set ('http://www.w3.org/2002/07/owl#', 'http://bsbm/');"
  docker exec -it virtuoso_bsbm-virtuoso-benchmark_1 isql-v -U dba -P dba exec="SELECT * FROM DB.DBA.SYS_RDF_SCHEMA"

  curl -X POST "http://localhost:8890/sparql" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept:application/sparql-results+json" \
    --data-urlencode 'format=json' \
    --data-urlencode 'query=SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o }' > "graph.factory.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"

  python3 ../LUBM_Benchmark.py -e "http://localhost:8890/sparql" -q "factory_queries/" -r "500" -o "factory.${VERSION}.${DATASET_SIZE}.json"

  docker stats --no-stream > "stats.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f

  rm -rf db
done