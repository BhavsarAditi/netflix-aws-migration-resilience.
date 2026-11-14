# Deliverable 1 — Lift-and-Shift deployment on AWS EC2

This guide deploys the same containerized Flask application to an EC2 VM. The local Docker Compose stack is the baseline; the cloud VM deployment is a separate action and must be verified in your AWS account.

## Before starting
- Create an EC2 instance in your chosen AWS Region (Amazon Linux 2023 or Ubuntu LTS).
- Create/choose a security group allowing SSH (22) from your own IP and HTTP (80) from the intended test audience. Do not expose PostgreSQL port 5432 publicly.
- Connect using SSH and install Docker Engine + Docker Compose plugin using the official instructions for the chosen OS.
- Transfer the project ZIP to EC2 or clone your Git repository.

## Run on EC2 (single VM with local PostgreSQL for Lift-and-Shift)
1. Extract the project on EC2 and enter its root directory.
2. Create `.env` from `.env.example`; set a unique strong DB_PASSWORD.
3. Run `docker compose --env-file .env -f infrastructure/docker-compose.yml up -d --build`.
4. Check `docker compose --env-file .env -f infrastructure/docker-compose.yml ps`.
5. Check `curl -i http://localhost:5000/health` from EC2.
6. Browse `http://EC2_PUBLIC_IPV4/` only after applying the EC2 port mapping below or use the EC2 compose configuration.

For public HTTP on port 80 with local PostgreSQL, change the web port mapping in `infrastructure/docker-compose.yml` from `5000:5000` to `80:5000`, then recreate the stack. Alternatively use the RDS compose in the next guide for the refactored deployment.

## Evidence to capture
- EC2 instance details showing running state and instance type.
- SSH terminal showing Docker Compose services running.
- Browser showing the StreamFlix app at the EC2 public IPv4 address.
- `/health` response showing `database: connected`.
- Do not include private keys, passwords, or AWS access keys in screenshots.

## Important
A successful local run is not proof of EC2 deployment. Record the public IP, region, instance type, date and screenshots after testing.
