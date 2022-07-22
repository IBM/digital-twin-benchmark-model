#!/bin/bash
SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  VERSION="9.10.0"
  if [ ! -f "../lubm-tools/Universities2-${DATASET_SIZE}.ttl" ]; then
    cd ../lubm-tools
    ./generate.sh --quiet --timing -u "${DATASET_SIZE}" --format TURTLE --consolidate Full --threads 1
    mv "Universities-1.ttl" "Universities2-${DATASET_SIZE}.ttl"
    python3 ../fix_lubm.py -i "Universities2-${DATASET_SIZE}.ttl"
    cat university-bench.ttl >> "Universities2-${DATASET_SIZE}.ttl"
    cd ../graphdb
  fi

  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep 10

  curl -f -X POST http://localhost:7200/rest/repositories -H 'Content-Type:application/json' -d '{"id":"test","params":{"ruleset":{"label":"Ruleset","name":"ruleset","value":"rdfsplus-optimized"},"title":{"label":"Repository title","name":"title","value":"GraphDB Free repository"},"checkForInconsistencies":{"label":"Check for inconsistencies","name":"checkForInconsistencies","value":"false"},"disableSameAs":{"label":"Disable owl:sameAs","name":"disableSameAs","value":"true"},"baseURL":{"label":"Base URL","name":"baseURL","value":"http://example.org/graphdb#"},"repositoryType":{"label":"Repository type","name":"repositoryType","value":"file-repository"},"id":{"label":"Repository ID","name":"id","value":"repo-test"},"storageFolder":{"label":"Storage folder","name":"storageFolder","value":"storage"}},"title":"Test","type":"free"}';
  sleep 10
  curl -f -X PUT -H 'Content-Type:application/x-turtle' -T "../lubm-tools/Universities2-${DATASET_SIZE}.ttl" http://localhost:7200/repositories/test/statements
  #curl -f -X PUT -H 'Content-Type:application/n-triples' -T "../lubm-tools/Universities-${DATASET_SIZE}.nt" http://localhost:7200/repositories/test/statements
  sleep 30

  curl -X POST "http://localhost:7200/repositories/test" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept:application/sparql-results+json" \
    --data-urlencode 'format=json' \
    --data-urlencode 'query=SELECT (COUNT(*) as ?Triples) WHERE { ?s ?p ?o }' > "graph.lubm.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"

  python3 ../LUBM_Benchmark.py -e "http://localhost:7200/repositories/test" -q "lubm_queries/" -r "500" -o "lubm.${VERSION}.${DATASET_SIZE}.json"

  docker stats --no-stream > "stats.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f
done