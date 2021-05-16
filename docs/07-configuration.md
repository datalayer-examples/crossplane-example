# Step 7: Deploy a Configuration

- https://crossplane.github.io/docs/v1.2/getting-started/create-configuration.html

## Build your Configuration

```bash
curl -OL https://raw.githubusercontent.com/crossplane/crossplane/release-1.2/docs/snippets/package/definition.yaml
curl -OL https://raw.githubusercontent.com/crossplane/crossplane/release-1.2/docs/snippets/package/gcp/composition.yaml
curl -OL https://raw.githubusercontent.com/crossplane/crossplane/release-1.2/docs/snippets/package/gcp/crossplane.yaml
kubectl crossplane install configuration .
kubectl crossplane build configuration .
ls *.xpkg
```

## Publish your Configuration

```bash
REG=gcr.io/datalayer-dev-1
kubectl crossplane push configuration ${REG}/getting-started-with-gcp:master
```

## Use your Configuration

```bash
# https://cloud.upbound.io/registry/upbound/platform-ref-gcp
# GKE + Network
kubectl crossplane install configuration registry.upbound.io/upbound/platform-ref-gcp:v0.0.2
# https://github.com/crossplane/crossplane/blob/master/.github/workflows/configurations.yml
# https://github.com/crossplane/crossplane/tree/master/docs/snippets/package/gcp
# crossplane/provider-gcp + PostgreSQL database
kubectl crossplane install configuration registry.upbound.io/xp/getting-started-with-gcp
watch kubectl get configuration
watch kubectl get pkg
watch kubectl get providers
kubectl get crd | grep database
kubectl get crd | grep postgresql
## Install GC configuration.
kubectl crossplane install configuration gcr.io/datalayer-dev-1/getting-started-with-gcp:master
```
