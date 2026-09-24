# Employee Task Management System — DevOps Learning Project

A deliberately simple 3-tier CRUD app (React + FastAPI + PostgreSQL) built
as a vehicle for practicing a full, realistic DevOps toolchain: Docker,
CI/CD (GitHub Actions + Jenkins), AWS (VPC/EC2/ALB/RDS/ECR), Terraform,
monitoring, and Kubernetes/EKS.

**The application is intentionally boring. The infrastructure is the point.**

---

## 1. Table of Contents

1. Architecture
2. Local Setup
3. Environment Variables
4. Docker Setup
5. Database Migrations
6. Testing
7. API Endpoints
8. Production Architecture (AWS)
9. DevOps Learning Path (start here if you're following along)

---

## 2. Architecture

### 2.1 Local architecture

```
 ┌─────────────┐        HTTP :8000        ┌──────────────┐
 │   Browser   │ ───────────────────────► │   FastAPI    │
 │ (React dev  │ ◄─────────────────────── │   (uvicorn)  │
 │  server)    │                           └──────┬───────┘
 └─────────────┘                                  │ SQL :5432
                                                   ▼
                                          ┌──────────────────┐
                                          │  PostgreSQL       │
                                          │  (local install)  │
                                          └──────────────────┘
```

### 2.2 Docker Compose architecture

```
                  Docker network: app-network
 ┌────────────┐   :80→3000   ┌────────────┐   :8000   ┌────────────┐
 │  Browser   │──────────────►│  frontend  │──────────►│  backend   │
 └────────────┘               │  (nginx)   │  fetch()   │ (FastAPI) │
                               └────────────┘           └─────┬──────┘
                                                                │ :5432
                                                                ▼
                                                        ┌───────────────┐
                                                        │   postgres    │
                                                        │ (no host port)│
                                                        └───────────────┘
```

### 2.3 AWS EC2 architecture (Phase 7-8)

```
 Internet
    │
    ▼
┌─────────────────────────── VPC ───────────────────────────┐
│  Public Subnet                                              │
│  ┌────────────────────┐                                     │
│  │ EC2 (docker compose)│  ports 80/443 not yet load-balanced │
│  └────────────────────┘                                     │
└──────────────────────────────────────────────────────────┘
```

### 2.4 AWS ALB + RDS architecture (Phase 9-12, "production target")

```
 Internet
    │  :443 (ACM cert)
    ▼
┌───────────────────────────────── VPC ─────────────────────────────────┐
│  Public Subnets (2 AZs)              Private Subnets (2 AZs)           │
│  ┌────────────┐                                                        │
│  │    ALB     │──── Target Group ────┐                                 │
│  └────────────┘                      ▼                                 │
│                              ┌────────────────┐      ┌───────────────┐ │
│                              │  EC2 app host   │─────►│  RDS Postgres │ │
│                              │ (docker compose)│ :5432│  (Multi-AZ)   │ │
│                              └────────────────┘      └───────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
      DNS: Route 53 app.example.com / api.example.com → ALB
```

### 2.5 Terraform architecture

```
terraform/environments/dev (or prod)
        │  wires together, passing outputs → inputs
        ▼
 ┌───────┬───────────────┬─────┬─────┬─────┬─────┬─────┐
 │  vpc  │ security-groups│ ecr │ iam │ ec2 │ alb │ rds │
 └───────┴───────────────┴─────┴─────┴─────┴─────┴─────┘
   each module = its own main.tf / variables.tf / outputs.tf
   state stored remotely in S3, locked via DynamoDB
```

### 2.6 Kubernetes architecture (Phase 16, local cluster)

```
 Namespace: employee-task
 ┌──────────────┐  ┌──────────────┐        ┌───────────────────┐
 │ Ingress       │  │ ConfigMap /  │        │ backend Deployment │──►HPA
 │ app.example.. │  │ Secret       │◄───────│  (2+ replicas)     │
 │ api.example.. │  └──────────────┘        └─────────┬──────────┘
 └──────┬────────┘                                    │
        │                ┌──────────────┐             ▼
        └───────────────►│ frontend Svc │      ┌───────────────┐
                          │ + Deployment │      │ postgres       │
                          └──────────────┘      │ StatefulSet    │
                                                 └───────────────┘
```

### 2.7 EKS architecture (Phase 17, future migration)

```
 Internet
    │
    ▼
 AWS Load Balancer (via AWS Load Balancer Controller)
    │
    ▼
 Kubernetes Ingress
    │
    ├──────────────┐
    ▼              ▼
 frontend Svc   backend Svc
    │              │
    ▼              ▼
 frontend Pods  backend Pods
                   │
                   ▼
                 RDS (unchanged -- still outside the cluster)
```

### 2.8 CI/CD pipeline

```
 GitHub push
    │
    ▼
 GitHub Actions / Jenkins
    │  test backend (pytest) ── build frontend (vite) ── docker build
    ▼
 Image scan (Trivy)
    │
    ▼
 Push to ECR (tagged with build number / git SHA -- never bare "latest")
    │
    ▼
 Deploy (SSH+compose today → kubectl/Helm after Phase 16)
    │
    ▼
 Health check (/health, /ready)
    │
    ▼
 CloudWatch / Prometheus + Grafana
```

---

## 3. Local Setup (Phase 1)

Requires Python 3.12+, Node 20+, and a local PostgreSQL (or skip to
Docker Compose in section 4 and avoid installing Postgres locally).

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:Harekrishna@123@localhost:5432/employee_task_db
alembic upgrade head
python seed.py
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Visit the frontend at `http://localhost:5173` and the API docs at
`http://localhost:8000/docs`.

---

## 4. Environment Variables

See `.env.example` at the repo root — it documents, variable by variable,
which value belongs in local dev, Docker Compose, Jenkins, AWS, and
Kubernetes. Never commit a populated `.env`; it's already git-ignored.

---

## 5. Docker Setup (Phase 2)

```bash
cp .env.example .env      # edit values as needed
docker compose up -d --build
docker compose ps
docker compose logs -f backend
docker compose down       # add -v to also wipe the postgres volume
```

For hot-reload during development:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

The frontend is served at `http://localhost:3000`, the API at
`http://localhost:8000`. PostgreSQL is **not** exposed to the host —
only the `backend` container can reach it, over the internal
`app-network`.

---

## 6. Database Migrations

Migrations use Alembic. Tables are **never** auto-created on startup —
you always run migrations explicitly, which keeps schema history
reviewable in Git and prevents accidental data loss.

```bash
cd backend

# Apply all migrations
alembic upgrade head

# Create a new migration after changing a model
alembic revision --autogenerate -m "add priority column to tasks"

# Roll back the last migration
alembic downgrade -1

# Load example data (safe to re-run)
python seed.py
```

---

## 7. Testing

```bash
cd backend
pytest -v
```

Tests run against an in-memory SQLite database (see `tests/conftest.py`),
so no Docker or real Postgres is required to run them, and CI stays fast.
Both `.github/workflows/ci.yml` and `jenkins/Jenkinsfile` fail the build
if any test fails.

---

## 8. API Endpoints

| Method | Path                    | Description                |
| ------ | ----------------------- | -------------------------- |
| GET    | `/health`             | Liveness check             |
| GET    | `/ready`              | Readiness check (DB)       |
| GET    | `/api/employees`      | List employees             |
| POST   | `/api/employees`      | Create employee            |
| GET    | `/api/employees/{id}` | Get one employee           |
| PUT    | `/api/employees/{id}` | Update employee            |
| DELETE | `/api/employees/{id}` | Delete employee            |
| GET    | `/api/tasks`          | List tasks                 |
| POST   | `/api/tasks`          | Create task                |
| GET    | `/api/tasks/{id}`     | Get one task               |
| PUT    | `/api/tasks/{id}`     | Update task (status, etc.) |
| DELETE | `/api/tasks/{id}`     | Delete task                |
| GET    | `/api/dashboard`      | Aggregate counts           |

Interactive docs: `/docs` (Swagger UI) and `/redoc`.

---

## 9. Production Architecture (AWS)

See diagrams 2.4 and 2.7 above. In short: ALB (HTTPS via ACM) → EC2
running Docker Compose today, migrating to ECS/EKS later → RDS
PostgreSQL in private subnets, never publicly reachable. Security
groups are layered (ALB → EC2 → RDS) so only the ALB is internet-facing.

---

## 10. DEVOPS LEARNING PATH

Work through these phases in order. Each phase builds on the last —
resist the urge to skip ahead to Kubernetes before EC2 is working; the
point of this repo is the incremental journey, not the destination.

| Phase | Goal                                                                                                        |
| ----- | ----------------------------------------------------------------------------------------------------------- |
| 1     | Run the application locally (`uvicorn` + `npm run dev`)                                                 |
| 2     | Run it with Docker Compose (`docker compose up -d`)                                                       |
| 3     | Push the code to GitHub                                                                                     |
| 4     | Set up GitHub Actions CI (`.github/workflows/ci.yml`)                                                     |
| 5     | Set up Jenkins and run`jenkins/Jenkinsfile` locally against Docker Hub or a dummy registry                |
| 6     | Create the two ECR repositories (`terraform/modules/ecr`, or manually first)                              |
| 7     | Deploy the containers to a single EC2 instance by hand                                                      |
| 8     | Create the VPC and Security Groups (`terraform/modules/vpc`, `security-groups`)                         |
| 9     | Move PostgreSQL to RDS (`terraform/modules/rds`) and repoint `DATABASE_URL`                             |
| 10    | Put an Application Load Balancer in front of EC2 (`terraform/modules/alb`)                                |
| 11    | Configure HTTPS with ACM (request/validate a cert, attach its ARN)                                          |
| 12    | Configure DNS with a real subdomain in Route 53                                                             |
| 13    | Convert everything above into Terraform end-to-end (`terraform/environments/dev`)                         |
| 14    | Add CloudWatch Logs/Metrics dashboards for EC2, ALB, RDS                                                    |
| 15    | Add Prometheus + Grafana for application-level metrics                                                      |
| 16    | Deploy to Kubernetes locally (minikube/kind) using`kubernetes/`                                           |
| 17    | Deploy to Amazon EKS                                                                                        |
| 18    | Implement Kubernetes Ingress with a real ingress controller / AWS Load Balancer Controller                  |
| 19    | Implement the Horizontal Pod Autoscaler (`kubernetes/hpa.yaml`) under load                                |
| 20    | Put together a production-style CI/CD pipeline that builds, scans, pushes, and deploys to EKS automatically |

By phase 20 you should be able to say, truthfully:

> "I built a containerized 3-tier application with a React frontend,
> FastAPI backend and PostgreSQL database. I implemented CI/CD using
> Jenkins/GitHub Actions, pushed container images to Amazon ECR,
> deployed on AWS, used an ALB for traffic management and HTTPS, moved
> the database to RDS, provisioned infrastructure using Terraform,
> implemented monitoring, and then migrated the workload to
> Kubernetes/EKS."

---

## 11. Project Structure

```
employee-task-devops/
├── frontend/            React + Vite UI (Dockerfile: multi-stage → Nginx)
├── backend/              FastAPI API + Alembic migrations + pytest suite
├── database/init/        Notes on DB bootstrapping (schema itself = Alembic)
├── docker-compose.yml    Local 3-tier stack
├── jenkins/Jenkinsfile   Full test→build→ECR→EC2 pipeline
├── .github/workflows/    GitHub Actions CI
├── terraform/
│   ├── modules/          vpc, security-groups, ecr, ec2, alb, rds, iam
│   └── environments/     dev, prod (wire modules together)
└── kubernetes/           namespace, configmap/secret, deployments,
                          services, ingress, hpa, postgres StatefulSet
```
# webhook test
