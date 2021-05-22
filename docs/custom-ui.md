# Custom User Interface

You are going to build and deploy a UI (React.js web application) to connect to a database created by Crossplane.

<img src="./../res/users.png" style="max-width: 800px"/>

## Prerequisites

You need the following tools on your local environment.

- [Conda](https://docs.conda.io/en/latest/miniconda.html).
- [Kubectl](https://kubernetes.io/docs/tasks/tools).
- [Helm](https://helm.sh).
- Optionally, a running [Postgresql](https://www.postgresql.org) server if you want to test the UI locally.

## Environment

```bash
# First remove if you want to start from zero.
# make env-rm
# Create your conda environment.
make env
```

```bash
# Install the node and python dependencies and be ready to rock the dev.
make dev
```

## Build the application

This will be a [React.js web application](./../src) with a [python server](./../crossplane_examples) exposing REST endpoints.

The UI allows you to insert and view a list of simple records from the Postgresql database.

The server endpoints connect to a Postgresql database. The database connection details are expected to be provided via environment variables.

```python
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    database="crossplane_examples",
    )
```

## Test with a local database

You need a running Postgresql database with e.g. a role `datalayer`

```bash
# Create the crossplane_examples database.
createdb crossplane_examples
# Create a user, e.g. datalayer
# !!! You will need a user with the same name on your operating system...
createuser --interactive --pwprompt
```

```sql
-- Create the USERS table.
psql -c "CREATE TABLE USERS(ID SERIAL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL);" -d crossplane_examples
-- Grant the USERS table.
psql -c "GRANT ALL PRIVILEGES ON DATABASE USERS TO datalayer;" -d crossplane_examples
```

```bash
# Save your config in a .env file.
echo """DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=datalayer
DB_PASSWORD=datalayer""" > .env
# Source that .env file in your shell environment.
source .env
```

You are now ready to run the application.

```bash
# open http://localhost:3003
# open http://localhost:8765
make start
```

## Prepare the Docker image

```bash
# Build a local docker image and push it to your registry.
make docker-build
REGISTRY=<YOUR_REGISTRY> make docker-tag docker-push
```

## 🚧 Run on the Control cluster

🚧 TBD

```bash
# Install the Helm chart
make helm-install.
```

## 🚧 Run on a Workload cluster

🚧 TBD

```bash
make crossplane-apply
make crossplane-status
```

```bash
# Install the Helm chart.
make helm-install
```

```bash
export DB_ENDPOINT=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.endpoint}' | base64 --decode)
export DB_USERNAME=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.username}' | base64 --decode)
export DB_PASSWORD=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.password}' | base64 --decode)
PGPASSWORD=$DB_PASSWORD psql "dbname=crossplane_examples user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\l
\q
```
