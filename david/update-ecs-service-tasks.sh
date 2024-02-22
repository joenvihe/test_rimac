# Create task
aws ecs run-task --cluster heart-dissease-app-ecs-cluster

# shut down all tasks
aws ecs update-service --cluster heart-dissease-app-ecs-cluster --service service3 --desired-count 0

# Stop a task
aws ecs stop-task --cluster heart-dissease-app-ecs-cluster --task $(aws ecs list-tasks --cluster heart-dissease-app-ecs-cluster  --service service3 --output text --query 'taskArns[0]')