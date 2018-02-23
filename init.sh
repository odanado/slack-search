#!/bin/bash

docker-compose up -d elasticsearch
sleep 10
docker-compose run --rm es-python python preprocess.py make_index
docker-compose run --rm es-python python preprocess.py import_json
