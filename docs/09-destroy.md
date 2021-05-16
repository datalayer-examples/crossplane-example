## Step 9: Destroy

## Destroy the applications

```bash
helm delete crossplane --namespace crossplane-system
```

## Destroy the infrastructure

```bash
# https://crossplane.github.io/docs/v1.2/reference/uninstall.html
# Crossplane has a number of components that must be cleaned up in order to guarantee proper removal from the cluster. When deleting objects, it is best to consider parent-child relationships and clean up the children first to ensure the proper action is taken externally. For instance, cleaning up provider-aws before deleting an RDSInstance will result in the RDS instance remaining provisioned on AWS as the controller responsible for cleaning it up will have already been deleted. It will also result in the RDSInstance CRD remaining in the cluster, which could make it difficult to re-install the same provider at a future time.
```

```bash
# Deleting Resources
# If you wish for all claims (XRC), composite resources (XR), and managed resources to have deletion handled properly both in the cluster in externally, they should be deleted and no longer exist in cluster before the package that extended the Kubernetes API to include them is uninstalled. You can use the following logic to clean up resources effectively:
# If an XRC exists for a given XR and set of managed resources, delete the XRC and both the XR and managed resources will be cleaned up.
# If only an XR exists for a given set of managed resources, delete the XR and each of the managed resources will be cleaned up.
# If a managed resource was provisioned directly, delete it directly.
# The following commands can be used to identify existing XRC, XR, and managed resources:
kubectl get claim # XRC get all resources of all claim kinds, like PostgreSQLInstance.
kubectl get composite # XR get all resources that are of composite kind, like CompositePostgreSQLInstance.
kubectl get managed # Managed Resources get all resources that represent a unit of external infrastructure.
```

```bash
# kubectl get <name-of-provider> # Managed Resources get all resources related to <provider>.
kubectl get gcp # get all resources related to <provider>.
kubectl get crossplane # get all resources related to Crossplane.
kubectl get providers
```

```bash
# Crossplane controllers add finalizers to resources to ensure they are handled externally before they are fully removed from the cluster. If resource deletion hangs it is likely due to a delay in the resource being handled externally, causing the controller to wait to remove the finalizer. If this persists for a long period of time, use the troubleshooting guide to fix the issue.
# Uninstall Packages
# Once all resources are cleaned up, it is safe to uninstall packages. Configuration packages can typically be deleted safely with the following command:
kubectl delete configuration.pkg <configuration-name>
# Before deleting Provider packages, you will want to make sure you have deleted all ProviderConfigs you created. An example command if you used AWS Provider:
kubectl delete providerconfig.gcp --all
# Now you are safe to delete the Provider package:
kubectl delete provider.pkg gcp
# Uninstall Crossplane
# When all resources and packages have been cleaned up, you are safe to uninstall Crossplane:
helm delete crossplane --namespace crossplane-system
kubectl delete namespace crossplane-system
# Helm does not delete CRD objects. You can delete the ones Crossplane created with the following commands:
kubectl patch lock lock -p '{"metadata":{"finalizers": []}}' --type=merge
kubectl get crd -o name | grep crossplane.io | xargs kubectl delete
```

## Destroy the Control cluster

```bash
kind delete cluster --name $CONTROL_CLUSTER_NAME
```

## Destroy the GCloud project

```bash
gcloud projects delete $PROJECT_ID
```
