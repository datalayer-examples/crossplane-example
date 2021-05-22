# Step 6: Deploy a Reference Platform

## Define the platform

```bash
# kubectl crossplane install configuration registry.upbound.io/upbound/platform-ref-multi-k8s:v0.0.4
make platform-install
kubectl get xrd
```

## Claim a platform

```bash
make platform-claim
kubectl get pkg
kubectl describe configurationrevision
kubectl get managed
kubectl get networks
kubectl get gkeclusters
kubectl get secrets -n crossplane-system | grep gkecluster
```

```bash
make platform-destroy
```

## Claim a platform (details)

```bash
# Taken from https://raw.githubusercontent.com/upbound/platform-ref-multi-k8s/master/examples/network-gcp.yaml
echo """
apiVersion: multik8s.platformref.crossplane.io/v1alpha1
kind: Network
metadata:
  name: network-gcp
spec:
  id: multik8s-network-gcp
  clusterRef:
    id: multik8s-cluster-gcp
  compositionSelector:
    matchLabels:
      provider: GCP
""" | kubectl apply -f -
k get networks
```

```bash
# Taken from https://raw.githubusercontent.com/upbound/platform-ref-multi-k8s/master/examples/cluster-gcp.yaml
echo """
apiVersion: multik8s.platformref.crossplane.io/v1alpha1
kind: Cluster
metadata:
  name: multik8s-cluster-gcp
spec:
  compositionSelector:
    matchLabels:
      provider: GCP
  id: multik8s-cluster-gcp
  parameters:
    nodes:
      count: 3
      size: small
    services:
      operators:
        prometheus:
          version: \"10.0.2\"
    networkRef:
      id: multik8s-network-gcp
  writeConnectionSecretToRef:
    name: cluster-conn-gcp
""" | kubectl apply -f -
kubectl get gkeclusters
```
