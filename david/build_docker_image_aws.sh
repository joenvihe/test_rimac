#!/bin/bash

docker build -t heart-disease-api-ecr-repo:latest . -f david/Dockerfile
docker images
docker pull 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo:latest
docker tag heart-disease-api-ecr-repo:latest 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo:latest

# aws --profile developer1 ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 656662427506.dkr.ecr.us-east-1.amazonaws.com
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 656662427506.dkr.ecr.us-east-1.amazonaws.com
docker push 656662427506.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api-ecr-repo:latest

# aws ecs update-service --cluster heart-dissease-app-ecs-cluster --service service3 --task-definition  task2 --force-new-deployment
aws ecs update-service --cluster heart-dissease-app-ecs-cluster --service service3 --desired-count 0 
sleep 20
aws ecs update-service --cluster heart-dissease-app-ecs-cluster --service service3 --desired-count 1