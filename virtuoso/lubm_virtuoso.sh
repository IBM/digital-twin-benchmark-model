#!/bin/bash

SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  VERSION="7.2.2"
  if [ ! -f "../lubm-tools/Universities2-${DATASET_SIZE}.ttl" ]; then
    cd ../lubm-tools
    ./generate.sh --quiet --timing -u "${DATASET_SIZE}" --format TURTLE --consolidate Full --threads 1
    mv "Universities-1.ttl" "Universities2-${DATASET_SIZE}.ttl"
    python3 ../fix_lubm.py -i "Universities2-${DATASET_SIZE}.ttl"
    cat university-bench.ttl >> "Universities2-${DATASET_SIZE}.ttl"
    cd ../virtuoso
  fi

  rm -rf db
  mkdir -p db/toLoad
  cp "../lubm-tools/Universities2-${DATASET_SIZE}.ttl" "db/toLoad/dataset.ttl"
  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep 300

  curl -X POST "http://localhost:8890/sparql" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept:application/sparql-results+json" \
    --data-urlencode 'format=json' \
    --data-urlencode 'query=SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o }' > "graph.lubm.${VERSION}.${DATASET_SIZE}.log"

  python3 ../LUBM_Benchmark.py -e "http://localhost:8890/sparql" -q "lubm_queries/" -r "500" -o "lubm.${VERSION}.${DATASET_SIZE}.json"
  docker stats --no-stream > "stats.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f
done