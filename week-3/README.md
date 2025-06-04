# Week 3: Kubernetes and Ray Cluster Setup

## Prerequisites
- Docker Desktop (min 8GB RAM)
- Required CLI tools:
  ```bash
  brew install kubectl kind kustomize helm
  ```

## Quick Start

1. Navigate to the k8s directory:
   ```bash
   cd week-3/k8s/
   chmod +x setup_cluster.sh
   ./setup_cluster.sh
   ```

2. Verify deployment:
   ```bash
   kubectl get pods
   kubectl exec $(kubectl get pod -l ray.io/node-type=head -o jsonpath='{.items[0].metadata.name}') -- ray status
   ```

## Available Services
- Ray Dashboard: http://localhost:8265
- Ray Client: `ray://localhost:10001`
- Ray Serve: http://localhost:8000

## Running YOLO Training
```bash
cd yolo-cpu
pip install -r requirements
python submit_job.py
```

## Cluster Management
```bash
# Stop port forwarding
pkill -f 'kubectl port-forward.*raycluster-kuberay-head-svc'

# Clean up
helm uninstall raycluster kuberay-operator
kind delete cluster --name ray-cluster
```

## Optional Tools
- K8s Lens (https://k8slens.dev/) for cluster visualization
