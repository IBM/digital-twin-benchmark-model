#!/bin/bash
SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  VERSION="9.10.0"
  if [ ! -f "../factory_${DATASET_SIZE}.ttl" ]; then
    cd ..
    python dt_model_generator.py -f "${DATASET_SIZE}"
    cd neo4j
  fi

  rm -rf td_data
  mkdir td_data
  cp "../factory_${DATASET_SIZE}.ttl" "td_data/dataset.ttl"

  docker-compose -f docker-compose_bsbm.yaml stop
  docker-compose -f docker-compose_bsbm.yaml rm -f
  docker-compose -f docker-compose_bsbm.yaml up -d
  sleep 120
  
  curl -X POST -H 'Content-type: application/json' -H "Accept: application/json" http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CALL n10s.graphconfig.init();"}]}'
  curl -X POST -H 'Content-type: application/json' -H "Accept: application/json" http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;"}]}'
  curl -X POST -H 'Content-type: application/json' -H "Accept: application/json" http://localhost:7474/db/data/transaction/commit -d '{"statements": [{"statement": "CALL n10s.rdf.import.fetch(\"file:///td_data/dataset.ttl\",\"Turtle\");"}]}'
  sleep 10

  python3 ../LUBM_Benchmark.py -l "cypher" -e "bolt://localhost:7687/" -q "queries_factory/" -r "500" -o "factory.${VERSION}.${DATASET_SIZE}.json"

  docker stats --no-stream > "stats.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose -f docker-compose_bsbm.yaml logs > "docker.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose -f docker-compose_bsbm.yaml stop
  docker-compose -f docker-compose_bsbm.yaml rm -f

  rm -rf td_data
done