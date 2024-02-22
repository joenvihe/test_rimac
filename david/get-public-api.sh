#!/bin/bash

# Take the cluster name from the script arguments
CLUSTER_NAME=$1

# Get a list of tasks in the cluster
TASKS=$(aws ecs list-tasks --cluster "$CLUSTER_NAME" --query "taskArns" --output text)

# Loop through each task to get the container instance ARN
for TASK_ARN in $TASKS
do
  # Get a human readable ARN.
  TASK_ID=$(basename $TASK_ARN)
  
  # Get the network interface ID for the task
  NETWORK_INTERFACE_ID=$(aws ecs describe-tasks --cluster $CLUSTER_NAME --tasks $TASK_ARN --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text)
  
  #Get the public IP of the network interface
  PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids $NETWORK_INTERFACE_ID --query 'NetworkInterfaces[0].Association.PublicIp' --output text)

  echo "Task: $TASK_ID -- Public IP: http://$PUBLIC_IP:8001"
done