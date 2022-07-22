#!/bin/bash
SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  echo "DATASIZE $DATASET_SIZE"
  VERSION="9.10.0"
  if [ ! -f "../factory_${DATASET_SIZE}.ttl" ]; then
    cd ..
    python dt_model_generator.py -f "${DATASET_SIZE}"
    bzip2 "factory_${DATASET_SIZE}.kitt"
    cd blazegraph
  fi

  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep 30

  curl -f -X POST -H 'Content-Type:text/turtle' -T "../factory_${DATASET_SIZE}.ttl" http://localhost:8889/blazegraph/sparql
  sleep 60

  curl -X POST "http://localhost:8889/blazegraph/sparql" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept:application/sparql-results+json" \
    --data-urlencode 'format=json' \
    --data-urlencode 'query=SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o }' > "graph.factory.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"

  python3 ../LUBM_Benchmark.py -e "http://localhost:8889/blazegraph/sparql" -u "http://localhost:8889/blazegraph/namespace/kb/update" -q "factory_queries/" -r "500" -o "factory.${VERSION}.${DATASET_SIZE}.json"

  docker stats --no-stream > "stats.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f
done
