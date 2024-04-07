#!/bin/bash

docker stop oyente && docker rm oyente
mkdir -p contracts
mkdir -p oyente_json_result
docker pull luongnguyen/oyente && docker run -itd --name oyente -v $(pwd)/contracts_bin:/root/contracts_bin -v $(pwd)/oyente_json_result:/root/results luongnguyen/oyente

docker exec oyente find datasets/contracts -name "*.bin" | xargs -I {} -P 30 -i -r sh -c 'python /oyente/oyente/oyente.py -j -b -s {} 2>>error.log'