# CloudPulse — DevOps CI/CD Project

A Flask web app deployed on AWS EKS using a complete automated CI/CD pipeline.

## What Happens When I Push Code?

```
git push → GitHub Webhook → Jenkins → Lint & Test → Docker Build → ECR Push → EKS Deploy → Email ✅
```

## Tools Used

| Tool | Purpose |
|------|---------|
| Python Flask | Simple web application |
| Docker | Containerize the app |
| GitHub | Source code + webhook trigger |
| Jenkins | CI/CD pipeline automation |
| Terraform | AWS infra as code (VPC, EKS, ECR, EC2) |
| Ansible Roles | Configure Jenkins server on EC2 |
| Kubernetes | Run & scale app containers on EKS |
| AWS (EKS, ECR, VPC) | Cloud platform |

## Project Structure

```
cloudpulse-app/                       ← GitHub Repo 1
├── app/
│   ├── main.py                    # Flask app
│   ├── Dockerfile                 # Container image
│   ├── .dockerignore
│   └── requirements.txt
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml            # 2 replicas, rolling update, probes
│   ├── service.yaml               # LoadBalancer
│   └── kustomization.yaml        # Apply all with: kubectl apply -k k8s/
├── jenkins/
│   └── Jenkinsfile                # Lint → Build → Push ECR → Deploy EKS
├── .gitignore
└── README.md

cloudpulse-infra/                     ← GitHub Repo 2
├── terraform/
│   ├── backend.tf                 # S3 remote state
│   ├── main.tf                    # Provider + modules
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   ├── bootstrap/                 # Step 1: Jenkins EC2 only
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── jenkins-ec2/           # EC2 + Security Group module
│   └── modules/                   # Step 3: Full infra via Jenkins
│       ├── vpc/                   # VPC, subnets, IGW, route table
│       ├── eks/                   # EKS cluster + node group + IAM
│       └── ecr/                   # ECR repository
├── ansible/
│   ├── setup-jenkins.yml          # Main playbook (uses roles)
│   ├── inventory.ini
│   ├── group_vars/
│   │   └── jenkins.yml
│   └── roles/
│       ├── java/                  # Install Java
│       ├── docker/                # Install Docker
│       ├── jenkins/               # Install & configure Jenkins
│       └── aws-tools/             # Install AWS CLI + kubectl
├── jenkins/
│   └── Jenkinsfile-infra          # plan → approval → apply/destroy
└── docs/
    ├── PROJECT_REPORT.md
    ├── SYNOPSIS.md
    ├── SETUP_GUIDE.md
    └── RUNBOOK.md                 # Exact commands to run everything
```

## Deployment Flow

```
Phase 1 — Bootstrap (run once locally)
  terraform/bootstrap → Jenkins EC2 banta hai

Phase 2 — Configure Jenkins
  ansible-playbook → Java, Docker, Jenkins, AWS CLI, kubectl install

Phase 3 — Infra via Jenkins
  Jenkins infra pipeline → VPC + EKS + ECR banta hai

Phase 4 — App Deploy
  git push → Jenkins auto-trigger → App live on EKS
```

## How to Demonstrate

1. App running: `http://<loadbalancer-url>` → `Hello from CloudPulse! Version 1.0`
2. Change version in `app/main.py` → `git push`
3. Show Jenkins building automatically
4. Refresh browser → `Version 2.0`
5. Show email notification received

## GitHub Webhook Setup

1. GitHub repo → Settings → Webhooks → Add webhook
2. **Payload URL:** `http://<jenkins-ip>:8080/github-webhook/`
3. **Content type:** `application/json`
4. **Events:** Just the push event
5. Jenkins job → Build Triggers → ✅ `GitHub hook trigger for GITScm polling`

## Quick Reference Commands

```bash
# Check running pods
kubectl get pods -n cloudpulse

# Check app URL
kubectl get svc -n cloudpulse

# Trigger infra pipeline manually
# Jenkins → cloudpulse-infra → Build with Parameters → apply

# Destroy everything (cost save karo!)
# Jenkins → cloudpulse-infra → Build with Parameters → destroy
```

> ⚠️ **EKS free nahi hai!** Demo ke baad turant destroy karo. See `docs/RUNBOOK.md` for full steps.

