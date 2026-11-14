# StreamFlix Architecture

## Components
- Browser: responsive HTML/CSS/JavaScript streaming interface.
- Flask/Gunicorn: web routes and JSON API.
- PostgreSQL: catalogue, per-profile My List, playback events and health data.
- Docker Compose: runs PostgreSQL, one-time migration/seed service and web service.

## Startup flow
1. Compose starts PostgreSQL and waits for `pg_isready`.
2. The migration service runs `initialize_database()`, creating tables and inserting/updating the demo catalogue.
3. The web service starts Gunicorn on port 5000.
4. Browser requests `/`, `/api/catalog`, `/api/my-list` and `/api/history`.
5. UI actions call JSON endpoints; My List and playback events are stored in PostgreSQL.

## Resilience and observability
- PostgreSQL health check gates the migration service.
- Web container restarts unless stopped.
- `/health` and `/api/health` validate the database connection.
- `SHOW-LOGS.bat` and Docker Compose logs support diagnosis.
