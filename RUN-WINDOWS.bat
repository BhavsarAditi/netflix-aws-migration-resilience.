@echo off
setlocal
title StreamFlix - Start local web app
cd /d "%~dp0"
echo.
echo  ============================================
echo       STREAMFLIX - LOCAL DEMO STARTUP
echo  ============================================
echo.
where docker >nul 2>nul
if errorlevel 1 (
  echo Docker was not found. Install Docker Desktop for Windows first:
  echo https://www.docker.com/products/docker-desktop/
  pause
  exit /b 1
)
docker info >nul 2>nul
if errorlevel 1 (
  echo Docker Desktop is installed but its engine is not running.
  echo Open Docker Desktop, wait until Engine running, then try again.
  pause
  exit /b 1
)
if not exist ".env" (
  echo .env is missing. Copy .env.example to .env and configure it.
  pause
  exit /b 1
)
echo [1/3] Starting PostgreSQL and synchronizing local DB credentials...
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\repair-local-db.ps1"
if errorlevel 1 (
  echo.
  echo Database repair did not complete. Run SHOW-LOGS.bat and share its output.
  pause
  exit /b 1
)
echo.
echo [2/3] Building and starting StreamFlix...
docker compose --env-file .env -f infrastructure\docker-compose.yml up -d --build
if errorlevel 1 (
  echo.
  echo Startup failed. Showing recent logs:
  docker compose --env-file .env -f infrastructure\docker-compose.yml logs --tail=100 migrate web db
  echo.
  echo Share the full output above for diagnosis.
  pause
  exit /b 1
)
echo.
echo [3/3] Checking application...
timeout /t 6 /nobreak >nul
start "" http://localhost:5000
echo.
echo StreamFlix should open at http://localhost:5000
echo Health check: http://localhost:5000/health
echo Keep Docker Desktop running while using the app.
pause
