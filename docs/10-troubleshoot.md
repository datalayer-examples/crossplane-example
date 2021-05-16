# Troubleshoot

Notes taken from the [troubleshooting](https://crossplane.io/docs/v1.2/reference/troubleshoot.html) crossplane documentation page.

```bash
kubectl -n crossplane-system logs -lapp=crossplane
# Sometimes, for example when you encounter a bug, it can be useful to pause Crossplane if you want to stop it from actively attempting to manage your resources. To pause Crossplane without deleting all of its resources, run the following command to simply scale down its deployment.
kubectl -n crossplane-system scale --replicas=0 deployment/crossplane
# Once you have been able to rectify the problem or smooth things out, you can unpause Crossplane simply by scaling its deployment back up.
kubectl -n crossplane-system scale --replicas=1 deployment/crossplane
```

```bash
# Deleting When a Resource Hangs.
# The resources that Crossplane manages will automatically be cleaned up so as not to leave anything running behind. This is accomplished by using finalizers, but in certain scenarios the finalizer can prevent the Kubernetes object from getting deleted.
# To deal with this, we essentially want to patch the object to remove its finalizer, which will then allow it to be deleted completely. Note that this won’t necessarily delete the external resource that Crossplane was managing, so you will want to go to your cloud provider’s console and look there for any lingering resources to clean up.
# In general, a finalizer can be removed from an object with this command:
kubectl patch <resource-type> <resource-name> -p '{"metadata":{"finalizers": []}}' --type=merge
# For example, for a CloudSQLInstance managed resource (database.gcp.crossplane.io) named my-db, you can remove its finalizer with:
kubectl patch cloudsqlinstance my-db -p '{"metadata":{"finalizers": []}}' --type=merge
```
