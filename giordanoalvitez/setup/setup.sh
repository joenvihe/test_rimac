

# Create repository in artifacts
gcloud artifacts repositories create $REPOSITORYNAME_ARTIFACT --repository-format=docker --location=us-central1 --description="My Artifact Repository"

# Create dataset
bq mk --dataset --location=us-central1 $GCP_PROJECT_ID:$DATASET_BIGQUERY

bq mk --dataset --location=us-central1 $GCP_PROJECT_ID:$DATASET_MLOPS_BIGQUERY

python build.py

# Assign roles for Cloud Build
gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} --member=serviceAccount:${GCP_NUMBER}@cloudbuild.gserviceaccount.com --role=roles/iam.serviceAccountUser
gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} --member=serviceAccount:${GCP_NUMBER}@cloudbuild.gserviceaccount.com --role=roles/run.admin





