@echo off
cd /d "%~dp0"
docker compose --env-file .env -f infrastructure\docker-compose.yml down
echo.
echo StreamFlix containers stopped. Your database volume is preserved.
pause
