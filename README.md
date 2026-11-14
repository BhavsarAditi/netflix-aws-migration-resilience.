# StreamFlix — Netflix-inspired Cloud Migration & Resilience Demo

This educational streaming-style application is built with Flask, PostgreSQL and Docker Compose. It supports the three cloud-computing deliverables: local baseline, EC2 Lift-and-Shift, and EC2 + Amazon RDS refactoring. Actual AWS resources must be created and tested in your own AWS account.

## Run locally on Windows — one click

1. Extract the ZIP.
2. Start Docker Desktop and wait for **Engine running**.
3. Open the extracted project folder.
4. Double-click **`RUN-WINDOWS.bat`**.
5. It starts PostgreSQL, synchronizes the configured database credentials with an existing local Docker volume, builds the app, runs migrations and opens `http://localhost:5000`.

If startup still fails, double-click `SHOW-LOGS.bat` and share the full output. The migration now prints the underlying Python/PostgreSQL exception.

## Important scripts
- `RUN-WINDOWS.bat` — start local app.
- `STOP-WINDOWS.bat` — stop local containers while preserving database volume.
- `SHOW-LOGS.bat` — print service status and migration/web/database logs.
- `scripts/repair-local-db.ps1` — align the local database role password and schema permissions with `.env`, using the configured `DB_USER` (not an assumed `postgres` role); it does not delete the database volume.

## Deliverables and guides
- `deployment/EC2-DEPLOY-GUIDE.md` — Lift-and-Shift on EC2 with local PostgreSQL.
- `deployment/RDS-REFACTOR-GUIDE.md` — refactor Flask to Amazon RDS PostgreSQL.
- `deployment/COST-AND-EFFORT-WORKSHEET.md` — record actual AWS estimates and team effort.
- `deployment/FINAL-SUBMISSION-CHECKLIST.md` — evidence checklist.
- `docs/architecture.md` — system architecture.
- `docs/case-study.md` — project case study.
- `docs/exercise-plan.md` — demonstration sequence.

## App features
Netflix-branded sign-in and registration, responsive streaming homepage, catalogue search, TV Shows and Movies browsing, title details, sample video player, account-scoped My List, playback history, PostgreSQL persistence, health endpoint and metrics endpoint.

## URLs
- Home: `http://localhost:5000`
- Health: `http://localhost:5000/health`
- Metrics: `http://localhost:5000/api/metrics`

## AWS security
Never expose PostgreSQL port 5432 to the public internet. Permit RDS inbound traffic from the EC2 security group only. Do not commit `.env`, passwords, SSH private keys or AWS credentials. Use Secrets Manager or secure environment injection for deployed secrets.

## Cost comparison
The included worksheet intentionally does not invent a bill. Actual cost depends on Region, EC2/RDS instance types, storage, backups, Multi-AZ, hours and data transfer. Use AWS Pricing Calculator and record the assumptions and estimates for both designs.

## Content and limitations
StreamFlix is an original educational demo brand, not Netflix. The catalogue is fictional and sample clips are public demo videos, not licensed films. External posters and video playback need internet access. This is not a production streaming service and does not implement DRM, paid subscriptions, CDN delivery or production-grade authentication.
