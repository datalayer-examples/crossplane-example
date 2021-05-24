# Custom User Interface

You are going to build and deploy a UI (React.js web application) to connect to a database created by Crossplane.

<img src="./../static/images/users.png" style="max-width: 800px"/>

## Prerequisites

You need the following tools on your local environment.

- [Conda](https://docs.conda.io/en/latest/miniconda.html).
- [Kubectl](https://kubernetes.io/docs/tasks/tools).
- [Helm](https://helm.sh).
- Optionally, a running [Postgresql](https://www.postgresql.org) server if you want to test the UI locally.

## Environment

```bash
# Remove the existing environement if you want to start from zero.
conda deactivate && \
  make env-rm
# Create your conda environment.
make env
# Install the node and python dependencies and be ready to rock the dev.
make dev
```

## Build the application

You are going to build a [React.js web application](./../src) backed by a [python server](./../crossplane_examples) exposing REST endpoints.

The UI allows you to insert and view a list of simple records from the Postgresql database.

The server endpoints connect to a Postgresql database. The database connection details are expected to be provided via environment variables.

## Test with a local database

You need a running Postgresql database with a role, e.g. `datalayer`.

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
psql -c "INSERT INTO USERS(first_name, last_name) VALUES('Charlie', 'Brown');" -d crossplane_examples
psql -c "SELECT * FROM USERS;" -d crossplane_examples
psql -c "DELETE FROM USERS;" -d crossplane_examples
```

```bash
# Save your database connection details in a .env file.
echo """export DB_HOST=localhost
export DB_PORT=5432
export DB_USERNAME=datalayer
export DB_PASSWORD=datalayer""" > .env
```

```bash
# Source that .env file in your shell environment.
source .env
```

You are now ready to run the application on your local environment.

```bash
# open http://localhost:3003 # The Webpack server.
# open http://localhost:8765 # The Python server.
make start
```

## Prepare the Docker image

```bash
# Build a local docker image and push it to your registry.
make docker-build
# Push to local registry.
make docker-push-local
# Push to your registry.
REGISTRY=<YOUR_REGISTRY> make docker-push-registry
```

## Run on the Control cluster

```bash
# Install the Helm chart.
make helm-install-local
watch make helm-status
```

```bash
# Connect with a proxy.
echo open http://localhost:8001/api/v1/namespaces/crossplane-examples/services/http:crossplane-examples-service:8765/proxy/
kubectl proxy
# Connect with a port-forwrd.
echo open http://localhost:30000
make port-forward
# Connect via the node port.
# 🚧 The nodeport does not work yet...
open http://localhost:30000
```

```bash
# Uninstall the helm chart.
make helm-rm
```

## 🚧 Run on a Workload cluster

```bash
# 🚧 Create a GKE workload Cluster
make gke-example-create # create a gke cluster example.
make crossplane-status
```

```bash
# 🚧 Install the Helm chart.
make helm-install
```

```bash
# Connect with a proxy.
echo open http://localhost:8001/api/v1/namespaces/crossplane-examples/services/http:crossplane-examples-service:8765/proxy/
kubectl proxy
```

```bash
# 🚧 Connect to the database.
export DB_ENDPOINT=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.endpoint}' | base64 --decode)
export DB_USERNAME=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.username}' | base64 --decode)
export DB_PASSWORD=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.password}' | base64 --decode)
PGPASSWORD=$DB_PASSWORD psql "dbname=crossplane_examples user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\l
\q
```

```bash
# Terminate the resources.
make helm-rm
make gke-example-rm # delete the gke cluster example.
```
