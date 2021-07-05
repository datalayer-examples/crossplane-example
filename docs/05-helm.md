# Step 5: Deploy Helm releases

## Install Helm Provider

```bash
# https://github.com/crossplane-contrib/provider-helm/tree/master/examples/sample
kubectl crossplane install provider crossplane/provider-helm:v0.7.0
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

```bash
# https://github.com/stefanprodan/podinfo
echo """
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: podinfo-example
spec:
  providerConfigRef:
    name: helm-provider
  forProvider:
    chart:
      name: podinfo
      repository: https://stefanprodan.github.io/podinfo
    namespace: podinfo
    values:
      replicaCount: 2 
      backend: http://backend-podinfo:9898/echo
""" | kubectl apply -f -
kubectl get helm
kubectl describe release.helm.crossplane.io/podinfo-example
watch kubectl get pods,svc -n podinfo
echo -e open http://localhost:8001/api/v1/namespaces/podinfo/services/http:podinfo-example:9898/proxy/
kubectl proxy
```

## Deploy a Helm Chart on a GKE Cluster

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

Deploy a Helm release on the GKE workload cluster.

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

## Msc

Create the database and reference the connection secret it produces in a helm Release values.

- https://doc.crds.dev/github.com/crossplane-contrib/provider-helm/helm.crossplane.io/Release/v1beta1@v0.5.0#spec-forProvider-valuesFrom-secretKeyRef

- https://github.com/crossplane-contrib/provider-helm/blob/master/examples/sample/release.yaml

```yaml
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: wordpress-example
spec:
# rollbackLimit: 3
  forProvider:
    chart:
      name: wordpress
      repository: https://charts.bitnami.com/bitnami
      version: 9.3.19
#     pullSecretRef:
#       name: museum-creds
#       namespace: default
#     url: "https://charts.bitnami.com/bitnami/wordpress-9.3.19.tgz"
    namespace: wordpress
#   skipCreateNamespace: true
#   wait: true
    values:
      service:
        type: ClusterIP
    set:
      - name: param1
        value: value2
#   valuesFrom:
#     - configMapKeyRef:
#         key: values.yaml
#         name: default-vals
#         namespace: wordpress
#         optional: false
#     - secretKeyRef:
#         key: svalues.yaml
#         name: svals
#         namespace: wordpress
#         optional: false
#  connectionDetails:
#    - apiVersion: v1
#      kind: Service
#      name: wordpress-example
#      namespace: wordpress
#      fieldPath: spec.clusterIP
#      #fieldPath: status.loadBalancer.ingress[0].ip
#      toConnectionSecretKey: ip
#    - apiVersion: v1
#      kind: Service
#      name: wordpress-example
#      namespace: wordpress
#      fieldPath: spec.ports[0].port
#      toConnectionSecretKey: port
#    - apiVersion: v1
#      kind: Secret
#      name: wordpress-example
#      namespace: wordpress
#      fieldPath: data.wordpress-password
#      toConnectionSecretKey: password
#  writeConnectionSecretToRef:
#    name: wordpress-credentials
#    namespace: crossplane-system
  providerConfigRef:
    name: helm-provider
```
