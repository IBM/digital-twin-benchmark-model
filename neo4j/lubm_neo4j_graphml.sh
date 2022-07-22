#!/bin/bash

SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  PARALLELISM=16
  VERSION="4.4.5"
  if [ ! -f "../lubm-tools/Universities-${DATASET_SIZE}.graphml" ]; then
    cd ../lubm-tools
    ./generate.sh --quiet --timing -u "${DATASET_SIZE}" --format NEO4J_GRAPHML --consolidate Full --threads "${PARALLELISM}"
    mv "Universities.graphml" "Universities-${DATASET_SIZE}.graphml"
    cd ../neo4j
  fi

  rm -rf td_data
  mkdir td_data
  cp "../lubm-tools/Universities-${DATASET_SIZE}.graphml" "./td_data/dataset.graphml"

  docker-compose up -d
  sleep 60

  # curl http://localhost:7474/rdf/ping
  curl -X POST -H 'Content-type: application/json' http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CALL apoc.import.graphml(\"/td_data/dataset.graphml\", {readLabels: true})"}]}' -v


  python3 ../LUBM_Benchmark.py -l "cypher" -e "bolt://localhost:7687/" -q "queries_lubm/" -r "500" -o "lubm.${VERSION}.${DATASET_SIZE}.json"

  docker stats --no-stream > "stats.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f

  rm -rf td_data
done