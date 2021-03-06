#!/bin/bash

DATASET_SIZE=10000 # number of products in the dataset. There is around 350 triples generated by product.
PARALLELISM=16
TOTAL_QUERIES_PER_QTYPE=500
VERSION='3.1.0'
if [ ! -f "../bsbm-tools/explore-${DATASET_SIZE}.ttl" ]; then
  cd ../bsbm-tools
  rm -rf td_data
  ./generate -fc -pc ${DATASET_SIZE} -s ttl -fn "explore-${DATASET_SIZE}" -ud -ufn "explore-update-${DATASET_SIZE}"
  mv td_data td_data-${DATASET_SIZE}
  cd ../kitt
fi

rm dataset*.ttl rdf_dataset*.yaml;
docker-compose stop
docker-compose rm -f
docker-compose up -d
sleep 30

if [ ! -f "dataset-${DATASET_SIZE}_v2.kitt.bz2" ]; then
  kitt_v3_linux -t -s iswc rdf -co "dataset-${DATASET_SIZE}_v2.kitt.bz2" "../bsbm-tools/explore-${DATASET_SIZE}.ttl"
fi

kitt_v3_linux -t -s iswc add --space iswc
kitt_v3_linux -t -s iswc add -g "bsbm-${DATASET_SIZE}" -m "dataset-${DATASET_SIZE}_v2.kitt.bz2"
python3 ../import_rdf.py -i "dataset-${DATASET_SIZE}.ttl" -f turtle -t iswc -g dataset-${DATASET_SIZE} c -ps 20000 -s True -u False
python3 bsbm_exp.py -t iswc -g bsbm-${DATASET_SIZE} -ps 20000 -qs ${TOTAL_QUERIES_PER_QTYPE} -pl ${PARALLELISM} > "bsbm-test.${DATASET_SIZE}.${PARALLELISM}.log"

kitt_v3_linux -t -s iswc get -g "bsbm-${DATASET_SIZE}"  > "graph.bsbm.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"
kitt_v3_linux -t ps -r > "pstats.bsbm.${VERSION}.${DATASET_SIZE}.log"
docker stats --no-stream > "stats.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"
docker-compose logs > "docker.${VERSION}.${DATASET_SIZE}.${PARALLELISM}.log"
docker-compose stop
docker-compose rm -f
rm dataset*.ttl rdf_dataset*.yaml;