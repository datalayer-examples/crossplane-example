## Step 4: Create GCP resources

## Create a Managed Bucket

```bash
# https://raw.githubusercontent.com/crossplane/provider-gcp/master/examples/storage/bucket.yaml
BUCKET_NAME=crossplane-example-$RAND
echo """
apiVersion: storage.gcp.crossplane.io/v1alpha3
kind: Bucket
metadata:
  name: example
  labels:
    example: \"true\"
  annotations:
    crossplane.io/external-name: $BUCKET_NAME
spec:
  location: US
  storageClass: MULTI_REGIONAL
  providerConfigRef:
    name: gcp-provider-config
  deletionPolicy: Delete
""" | kubectl create -f -
kubectl get managed
kubectl get bucket example
kubectl describe bucket.storage.gcp.crossplane.io/example
open https://console.cloud.google.com/storage/browser?project=$PROJECT_ID
```

```bash
# Destroy the bucket.
kubectl delete bucket.storage.gcp.crossplane.io/example
```

## Create a Managed Database

```bash
# Create a database.
echo """
apiVersion: v1
kind: Namespace
metadata:
  name: crossplane-examples
---
apiVersion: database.gcp.crossplane.io/v1beta1
kind: CloudSQLInstance
metadata:
  name: crossplane-example-db-1
spec:
  forProvider:
    databaseVersion: POSTGRES_9_6
    region: us-central1
    settings:
      tier: db-custom-1-3840
      dataDiskType: PD_SSD
      ipConfiguration:
        ipv4Enabled: true
        authorizedNetworks:
          - value: \"0.0.0.0/0\"
  writeConnectionSecretToRef:
    namespace: crossplane-examples
    name: db-conn-secret
""" | kubectl create -f -
kubectl get managed
kubectl get cloudsqlinstances
kubectl get cloudsqlinstance crossplane-example-db
kubectl describe secret db-conn-secret -n crossplane-examples
kubectl get secret db-conn-secret -n crossplane-examples -o jsonpath='{.data.endpoint}' | base64 --decode
open https://console.cloud.google.com/sql/instances?project=$PROJECT_ID
kubectl delete cloudsqlinstance crossplane-example-db
```

```bash
# Create a composed database.
# Composition available in https://github.com/crossplane/crossplane/tree/d04a059fe341a941760a3a94ef07085ae7158365/docs/snippets/package/gcp
# Docs on https://crossplane.io/docs/v1.2/getting-started/create-configuration.html
echo """
apiVersion: database.example.org/v1alpha1
kind: PostgreSQLInstance
metadata:
  name: my-db
  namespace: default
spec:
  parameters:
    storageGB: 20
  compositionSelector:
    matchLabels:
      provider: gcp
  writeConnectionSecretToRef:
    name: db-conn
""" | kubectl create -f -
kubectl get managed
kubectl get postgresqlinstance my-db
kubectl describe postgresqlinstance my-db
kubectl describe cloudsqlinstance my-db
# kubectl describe cloudsqlinstance.database.gcp.crossplane.io/my-db-d8z4g-6rf6v
kubectl describe secrets db-conn
open https://console.cloud.google.com/sql/instances?project=$PROJECT_ID
```

```bash
# https://github.com/datalayer-externals/crossplane-provider-sql
kubectl crossplane install provider crossplane/provider-sql:master
kubectl get providers
k describe providers crossplane-provider-sql
echo """
apiVersion: postgresql.sql.crossplane.io/v1alpha1
kind: ProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: PostgreSQLConnectionSecret
    connectionSecretRef:
      namespace: default
      name: db-conn
---
apiVersion: postgresql.sql.crossplane.io/v1alpha1
kind: Database
metadata:
  name: jupyterhub
spec:
  forProvider: {}
---
apiVersion: postgresql.sql.crossplane.io/v1alpha1
kind: Role
metadata:
  name: example-role
spec:
  forProvider:
    privileges:
      createDb: true
      login: true
  writeConnectionSecretToRef:
    name: example-role-secret
    namespace: default
---
apiVersion: postgresql.sql.crossplane.io/v1alpha1
kind: Grant
metadata:
  name: example-grant-role-1-on-database
spec:
  forProvider:
    privileges:
      - CREATE
    withOption: GRANT
    roleRef:
      name: example-role
    databaseRef:
      name: example
""" | kubectl create -f -
kubectl describe database.postgresql.sql.crossplane.io/example 
```

```bash
# Connect to the database https://cloud.google.com/sql/docs/postgres/connect-admin-ip
export DB_ENDPOINT=$(kubectl get secret db-conn -n default -o jsonpath='{.data.endpoint}' | base64 --decode)
export DB_PORT=$(kubectl get secret db-conn -n default -o jsonpath='{.data.port}' | base64 --decode)
export DB_USERNAME=$(kubectl get secret db-conn -n default -o jsonpath='{.data.username}' | base64 --decode)
export DB_PASSWORD=$(kubectl get secret db-conn -n default -o jsonpath='{.data.password}' | base64 --decode)
PGPASSWORD=$DB_PASSWORD psql "sslmode=disable dbname=postgres user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\l
\q
PGPASSWORD=$DB_PASSWORD psql "sslmode=disable dbname=example user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\l
\q
```

