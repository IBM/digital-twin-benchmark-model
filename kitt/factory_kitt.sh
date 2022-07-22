#!/bin/bash
SIZES=(2 5 10 20 50 100)
for DATASET_SIZE in ${SIZES[@]}; do
  echo "DATASIZE $DATASET_SIZE"
  VERSION='3.1.0'
  if [ ! -f "../factory_${DATASET_SIZE}.kitt.bz2" ]; then
    cd ..
    python dt_model_generator.py -f "${DATASET_SIZE}"
    bzip2 "factory_${DATASET_SIZE}.kitt"
    cd kitt
  fi

  docker-compose stop
  docker-compose rm -f
  docker-compose up -d
  sleep 90

  kitt_v3_linux -t -s iswc add --space iswc
  kitt_v3_linux -t -s iswc -l 100000 add -g "factory-${DATASET_SIZE}" -m "../factory_${DATASET_SIZE}.kitt.bz2"
  kitt_v3_linux -t -s iswc get -g "factory-${DATASET_SIZE}"  > "graph.factory.start.${VERSION}.${DATASET_SIZE}.log"
  sleep 60

  python3 LUBM_Benchmark.py -e ${KITT_URL} -u ${KITT_USR} -p ${KITT_PWD}  -t iswc -g factory-${DATASET_SIZE} -pg "2000" -q "factory_queries/" -r "500" -o "factory.${VERSION}.${DATASET_SIZE}.json"

  kitt_v3_linux -t -s iswc get -g "bsbm-${DATASET_SIZE}"  > "graph.factory.end.${VERSION}.${DATASET_SIZE}.log"
  kitt_v3_linux -t ps -r > "pstats.factory.${VERSION}.${DATASET_SIZE}.log"
  docker stats --no-stream > "stats.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose logs > "docker.factory.${VERSION}.${DATASET_SIZE}.log"
  docker-compose stop
  docker-compose rm -f
done