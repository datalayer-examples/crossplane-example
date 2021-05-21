[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# Step 1: Setup the prerequisistes

```bash
# Get to https://console.cloud.google.com/billing and copy the Billing Account ID value.
ACCOUNT_ID=<YOUR_ACCOUNT_ID>
# Create a new project (project id must be <=30 characters)
RAND=$RANDOM
PROJECT_ID="crossplane-example-$RAND"
```

## Create a GCloud project

```bash
gcloud projects create $PROJECT_ID --enable-cloud-apis # [--organization $ORGANIZATION_ID]
gcloud config set project $PROJECT_ID
# or, record the PROJECT_ID value of an existing project
# PROJECT_ID=$(gcloud projects list --filter NAME=<YOUR_PROJECT_NAME> --format="value(PROJECT_ID)")
```

## Link billing to your project

```bash
# Link billing to the new project.
gcloud beta billing projects link $PROJECT_ID --billing-account=$ACCOUNT_ID
```

## Enable GCloud services on your project

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

## Assign GCloud roles to your project

```bash
# Assign roles.
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/container.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/compute.networkAdmin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/cloudsql.admin"
# Enable Additional roles needed for the example or project.
# Run `gcloud iam roles list` for a complete list.
# gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:$SERVICE_ACCOUNT" --role="roles/redis.admin"
```
