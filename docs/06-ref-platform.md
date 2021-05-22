# Step 6: Deploy a Reference Platform

```bash
kubectl crossplane install configuration registry.upbound.io/upbound/platform-ref-multi-k8s:v0.0.4
kubectl get pkg
kubectl describe configurationrevision
kubectl get xrd
```

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
          version: "10.0.2"
    networkRef:
      id: multik8s-network-gcp
  writeConnectionSecretToRef:
    name: cluster-conn-gcp
""" | kubectl apply -f -
```
 