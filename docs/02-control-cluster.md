[![Datalayer](https://assets.datalayer.design/datalayer-25.svg)](https://datalayer.io)

# Step 2: Create a Control Cluster

## Setup Kubectl Crossplane CLI

```bash
# Install CLI.
# curl -sL https://raw.githubusercontent.com/crossplane/crossplane/master/install.sh | sh
curl -sL https://raw.githubusercontent.com/crossplane/crossplane/release-1.3/install.sh | sh
mv kubectl-crossplane $(dirname $(which kubectl))
kubectl crossplane -h
kubectl crossplane -v
```

## Create a Control Cluster

```bash
# Create Control cluster.
CONTROL_CLUSTER_NAME=crossplane-examples
kind create cluster --name $CONTROL_CLUSTER_NAME
kubectl config use-context kind-$CONTROL_CLUSTER_NAME
```

```bash
# ... or if you also need a local registry.
./sbin/create-kind.sh
```

## Deploy Crossplane Controller on the Control Cluster

```bash
# https://crossplane.github.io/docs/v1.3/reference/install.html
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update
```

```bash
helm install crossplane \
  --namespace crossplane-system \
  crossplane-stable/crossplane \
  --version 1.3.0 \
  --create-namespace
watch kubectl get all -n crossplane-system
```

```bash
# Create a crossplanee-examples namespace for later usage.
echo """
apiVersion: v1
kind: Namespace
metadata:
  name: crossplane-examples
""" | kubectl create -f -
