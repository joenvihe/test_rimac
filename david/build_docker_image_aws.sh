#!/bin/bash

docker build -t heart-disease-api-ecr-repo:latest . -f david/Dockerfile
docker images
docker tag heart-disease-api-ecr-repo:latest 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo:latest

# aws ecr  get-login --no-include-email --region us-east-1
aws --profile developer1 ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 656662427506.dkr.ecr.us-east-1.amazonaws.com
# docker run -p 8001:8001 -e PORT=8001 heart-dissease-prediction-api
docker push 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo:latests