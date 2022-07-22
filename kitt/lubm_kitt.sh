#!/bin/bash

SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  VERSION='3.1.0'
  if [ ! -f "../lubm-tools/Universities2-${DATASET_SIZE}.ttl" ]; then
    cd ../lubm-tools
    ./generate.sh --quiet --timing -u "${DATASET_SIZE}" --format TURTLE --consolidate Full --threads 1
    mv "Universities-1.ttl" "Universities2-${DATASET_SIZE}.ttl"
    python3 ../fix_lubm.py -i "Universities2-${DATASET_SIZE}.ttl"
    cat university-bench.ttl >> "Universities2-${DATASET_SIZE}.ttl"
    cd ../kitt
  fi

  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep 120

  if [ ! -f "Universities2-${DATASET_SIZE}.kitt.bz2" ]; then
    python3 ../import_lubm_rdf.py -i "../lubm-tools/Universities2-${DATASET_SIZE}.ttl" -o "Universities2-${DATASET_SIZE}.kitt.bz2" -f turtle -ps 20000
  fi

  kitt_v3_linux -t -s iswc add --space iswc
  kitt_v3_linux -t -s iswc -l 100000 add -g "lubm-${DATASET_SIZE}" -m "Universities2-${DATASET_SIZE}.kitt.bz2"
  kitt_v3_linux -t -s iswc get -g "lubm-${DATASET_SIZE}"  > "graph.lubm.${VERSION}.${DATASET_SIZE}.log"
  sleep 60

  python3 LUBM_Benchmark.py -e ${KITT_URL} -u ${KITT_USR} -p ${KITT_PWD}  -t iswc -g lubm-${DATASET_SIZE} -pg "2000" -q "lubm_queries/" -r "500" -o "lubm.${VERSION}.${DATASET_SIZE}.json"

  kitt_v3_linux -t ps -r > "pstats.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker stats --no-stream > "stats.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.lubm.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f
done