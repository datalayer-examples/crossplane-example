# Custom User Interface

You are going to build and deploy a UI (React.js web application) to connect to a database created by Crossplane.

<img src="./../static/images/users.png" style="max-width: 800px"/>

## Prerequisites

You need the following tools on your local environment.

- [Conda](https://docs.conda.io/en/latest/miniconda.html).
- [Postgresql](https://www.postgresql.org) server if you want to test the UI locally.
- [Kubectl](https://kubernetes.io/docs/tasks/tools).
- [Helm](https://helm.sh).

## Environment

```bash
# Setup your development environment.
conda deactivate && \
  make env-rm # If you want to reset your env.
# Create your conda environment.
make env && \
  conda activate crossplane-examples
```

## Build the application

You are going to build a [react.js web application](./../src) connecting to a [python server](./../crossplane_examples) REST endpoints.

The UI allows you to insert and view a list of simple records from the [postgresql](https://www.postgresql.org) database. The server endpoints connect to a postgresql database. The database connection details are expected to be provided via environment variables.

```bash
# Install the node and python dependencies and be ready to rock the dev.
make install
# Build the application.
make build
```

## Test with a local Database

You need a running postgresql database with a role, e.g. `datalayer`.

!!! You will need a user with the same name as the chosen role on your operating system...

```bash
# Create the crossplane_examples database.
createdb crossplane_examples
# Create a user, e.g. datalayer
createuser --interactive --pwprompt
```

```bash
# Create the USERS table.
psql -c "CREATE TABLE USERS(ID SERIAL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL);" -d crossplane_examples
# Grant the USERS table.
psql -c "GRANT ALL PRIVILEGES ON DATABASE USERS TO datalayer;" -d crossplane_examples
# Test dummy data insertion.
psql -c "INSERT INTO USERS (first_name, last_name) VALUES ('Charlie', 'Brown');" -d crossplane_examples
psql -c "SELECT * FROM USERS;" -d crossplane_examples
psql -c "DELETE FROM USERS;" -d crossplane_examples
```

```bash
# Save your database connection details in a .env file.
echo """export DB_HOST=localhost
export DB_PORT=5432
export DB_USERNAME=datalayer
export DB_PASSWORD=datalayer""" > .env
# Source that .env file in your shell environment.
source .env
printenv | grep "DB_"
```

You are now ready to run the application on your local environment.

```bash
echo open http://localhost:3003 # The Webpack server.
echo open http://localhost:8765 # The Python server.
make start
```

## Docker Image

To run on a Kubernetes cluster, you need a docker image.

```bash
# Build the docker image.
make docker-build
```

```bash
# Save your database connection details in a .env file.
echo """DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=datalayer
DB_PASSWORD=datalayer
DB_LOCAL_START=true""" > .docker-env
```

```bash
# Start a local docker container.
echo open http://localhost:8765
make docker-start
make docker-logs
```

```bash
# Stop the local docker container.
make docker-rm
```

## Run on the Control Cluster

```bash
# Push the docker image to local registry.
make docker-push-local
```

```bash
# Install the helm chart on the local control cluster.
make helm-install-local
watch make helm-status
```

```bash
# Browse the UI.
# Option 1 - Connect with a proxy.
echo open http://localhost:8001/api/v1/namespaces/crossplane-examples/services/http:crossplane-examples-service:8765/proxy/
kubectl proxy
# Option 2 - Connect with port-forward.
echo open http://localhost:30000
make port-forward
# 🚧 Option 3 - Connect via the node port - The nodeport does not work yet...
open http://localhost:30000
```

```bash
# Uninstall the helm chart.
make helm-rm
```

## Run on a Workload Cluster

```bash
# Push the docker image to your registry.
# REGISTRY=docker.io/datalayer make docker-push-registry
REGISTRY=<YOUR_REGISTRY> make docker-push-registry
```

```bash
# Install the ExampleUI composition.
kubectl apply -f ./etc/composition/example-ui/compose
kubectl get xrd | grep exampleuis
```

```bash
# Claim a ExampleUI cluster.
kubectl apply -f ./etc/composition/example-ui/claim
```

```bash
# Get the ExampleUI cluster status.
watch kubectl get managed
kubectl get networks
kubectl get gkeclusters
kubectl get cloudsqlinstances
kubectl get sql
kubectl get helm
kubectl get exampleuis
```

```bash
# Proxy to the workload GKE cluster.
K8S_SECRET=$(kubectl get secrets -n crossplane-system | grep gkecluster | awk '{print $1;}')
echo $K8S_SECRET
kubectl describe secret $K8S_SECRET -n crossplane-system
kubectl get secret $K8S_SECRET -n crossplane-system -o jsonpath='{.data.kubeconfig}' | base64 --decode > kubeconfig
kubectl --kubeconfig kubeconfig get pods -A
# Browse the ExampleUI with a proxy and insert records.
echo open http://localhost:8001/api/v1/namespaces/crossplane-examples/services/http:crossplane-examples-service:8765/proxy/
kubectl --kubeconfig kubeconfig proxy
```

```bash
# Connect to the database.
# DB_SECRET=$(kubectl get secrets -n crossplane-system | grep postgresql | awk '{print $1;}')
# kubectl describe secret $DB_SECRET -n crossplane-system
DB_SECRET=$(kubectl get secrets -n crossplane-system | grep role-exampleui-postgresql | awk '{print $1;}')
echo $DB_SECRET
kubectl describe secret $DB_SECRET -n crossplane-system
export DB_ENDPOINT=$(kubectl get secret $DB_SECRET -n crossplane-system -o jsonpath='{.data.endpoint}' | base64 --decode)
export DB_USERNAME=$(kubectl get secret $DB_SECRET -n crossplane-system -o jsonpath='{.data.username}' | base64 --decode)
export DB_PASSWORD=$(kubectl get secret $DB_SECRET -n crossplane-system -o jsonpath='{.data.password}' | base64 --decode)
PGPASSWORD=$DB_PASSWORD psql "dbname=postgres user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\l
\c crossplane_examples
# You are now connected to database "crossplane_examples" as user "crossplane-example-role".
SELECT * FROM USERS;
\q
```

```bash
# Terminate the ExampleUI cluster.
kubectl delete -f ./etc/composition/example-ui/claim
```
