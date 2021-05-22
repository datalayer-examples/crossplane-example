[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# Step 2: Create a Control cluster

## Setup Kubectl Crossplane CLI

```bash
# Install CLI.
curl -sL https://raw.githubusercontent.com/crossplane/crossplane/release-1.2/install.sh | sh
mv kubectl-crossplane $(dirname $(which kubectl))
kubectl crossplane -h
kubectl crossplane -v
```

## Create a Control cluster

```bash
# Create Control cluster.
CONTROL_CLUSTER_NAME=crossplane-examples
kind create cluster --name $CONTROL_CLUSTER_NAME
kubectl config use-context kind-$CONTROL_CLUSTER_NAME
```

```bash
# ... or if you also need a local registry.
./sbin/create-kind.sh
# Test the local registry.
docker pull gcr.io/google-samples/hello-app:1.0
docker tag gcr.io/google-samples/hello-app:1.0 localhost:5000/hello-app:1.0
docker push localhost:5000/hello-app:1.0
kubectl create deployment hello-server --image=localhost:5000/hello-app:1.0
k get deployment hello-server
k delete deployment hello-server
```

## Deploy Crossplane Controller on the Control cluster

```bash
# https://crossplane.github.io/docs/v1.2/reference/install.html
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update
```

```bash
helm install crossplane \
  --namespace crossplane-system \
  crossplane-stable/crossplane \
  --version 1.2.1 \
  --create-namespace
watch kubectl get all -n crossplane-system
```
