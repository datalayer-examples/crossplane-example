# Custom User Interface

Your are going to build and deploy a UI (React.js web application) to connect to a database created by Crossplane.

<img src="./../res/users.png" style="max-width: 800px"/>

## Prerequisites

You need on your local environment:

- [Conda](https://docs.conda.io/en/latest/miniconda.html)
- A running [Postgresql](https://www.postgresql.org) server
- [Kubectl](https://kubernetes.io/docs/tasks/tools)
- [Helm](https://helm.sh)

## Environment

```bash
# Create your conda environment.
make env
```

```bash
# Install the node and python dep and be ready to rock the dev.
make dev
```

## Create the application

This will be a React.js packaged as a [single page web application](./../src) with a [python server](./../crossplane_examples) exposing REST endpoints. The UI allows you to insert and view a list of simple records from the Postgresql database. The endpoints connect to a Postgresql database. The database connection details are expected to be provided via environment variables.

```python
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    database="crossplane_examples",
    )
```

## Prepare the local database

You need a running Postgresql database with e.g. a role `datalayer`

```bash
echo """DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=datalayer
DB_PASSWORD=datalayer""" > .env
source .env
```

```bash
# Create the crossplane_examples database.
createdb crossplane_examples
# Create a user, e.g. datalayer
# !!! You will need a user with the same name on your Operating System...
createuser --interactive --pwprompt
```

```sql
-- Create the USERS table.
psql -c "CREATE TABLE USERS(ID SERIAL, FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL);" -d crossplane_examples
-- Grant the USERS table.
psql -c "GRANT ALL PRIVILEGES ON DATABASE USERS TO datalayer;" -d crossplane_examples
-- psql -c "DELETE FROM USERS;" -d crossplane_examples
```

## Test with a local database

You should be ready to run the application.

```bash
# open http://localhost:3003
# open http://localhost:8765
make start
```

## Prepare a Docker image

```bash
make docker-build
make docker-push
```

## Prepare the Helm chart

```bash
make helm-install
make helm-deploy
```

## 🚧 Run on the Control Cluster

🚧 TBD

## 🚧 Run on a Workload Cluster

🚧 TBD

```bash
make crossplane-apply
make crossplane-status
```

```bash
export DB_ENDPOINT=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.endpoint}' | base64 --decode)
export DB_USERNAME=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.username}' | base64 --decode)
export DB_PASSWORD=$(kubectl get secret crossplane-example-role-secret -n crossplane-examples -o jsonpath='{.data.password}' | base64 --decode)
PGPASSWORD=$DB_PASSWORD psql "dbname=crossplane_examples user=$DB_USERNAME hostaddr=$DB_ENDPOINT"
\l
\q
```
