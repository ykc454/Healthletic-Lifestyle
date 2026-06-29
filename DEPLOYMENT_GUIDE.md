# DEPLOYMENT_GUIDE.md

# Healthletic Lifestyle Flask API - Deployment Guide

## Project Overview

This project demonstrates a complete CI/CD pipeline for deploying a Flask REST API using GitHub Actions, Docker, Docker Hub, Kubernetes, and Helm.

The pipeline automatically performs the following tasks:

* Build and test the Flask application
* Build a Docker image
* Scan the Docker image for vulnerabilities using Trivy
* Push the Docker image to Docker Hub
* Deploy the application to a Kubernetes cluster using Helm
* Perform smoke testing after deployment
* Automatically rollback if deployment verification fails

---

# Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml
├── helm/
│   └── flask-api/
├── app.py
├── deploy.sh
├── Dockerfile
├── requirements.txt
├── test_app.py
└── DEPLOYMENT_GUIDE.md
```

---

# Prerequisites

Install the following software before deployment:

* Git
* Python 3.12
* Docker
* Kubernetes (Kind or Minikube)
* kubectl
* Helm
* GitHub Account
* Docker Hub Account

---

# GitHub Secrets

Configure the following repository secrets.

Navigate to:

```
GitHub Repository

↓

Settings

↓

Secrets and variables

↓

Actions

↓

New Repository Secret
```

Create the following secrets:

| Secret Name     | Description                                  |
| --------------- | -------------------------------------------- |
| DOCKER_USERNAME | Docker Hub username                          |
| DOCKER_PASSWORD | Docker Hub password or Personal Access Token |

---

# Docker Registry

Docker images are pushed to Docker Hub using the following format:

```
docker.io/<docker-username>/flask-api:v1.0.x
```

Example:

```
docker.io/yash/flask-api:v1.0.5
```

---

# GitHub Actions Workflow

The workflow automatically executes when:

* Push to the main branch
* Pull Request targeting the main branch

Pipeline Flow:

```
Code Push / Pull Request

↓

Checkout Repository

↓

Install Dependencies

↓

Run Unit Tests

↓

Build Docker Image

↓

Trivy Security Scan

↓

Login to Docker Hub

↓

Push Docker Image

↓

Deploy with Helm

↓

Smoke Test

↓

Rollback (if deployment fails)
```

---

# Docker Image Versioning

Each workflow execution creates a unique Docker image tag.

Example:

```
v1.0.1

v1.0.2

v1.0.3
```

The version is generated using the GitHub Actions run number.

---

# Manual Deployment

The deployment script supports manual deployments.

Usage:

```bash
./deploy.sh <environment> <version> <image_registry>
```

Example:

```bash
./deploy.sh dev v1.0.5 docker.io/yash
```

Supported environments:

* dev
* staging
* prod

The script validates all input parameters before deployment.

---

# Helm Deployment

Deployment is performed using:

```bash
helm upgrade --install flask-api ./helm/flask-api \
--set image.repository=<registry>/flask-api \
--set image.tag=<version> \
--wait
```

The `--wait` flag ensures Kubernetes resources become ready before deployment completes.

---

# Smoke Testing

After deployment, the application health endpoint is verified.

```
GET /health
```

Example:

```
http://localhost:5000/health
```

Expected Response:

```json
{
    "status": "healthy"
}
```

If the smoke test fails, the deployment is considered unsuccessful.

---

# Automatic Rollback

If deployment verification fails:

* Helm rollback is executed automatically.
* The previous stable release is restored.
* Failure is recorded in the deployment log.

Rollback command:

```bash
helm rollback flask-api
```

---

# Deployment Log

Deployment information is stored in:

```
deployment.log
```

The log contains:

* Deployment start time
* Application version
* Deployment status
* Smoke test result
* Rollback status (if executed)

---

# Troubleshooting

## Docker Image Push Failure

Possible causes:

* Incorrect Docker credentials
* Invalid Docker Hub repository
* Network connectivity issues

Solution:

* Verify DOCKER_USERNAME
* Verify DOCKER_PASSWORD
* Login manually:

```bash
docker login
```

---

## Kubernetes Deployment Failure

Possible causes:

* Kubernetes cluster not running
* Incorrect kubeconfig
* Helm chart configuration error

Verify cluster:

```bash
kubectl cluster-info
```

Check nodes:

```bash
kubectl get nodes
```

---

## Helm Deployment Error

Validate Helm chart:

```bash
helm lint ./helm/flask-api
```

Preview generated manifests:

```bash
helm template ./helm/flask-api
```

---

## Smoke Test Failure

Check application logs:

```bash
kubectl logs deployment/flask-api
```

Verify pods:

```bash
kubectl get pods
```

Verify services:

```bash
kubectl get svc
```

---

## Rollback Procedure

Rollback can be performed manually.

View release history:

```bash
helm history flask-api
```

Rollback:

```bash
helm rollback flask-api
```

Verify deployment:

```bash
kubectl get pods
```

---

# Testing the CI/CD Pipeline

1. Make changes to the application.
2. Commit the changes.
3. Push to GitHub.
4. GitHub Actions starts automatically.
5. Verify successful completion in the Actions tab.

To test failure handling:

* Modify a unit test so it fails.
* Push the changes.
* Observe that the workflow stops during the testing stage.
* No Docker image is pushed.
* No deployment occurs.

---

# Conclusion

This project demonstrates a complete CI/CD pipeline for a Flask application using GitHub Actions, Docker, Docker Hub, Kubernetes, and Helm. The workflow automates testing, image creation, security scanning, deployment, smoke testing, and rollback to ensure reliable and repeatable application delivery.
