[![Datalayer](https://assets.datalayer.design/datalayer-25.svg)](https://datalayer.io)

# Crossplane Examples

<img src="./static/images/crossplane.svg" width="300"/>

This repository showcases different usecase for [Crossplane](https://crossplane.io) on top of [Google Cloud](https://cloud.google.com). It aims to complement the official [Crossplane documentation](https://crossplane.io/docs) to give step-by-step examples to deploy infrastructure and services on [Google Cloud](https://cloud.google.com). It focuses on GCP but can be applied to other clouds like [Amazon](https://aws.amazon.com), [Azure](https://azure.microsoft.com)...

You can read more context about Crossplane on the companion blog post [Crossplane by example](https://datalayer.blog/2021/05/16/crossplane-by-example).

> Ensure you have credits to spend on GCloud to run these examples.

We have a first section with use case like settting-up the environment, deploying managed and composite resources as helm chart... We also have a second section where we build a custom React.js user interface interacting with a managed database.

We are trying to stick to some definitions:

- `Control cluster`: The Kubernetes cluster that hosts the Crossplane operator, in our case a [Kind](https://kind.sigs.k8s.io) cluster.
- `Managed resources`: The managed infrastructure like Kubernetes clusters, databases, IAM roles... created by the Control cluster and running in the cloud.
- `Workload cluster`: The Kubernetes managed clusters created by the Control cluster and running in the cloud.

## Use Cases

You are expected to start from step 1 and follow-up step by step until the end. If you jump directly to a specific step, ensure your environment, including the shell environment variables, are set as expected.

Step 1: [Create GCloud Project](./docs/01-gcloud-project.md).

Step 2: [Create a Control Cluster](./docs/02-control-cluster.md).

Step 3: [Create a GCP Provider on the Control Cluster](./docs/03-gcp-provider.md)

Step 4: [Create GCP managed Resources](./docs/04-managed.md).

Step 5: [Deploy Helm Releases](./docs/05-helm.md).

Step 6: [Deploy a Composition](./docs/06-composition.md).

Step 7: [Deploy a Reference Platform](./docs/07-ref-platform.md).

Step 8: [Deploy a Wordpress Cluster](./docs/08-wordpress-cluster.md).

Step 9: [Destroy](./docs/09-destroy.md).

How to [Troubleshoot](./docs/10-troubleshoot.md) if needed, hopefully not too much.

## Custom Web User Interface

Build and deploy a UI to insert and view a list of rows from a Postgresql table deployed on GCP. Follow [these instructions](./docs/example-ui.md) to get the following UI in your browser.

<img src="./static/images/users.png" style="max-width: 800px"/>

## Bare Minimum Setup

Assuming you have a [created a GCloud project](./docs/01-gcloud-project.md) and [created a Control cluster](./docs/02-control-cluster.md), the bare minimun to run is the following.

```bash
./sbin/create-kind.sh
./sbin/crossplane-gcp-min.sh <YOUR_RANDOM_PROJECT_NUMBER>
```