```bash
# Run JupyterHub with the database.
# export JPY_PSQL_PASSWORD=jupyterhub
# PGPASSWORD=$DB_PASSWORD psql "sslmode=disable dbname=postgres user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
# CREATE DATABASE jupyterhub;
# CREATE USER jupyterhub WITH ENCRYPTED PASSWORD '$JPY_PSQL_PASSWORD';
# GRANT ALL PRIVILEGES ON DATABASE jupyterhub TO jupyterhub;
\q
jupyterhub --db=postgresql://$DB_USERNAME:$DB_PASSWORD@$DB_ENDPOINT:$DB_PORT/jupyterhub
open http://localhost:8000
PGPASSWORD=$DB_PASSWORD psql "sslmode=disable dbname=jupyterhub user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\d
SELECT * FROM pg_catalog.pg_tables where schemaname='public';
SELECT * FROM users;
SELECT * FROM groups;
SELECT * FROM servers;
\q
```

```bash
# Consume the database from a Pod.
echo """
apiVersion: v1
kind: Pod
metadata:
  name: see-db
  namespace: default
spec:
  containers:
  - name: see-db
    image: postgres:9.6
    command: ['psql']
    args: ['-c', 'SELECT current_database();']
    env:
    - name: PGDATABASE
      value: postgres
    - name: PGHOST
      valueFrom:
        secretKeyRef:
          name: db-conn
          key: endpoint
    - name: PGPORT
      valueFrom:
        secretKeyRef:
          name: db-conn
          key: port
    - name: PGUSER
      valueFrom:
        secretKeyRef:
          name: db-conn
          key: username
    - name: PGPASSWORD
      valueFrom:
        secretKeyRef:
          name: db-conn
          key: password
""" | kubectl create -f -
kubectl logs see-db
```

```bash
# Destroy the database.
kubectl delete pod see-db
kubectl delete postgresqlinstance my-db
```

## Create a Managed Network

```bash
# https://raw.githubusercontent.com/crossplane/provider-gcp/master/examples/compute/network.yaml
echo """
apiVersion: compute.gcp.crossplane.io/v1beta1
kind: Network
metadata:
  name: gke-test
spec:
  forProvider:
    autoCreateSubnetworks: false
    routingConfig:
      routingMode: REGIONAL
#  reclaimPolicy: Delete
  providerConfigRef:
    name: gcp-provider-config
""" | kubectl create -f -
kubectl get network gke-test
watch kubectl get network.compute.gcp.crossplane.io/gke-test
kubectl describe network.compute.gcp.crossplane.io/gke-test
open https://console.cloud.google.com/networking/networks/details/gke-test?project=$PROJECT_ID&pageTab=SUBNETS
```

```bash
# https://github.com/crossplane/provider-gcp/blob/master/examples/compute/subnetwork.yaml
echo """
apiVersion: compute.gcp.crossplane.io/v1beta1
kind: Subnetwork
metadata:
  name: gke-test-subnetwork
spec:
  forProvider:
    region: us-central1
    ipCidrRange: \"192.168.0.0/24\"
    privateIpGoogleAccess: true
    secondaryIpRanges:
      - rangeName: pods
        ipCidrRange: 10.128.0.0/20
      - rangeName: services
        ipCidrRange: 172.16.0.0/16
    networkRef:
      name: gke-test
#  reclaimPolicy: Delete
  providerConfigRef:
    name: gcp-provider-config
""" | kubectl create -f -
kubectl get subnetwork gke-test-subnetwork
watch kubectl get network.compute.gcp.crossplane.io/gke-test \
  subnetwork.compute.gcp.crossplane.io/gke-test-subnetwork
kubectl describe subnetwork.compute.gcp.crossplane.io/gke-test-subnetwork
open https://console.cloud.google.com/networking/networks/details/gke-test?project=$PROJECT_ID&pageTab=SUBNETS
```

## Creata a Managed GKE cluster

```bash
GKE_CLUSTER_NAME=cluster-example-1
```

Create a GKE cluster master.

