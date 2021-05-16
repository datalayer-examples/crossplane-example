# Step 8: Deploy a Wordpress Cluster

```bash
kubectl apply -f ./etc/wordpress-cluster/configuration
kubectl apply -f ./etc/wordpress-cluster/claim
```

```bash
cd ./etc/wordpress-cluster/configuration && \
  kubectl crossplane build configuration
ls *.xpkg
REG=...
kubectl crossplane push configuration ${REG}/wordpresscluster:master
kubectl crossplane install configuration ${REG}/wordpresscluster:master
watch kubectl get configuration
watch kubectl get pkg
watch kubectl get providers
```
