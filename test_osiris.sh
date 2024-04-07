#!/bin/bash

docker stop osiris && docker rm osiris
mkdir -p contracts
mkdir -p osiris_json_result
docker pull christoftorres/osiris && docker run -itd --name osiris -v $(pwd)/contracts_bin:/root/contracts_bin -v $(pwd)/osiris_json_result:/root/results christoftorres/osiris


docker exec osiris find /root/contracts_bin -name "*.bin" | xargs -I {} -P 30 -i -r sh -c 'python /root/osiris/osiris.py -j -b -s {} 2>>error.log'