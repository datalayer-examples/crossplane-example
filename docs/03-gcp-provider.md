# Step 3: Create a GCP Provider on the Control cluster

## Install Crossplane GCP Provider

```bash
# Option 1 - Using the Crossplane CLI.
kubectl crossplane install provider crossplane/provider-gcp:v0.17.1
kubectl get pkg
watch kubectl get providers
kubectl describe provider crossplane-provider-gcp
```

```bash
# Option 2 - The core Crossplane controller can install provider controllers and CRDs for you through its own provider packaging mechanism, which is triggered by the application of a Provider resource.
# For example, in order to request installation of the provider-gcp package, apply the following resource to the cluster where Crossplane is running.
# The field spec.package is where you refer to the container image of the provider.
# Crossplane Package Manager will unpack that container, register CRDs and set up necessary RBAC rules and then start the controllers.
echo """
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp
spec:
  package: \"crossplane/provider-gcp:v0.17.1\"
""" | kubectl create -f - 
```

```bash
# Option 3 - As part of Crossplane Helm chart by adding the following statement to your helm install command:
helm install crossplane \
  --namespace crossplane-system \
  crossplane-stable/crossplane \
  --version 1.2.1 \
  --create-namespace \
  --set provider.packages={crossplane/provider-gcp:v0.17.1}
```

## Install more providers

Watch out when you install the more providers, the later providerconfigs may be hidden (read more on e.g. [provider-helm hides providerconfigs](https://github.com/crossplane-contrib/provider-helm/issues/89)).

```bash
# Helm provider may be useful for you.
kubectl crossplane install provider crossplane/provider-helm:v0.7.0
```

You calso install a `Configuration` shipping the providers.

```bash
# Install platform-ref-gcp configuration that contains provider-gcp and provider-helm.
kubectl crossplane install configuration registry.upbound.io/upbound/platform-ref-gcp:v0.0.2
watch kubectl get providers
kubectl get crds
kubectl get crds | grep gcp
kubectl get crds | grep database
```

```bash
# Install getting-started-with-gcp configuration that contains provider-gcp, provider-helm and custom postgresql database CRD.
kubectl crossplane install configuration registry.upbound.io/xp/getting-started-with-gcp:v1.2.1
kubectl get crds | grep gcp
kubectl get crds | grep database
kubectl get crds | grep postgresql
kubectl get xrd | grep postgresql
```

## Create Crossplane GCP Secret

```bash
# Create service account key (this will create a `crossplane-gcp-provider-key.json` file in your current working directory)
KEY_FILE=crossplane-gcp-provider-key.json
gcloud iam service-accounts keys create $KEY_FILE --project $PROJECT_ID --iam-account $SERVICE_ACCOUNT
# Change this namespace value if you want to use a different namespace (e.g. gitlab-managed-apps)
PROVIDER_SECRET_NAMESPACE=crossplane-system
```

```bash
# Option 1.
kubectl create secret generic gcp-creds -n $PROVIDER_SECRET_NAMESPACE --from-file=creds=$KEY_FILE
rm $KEY_FILE
```

```bash
# Option 2.
GOOGLE_APPLICATION_CREDENTIALS=$PWD/$KEY_FILE
# Base64 encode the GCP credentials.
BASE64ENCODED_GCP_PROVIDER_CREDS=$(base64 $KEY_FILE | tr -d "\n")
echo """
apiVersion: v1
kind: Secret
metadata:
  name: gcp-creds
  namespace: ${PROVIDER_SECRET_NAMESPACE}
type: Opaque
data:
  creds: ${BASE64ENCODED_GCP_PROVIDER_CREDS}
""" | kubectl create -f -
kubectl get secret gcp-creds -n $PROVIDER_SECRET_NAMESPACE
kubectl describe secret gcp-creds -n $PROVIDER_SECRET_NAMESPACE
# Delete the credentials.
unset BASE64ENCODED_GCP_PROVIDER_CREDS
rm $KEY_FILE
```

## Create Crossplane GCP Provider Configuration

```bash
# The default GCP configuration.
echo """
apiVersion: gcp.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  projectID: ${PROJECT_ID}
  credentials:
    source: Secret
    secretRef:
      namespace: ${PROVIDER_SECRET_NAMESPACE}
      name: gcp-creds
      key: creds
""" | kubectl create -f -
kubectl get providerconfig default
# Another GCP configuration, named gcp-provider-config, which is used in some examples.
echo """
apiVersion: gcp.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: gcp-provider-config
spec:
  projectID: ${PROJECT_ID}
  credentials:
    source: Secret
    secretRef:
      namespace: ${PROVIDER_SECRET_NAMESPACE}
      name: gcp-creds
      key: creds
""" | kubectl create -f -
kubectl get providerconfig gcp-provider-config
kubectl get providerconfigs
```
