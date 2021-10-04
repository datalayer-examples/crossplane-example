[![Datalayer](https://datalayer.s3.us-east-1.amazonaws.com/datalayer-25.svg)](https://datalayer.io)

# Step 1: Create GCloud Project

```bash
# Get to https://console.cloud.google.com/billing and copy the Billing Account ID value.
ACCOUNT_ID=<YOUR_ACCOUNT_ID>
# Create a new project (project id must be <=30 characters)
RAND=$RANDOM
PROJECT_ID="crossplane-example-$RAND"
```

## Create a GCloud Project

```bash
gcloud projects create $PROJECT_ID --enable-cloud-apis # [--organization $ORGANIZATION_ID]
gcloud config set project $PROJECT_ID
# or, record the PROJECT_ID value of an existing project
# PROJECT_ID=$(gcloud projects list --filter NAME=<YOUR_PROJECT_NAME> --format="value(PROJECT_ID)")
```

## Link Billing to your Project

```bash
# Link billing to the new project.
gcloud beta billing projects link $PROJECT_ID --billing-account=$ACCOUNT_ID
```

## Enable GCloud Services on your Project

```bash
# Enable service on the new project.
gcloud services enable compute.googleapis.com --project $PROJECT_ID # enable Compute API
gcloud services enable servicenetworking.googleapis.com --project $PROJECT_ID # enable Service Networking API
gcloud services enable container.googleapis.com --project $PROJECT_ID # enable Kubernetes API
gcloud services enable sqladmin.googleapis.com --project $PROJECT_ID # enable CloudSQL API
gcloud services enable redis.googleapis.com --project $PROJECT_ID # enable Redis API
# Enable Additional APIs needed for the example or project.
# Run `gcloud services list` for a complete list.
```

## Create a GCloud Service Account

```bash
# Create a Service Account.
SERVICE_ACCOUNT_NAME="example-$RAND"
SERVICE_ACCOUNT="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME --project $PROJECT_ID --display-name "Crossplane Example"
```

## Assign GCloud Roles to your Project

```bash
# Assign roles.
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/container.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/compute.networkAdmin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/cloudsql.admin"
```

Enable additional roles needed for your needs.

```bash
# To get a complete list of roles
gcloud iam roles list
# gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/redis.admin"
```
