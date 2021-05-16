# Step 5: Deploy Helm charts

## Install Helm Provider

```bash
# https://github.com/crossplane-contrib/provider-helm/tree/master/examples/sample
kubectl crossplane install provider crossplane/provider-helm:master
kubectl get providers
```

## Deploy a Helm Chart on the Control cluster

Create a Helm Provider Config for the Control cluster.

```bash
# Define a provider config for Kind cluster (aka In Cluster).
# https://github.com/crossplane-contrib/provider-helm/blob/master/examples/provider-config/provider-config-incluster.yaml
# Make sure provider-helm has enough permissions to install your chart into cluster.
HELM_SERVICE_ACCOUNT=$(kubectl -n crossplane-system get sa -o name | grep provider-helm | sed -e 's|serviceaccount\/|crossplane-system:|g')
echo $HELM_SERVICE_ACCOUNT
kubectl create clusterrolebinding provider-helm-admin-binding --clusterrole cluster-admin --serviceaccount="${HELM_SERVICE_ACCOUNT}"
# https://raw.githubusercontent.com/crossplane-contrib/provider-helm/master/examples/provider-config/provider-config-incluster.yaml
echo """
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: helm-provider
spec:
  credentials:
    source: InjectedIdentity
""" | kubectl create -f -
kubectl get providerconfigs
kubectl get providerconfig helm-provider
```

Deploy a Helm release on the Control cluster.

```bash
# Deploy a helm chart on Kind cluster.
# https://raw.githubusercontent.com/crossplane-contrib/provider-helm/master/examples/sample/release.yaml
echo """
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: wordpress-example
spec:
  providerConfigRef:
    name: helm-provider
  forProvider:
    chart:
      name: wordpress
      repository: https://charts.bitnami.com/bitnami
      version: 9.3.19
    namespace: wordpress
    values:
      service:
        type: ClusterIP
    set:
      - name: param1
        value: value2
""" | kubectl apply -f -
kubectl get helm
kubectl get pods,svc -n wordpress
echo open http://localhost:8001/api/v1/namespaces/wordpress/services/http:wordpress-example:80/proxy/
kubectl proxy
```

## Deploy a Helm Chart on a GKE cluster

Create a Helm Provider Config for the GKE cluster.

```bash
# Define a provider config for the GKE cluster (with secret).
# https://github.com/crossplane-contrib/provider-helm/blob/master/examples/provider-config/provider-config-with-secret.yaml
echo """
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: helm-provider-$GKE_CLUSTER_NAME
spec:
  credentials:
    source: Secret
    secretRef:
      name: $GKE_CLUSTER_NAME-conn
      namespace: crossplane-system
      key: kubeconfig
""" | kubectl create -f -
kubectl get providerconfigs
kubectl get providerconfig helm-provider-$GKE_CLUSTER_NAME
kubectl describe providerconfig.helm.crossplane.io/helm-provider-$GKE_CLUSTER_NAME
```

Deploy a Helm release on the GKE cluster.

```bash
# Deploy a helm chart on the managed GKE cluster.
# https://raw.githubusercontent.com/crossplane-contrib/provider-helm/master/examples/sample/release.yaml
echo """
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: wordpress-example-$GKE_CLUSTER_NAME
spec:
  providerConfigRef:
    name: helm-provider-$GKE_CLUSTER_NAME
  forProvider:
    chart:
      name: wordpress
      repository: https://charts.bitnami.com/bitnami
      version: 9.3.19
    namespace: wordpress
    values:
      service:
        type: ClusterIP
    set:
      - name: param1
        value: value2
""" | kubectl apply -f -
kubectl get helm
kubectl describe release.helm.crossplane.io/wordpress-example-$GKE_CLUSTER_NAME
watch kubectl --kubeconfig=./kubeconfig get pods,svc -n wordpress
echo -e open http://localhost:8001/api/v1/namespaces/wordpress/services/http:wordpress-example-$GKE_CLUSTER_NAME:80/proxy/
kubectl --kubeconfig=./kubeconfig proxy
```

```bash
# https://github.com/stefanprodan/podinfo
echo """
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: podinfo-example-$GKE_CLUSTER_NAME
spec:
  providerConfigRef:
    name: helm-provider-$GKE_CLUSTER_NAME
  forProvider:
    chart:
      name: podinfo
      repository: https://stefanprodan.github.io/podinfo
#      version: 9.3.19
    namespace: podinfo
    values:
      replicaCount: 2 
      backend: http://backend-podinfo:9898/echo
""" | kubectl apply -f -
kubectl get helm
kubectl describe release.helm.crossplane.io/podinfo-example-$GKE_CLUSTER_NAME
watch kubectl --kubeconfig=./kubeconfig get pods,svc -n podinfo
echo -e open http://localhost:8001/api/v1/namespaces/podinfo/services/http:podinfo-example-$GKE_CLUSTER_NAME:9898/proxy/
kubectl --kubeconfig=./kubeconfig proxy
```
