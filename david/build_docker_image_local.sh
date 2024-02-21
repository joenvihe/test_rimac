#!/bin/bash

docker build -t heart-dissease-prediction-api:latest . -f david/Dockerfile
docker run -p 8001:8001 -e PORT=8001 heart-dissease-prediction-api