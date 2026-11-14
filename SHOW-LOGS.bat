@echo off
cd /d "%~dp0"
echo ===== SERVICE STATUS =====
docker compose --env-file .env -f infrastructure\docker-compose.yml ps -a
echo.
echo ===== MIGRATION / WEB / DATABASE LOGS =====
docker compose --env-file .env -f infrastructure\docker-compose.yml logs --no-color --tail=200 migrate web db
echo.
pause
