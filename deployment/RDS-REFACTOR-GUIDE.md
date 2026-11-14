# Deliverable 2 — Refactor the app to Amazon RDS PostgreSQL

This is the managed-database deployment. The Flask application uses environment variables for its DB connection, so the app container can connect to RDS without embedding credentials in source code.

## Create RDS PostgreSQL
1. In the same AWS Region/VPC as EC2, create an Amazon RDS for PostgreSQL DB instance.
2. Prefer private accessibility (not publicly accessible).
3. Configure an RDS security group with inbound TCP 5432 sourced only from the EC2 instance's security group.
4. Create the database and login user (use the values selected for DB_NAME and DB_USER).
5. Keep the master password private. Use AWS Secrets Manager or secure environment variables for deployment secrets.

## Configure the EC2 application
1. Copy `.env.rds.example` to `.env` on EC2 (do not commit it).
2. Set `DB_HOST` to the RDS endpoint (hostname only), `DB_PORT=5432`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.
3. Confirm EC2 can reach the RDS endpoint on port 5432. Do not open RDS to `0.0.0.0/0`.
4. From the project root, run:

```bash
docker compose --env-file .env -f deployment/docker-compose.rds.yml up -d --build
```

5. Verify:

```bash
docker compose --env-file .env -f deployment/docker-compose.rds.yml ps
curl -i http://localhost/health
```

6. Open `http://EC2_PUBLIC_IPV4/` and verify the app loads.
7. Add a title to My List or play a sample clip, then verify the event/data persists after restarting the web container.

## Evidence to capture
- RDS database status and engine/version.
- RDS security group inbound rule showing source is the EC2 security group (hide account identifiers if desired).
- EC2 environment variable names only (never reveal values).
- Docker Compose web and migration services running.
- Browser showing the app on EC2 public IPv4.
- `/health` showing `database: connected`.
- A persistence test after restarting the web container.

## Architecture distinction
- Lift-and-Shift: EC2 VM + PostgreSQL running in Docker on the same VM.
- Refactored: EC2 VM runs Flask; Amazon RDS runs PostgreSQL as a separate managed service.
