#!/bin/bash

docker build -t heart-dissease-prediction-api:latest .

docker tag heart-dissease-prediction-api:latest 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo/heart-dissease-prediction-api:latest

# aws ecr  get-login --no-include-email --region us-east-1

# docker run -p 8001:8001 -e PORT=8001 heart-dissease-prediction-api
docker push 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo/heart-dissease-prediction-api:latest