```bash
# Create the gke cluster https://raw.githubusercontent.com/crossplane/provider-gcp/master/examples/gke/gke.yaml
echo """
apiVersion: container.gcp.crossplane.io/v1beta1
kind: GKECluster
metadata:
  name: $GKE_CLUSTER_NAME
spec:
  providerConfigRef:
    name: gcp-provider-config
  writeConnectionSecretToRef:
    name: $GKE_CLUSTER_NAME-conn
    namespace: crossplane-system
  forProvider:
    initialClusterVersion: \"1.18\"
    network: \"gke-test\"
    location: us-central1-a
    masterAuth:
      username: admin
      clientCertificateConfig:
        issueClientCertificate: true
    binaryAuthorization:
      enabled: false
    ipAllocationPolicy:
      useIpAliases: true
      createSubnetwork: true
    legacyAbac:
      enabled: false
    loggingService: \"logging.googleapis.com/kubernetes\"
    monitoringService: \"monitoring.googleapis.com/kubernetes\"
    networkPolicy:
      enabled: false
#      provider: CALICO
    podSecurityPolicyConfig:
      enabled: false
    addonsConfig:
      cloudRunConfig:
        disabled: true
      dnsCacheConfig:
        enabled: false
      gcePersistentDiskCsiDriverConfig:
        enabled: true
      horizontalPodAutoscaling:
        disabled: true
      httpLoadBalancing:
        disabled: true
      istioConfig:
        disabled: true
#        auth: \"AUTH_NONE\"
      kalmConfig:
        enabled: false
      kubernetesDashboard:
        disabled: true
      networkPolicyConfig:
        disabled: true
""" | kubectl create -f -
kubectl get gkecluster $GKE_CLUSTER_NAME
watch kubectl get gkeclusters
watch kubectl get gkecluster.container.gcp.crossplane.io/$GKE_CLUSTER_NAME \
  nodepool.container.gcp.crossplane.io/$GKE_CLUSTER_NAME-np
kubectl describe gkecluster.container.gcp.crossplane.io/$GKE_CLUSTER_NAME
open https://console.cloud.google.com/kubernetes/list?project=$PROJECT_ID
```

Create the GKE cluster Nodepool.

```bash
# Create the nodepool https://raw.githubusercontent.com/crossplane/provider-gcp/master/examples/gke/gke.yaml
echo """
apiVersion: container.gcp.crossplane.io/v1alpha1
kind: NodePool
metadata:
  name: $GKE_CLUSTER_NAME-np
spec:
  providerConfigRef:
    name: gcp-provider-config
  forProvider:
    clusterRef:
      name: $GKE_CLUSTER_NAME
    initialNodeCount: 3
    locations:
      - \"us-central1-a\"
    autoscaling:
      autoprovisioned: false
      enabled: true
      maxNodeCount: 5
      minNodeCount: 3  
    config:
      machineType: n1-standard-1
      diskSizeGb: 12
      diskType: pd-ssd
      imageType: cos_containerd
      labels:
        test-label: crossplane-created
#      sandboxConfig:
#        sandboxType: gvisor
      oauthScopes:
      - \"https://www.googleapis.com/auth/devstorage.read_only\"
      - \"https://www.googleapis.com/auth/logging.write\"
      - \"https://www.googleapis.com/auth/monitoring\"
      - \"https://www.googleapis.com/auth/servicecontrol\"
      - \"https://www.googleapis.com/auth/service.management.readonly\"
      - \"https://www.googleapis.com/auth/trace.append\"
""" | kubectl create -f -
watch kubectl get gkeclusters,nodepools
kubectl get nodepool $GKE_CLUSTER_NAME-np
kubectl describe nodepool.container.gcp.crossplane.io/$GKE_CLUSTER_NAME-np
open https://console.cloud.google.com/kubernetes/list?project=$PROJECT_ID
```

Get GKE kubeconfig.

```bash
kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system
kubectl describe secret $GKE_CLUSTER_NAME-conn -n crossplane-system
kubectl get all -n operators
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.username}') | base64 --decode > username
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.password}') | base64 --decode > password
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.clientCert}') | base64 --decode > clientCert
openssl x509 -in ./clientCert -noout -text
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.clientKey}') | base64 --decode > clientKey
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.endpoint}') | base64 --decode > endpoint
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.clusterCA}') | base64 --decode > clusterCA
openssl x509 -in ./clusterCA -noout -text
echo $(kubectl get secret $GKE_CLUSTER_NAME-conn -n crossplane-system -o jsonpath='{.data.kubeconfig}') | base64 --decode > kubeconfig
# Optionally, connect to GKE API via gcloud CLI.
# KUBECONFIG=$PWD/kubeconfig gcloud container clusters get-credentials $GKE_CLUSTER_NAME --region us-central1-a --project $PROJECT_ID
```

```bash
# Connect to GKE API via the provided kubeconfig.
kubectl --kubeconfig=./kubeconfig cluster-info --context $GKE_CLUSTER_NAME
kubectl --kubeconfig=./kubeconfig get pods -A
```

```bash
# kubectl get compositenetwork
# kubectl describe compositenew
# kubectl get managed
```

```bash
# Destroy GKE cluster.
kubectl delete nodepool $GKE_CLUSTER_NAME-np
kubectl delete gkecluster $GKE_CLUSTER_NAME
```

```bash
# Destroy networks.
kubectl delete subnetwork gke-test-subnetwork
kubectl delete network gke-test-network
```
