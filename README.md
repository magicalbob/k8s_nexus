# Nexus OSS Deployment on Kubernetes

This project provides configurations and scripts to deploy **Nexus OSS** on a Kubernetes cluster. Nexus is a repository manager that supports various artifact formats, including Docker images, Maven artifacts, and more.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment Configuration](#deployment-configuration)
- [Setting Up Persistent Storage](#setting-up-persistent-storage)
- [Services and Access](#services-and-access)
- [Proxy Configuration](#proxy-configuration)
- [Systemd Services](#systemd-services)
- [Notes](#notes)
- [License](#license)

## Prerequisites

Before deploying Nexus OSS, ensure you have the following:

- A Kubernetes cluster up and running.
- `kubectl` installed and configured to interact with your cluster.
- Sufficient resources (CPU and memory) on your cluster to run Nexus.
- Access to a Docker registry for pulling Nexus images.

## Deployment Configuration

The primary Kubernetes configuration file for deploying Nexus is `nexus.deploy.common.yml`. This file includes:

- A **Deployment** definition for Nexus OSS.
- A **PersistentVolumeClaim** for storage.
- Environment variables for proxy configuration and JVM options.

### To deploy Nexus OSS:

1. Apply the deployment configuration:
   ```sh
   ./install-nexus.sh
   ```
This script makes sure that the nexus namespace exists, creates the nexus service, adds am options, creates persistent volumes, and applies the nexus.dpeloy.commonyml manifest. It then waits for the deployment to be available before setting up port forwarding to give access to the nexus app.

Note that the install-nexus.sh will attempt to set up a kind cluster if a real kubernetes cluster is not available to it.

## Setting Up Persistent Storage

Nexus requires persistent storage for its data. Below are the files responsible for creating a PersistentVolume and a PersistentVolumeClaim:

- `nexus.deploy.pv.yml`: A specific PV configuration that points to a local storage path.
- `nexus.deploy.pv.kind.yml.template` and `nexus.deploy.pv.linux.yml.template`: Templates for creating PV with your desired settings.

You can create the PersistentVolume by tweaking these templates to fit your environment and applying them similarly:

```sh
kubectl apply -f nexus.deploy.pv.yml
```

Make sure to replace the path in the `local.path` with a valid path on the host node.

## Services and Access

A Kubernetes Service is created to expose Nexus:

- `nexus.svc.yml`: This Service file configures access to Nexus on port `8081`.

To create the service, run:
```sh
kubectl apply -f nexus.svc.yml
```

Once running, you can access Nexus at `http://<NODE_IP>:8081` where `<NODE_IP>` is the IP address of the node where Nexus is deployed.

## Proxy Configuration

The deployment configuration includes several environment variables for proxy settings. These are crucial if your cluster resides behind a proxy:

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `http_proxy`
- `https_proxy`

Adjust these values in the `nexus.deploy.common.yml` file if necessary.

## Systemd Services

Two systemd service files are provided to set up port forwarding:

1. **port8081.service**: For port forwarding Nexus service on `8081`.
   ```sh
   sudo cp systemd/port8081.service /etc/systemd/system/
   sudo systemctl enable port8081.service
   sudo systemctl start port8081.service
   ```

2. **port8085.service**: (Optional) For forwarding deployment directly on port `8085`.
   ```sh
   sudo cp systemd/port8085.service /etc/systemd/system/
   sudo systemctl enable port8085.service
   sudo systemctl start port8085.service
   ```

## Notes

- Make sure to monitor Nexus logs if you run into any issues:
  ```sh
  kubectl logs -f deployment/nexus -n newnexus
  ```
- Adjust resource requests and limits in the deployment file based on your cluster capacity.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
