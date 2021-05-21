[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# Crossplane Examples

<img src="./res/crossplane.svg" width="300"/>

This repository showcases different usecase for [Crossplane](https://crossplane.io) on top of [Google Cloud](https://cloud.google.com). It aims to complement the official [Crossplane documentation](https://crossplane.io/docs) to give step-by-step examples to deploy infrastructure and services on [Google Cloud](https://cloud.google.com). It focuses on GCP but can be applied to other clouds like [Amazon](https://aws.amazon.com), [Azure](https://azure.microsoft.com)...

You can read more context about Crossplane on the companion blog post [Crossplane by example](https://blog.datalayer.io/2021/05/16/crossplane-by-example).

> Ensure you have credits to spend on GCloud to run these examples.

We have a first section with standard case like settting-up the environment, deploying managed and composite resources as helm chart... We also have a second section where we build our own application, a React.js user interface interacting with managed resources.

We are trying to stick to some nomenclature like:

- `Control Cluster`: The K8S cluster that hosts the Crossplane operator, in our case a [Kind](https://kind.sigs.k8s.io) cluster.
- `Managed Resources`: The managed infrastructure like cluster, database, IAM roles... created by the Control Cluster and running in the cloud.
- `Workload Cluster`: The K8S managed clusters created by the Control Cluster and running in the cloud.

## Standard Cases

You are expected to start from step 1 and follow-up step by step until the end. If you jump directly to a specific step, ensure your environment, including the shell environment variables, are set as expected.

Step 1: [Create GCloud Project](./docs/01-gcloud-project.md).

Step 2: [Create a Control Cluster](./docs/02-control-cluster.md).

Step 3: [GCP Provider on the Control cluster.](./docs/03-gcp-provider.md)

Step 4: [Create GCP managed resources](./docs/04-managed.md).

Step 5: [Deploy Helm releases](./docs/05-helm.md).

Step 6: [Deploy a Reference Platform](./docs/07-ref-platform.md).

Step 7: [Deploy a Configuration](./docs/06-configuration.md).

Step 8: [Deploy a Wordpress Cluster](./docs/08-wordpress-cluster.md).

Step 9: [Destroy](./docs/09-destroy.md).

How to [Troubleshoot](./docs/10-troubleshoot.md) if needed, hopefully not too much.

## Custom Web User Interface

Build and deploy a UI to insert and view a list of records from a Postgresql table deployed on GCP. Follow [these instructions](./docs/custom-ui.md) to get the following UI in your browser.

<img src="./res/users.png" style="max-width: 800px"/>
