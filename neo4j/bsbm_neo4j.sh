#!/bin/bash
SIZES=(2000 5000 10000 20000 50000 100000)
#export DATASET_SIZE=2000
for DATASET_SIZE in ${SIZES[@]}; do
  PARALLELISM=16
  VERSION="4.4.5"
  if [ ! -f "../bsbm-tools/explore-${DATASET_SIZE}.ttl" ]; then
    cd ../bsbm-tools
    rm -rf td_data
    ./generate -fc -pc ${DATASET_SIZE} -s ttl -fn "explore-${DATASET_SIZE}" -ud -ufn "explore-update-${DATASET_SIZE}"
    mv td_data td_data-${DATASET_SIZE}
    cd ../kitt
  fi

  rm -rf td_data
  mkdir td_data
  cp "../bsbm-tools/explore-${DATASET_SIZE}.ttl" "td_data/dataset.ttl"

  docker-compose -f docker-compose_bsbm.yaml stop
  docker-compose -f docker-compose_bsbm.yaml rm -f
  docker-compose -f docker-compose_bsbm.yaml up -d
  sleep 120

  curl http://localhost:7474/rdf/ping
  curl -X POST -H 'Content-type: application/json' http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CALL n10s.graphconfig.init();"}]}'
  curl -X POST -H 'Content-type: application/json' http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;"}]}'
  curl -X POST -H 'Content-type: application/json' http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CALL n10s.rdf.import.fetch(\"file:///td_data/dataset.ttl\",\"Turtle\");"}]}'
  sleep 120

  python3 ../LUBM_Benchmark.py -l "cypher" -e "bolt://localhost:7687/" -q "queries_bsbm/" -r "500" -o "bsbm.explore.neo4j.${VERSION}.${DATASET_SIZE}.json"

  docker stats --no-stream > "stats.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f

  rm -rf td_data
done