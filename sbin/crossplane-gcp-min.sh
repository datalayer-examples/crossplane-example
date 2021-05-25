#!/bin/sh

export RAND=$1
export PROJECT_ID="crossplane-example-$RAND"
export SERVICE_ACCOUNT="example-$RAND@${PROJECT_ID}.iam.gserviceaccount.com"

echo
echo ❇️ Installing Crossplane on the Control cluster
echo

helm install crossplane \
    --namespace crossplane-system \
    crossplane-stable/crossplane \
    --version 1.2.1 \
    --create-namespace && \
  sleep 15

echo
echo ❇️ Installing Crossplane GCP Provider on the Control cluster
echo

kubectl crossplane install provider crossplane/provider-gcp:master && \
  kubectl crossplane install provider crossplane/provider-helm:master && \
  sleep 60

echo
echo ❇️ Creating the CGP Credentials
echo

KEY_FILE=crossplane-gcp-provider-key.json && \
  gcloud iam service-accounts keys create $KEY_FILE --project $PROJECT_ID --iam-account $SERVICE_ACCOUNT && \
  kubectl create secret generic gcp-creds -n crossplane-system --from-file=creds=$KEY_FILE && \
  rm $KEY_FILE

function create_provider_config() {
  PROVIDER_CONFIG_NAME=$1
  echo
  echo ❇️ Creating the CGP secret with name $PROVIDER_CONFIG_NAME
  echo
  echo """
  apiVersion: gcp.crossplane.io/v1beta1
  kind: ProviderConfig
  metadata:
    name: $PROVIDER_CONFIG_NAME
  spec:
    projectID: ${PROJECT_ID}
    credentials:
      source: Secret
      secretRef:
        namespace: crossplane-system
        name: gcp-creds
        key: creds
  """ | kubectl create -f -
}

create_provider_config default
create_provider_config gcp-provider-config
