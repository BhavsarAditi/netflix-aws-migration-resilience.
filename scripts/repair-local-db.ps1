$ErrorActionPreference = "Stop"
# Uses DB_USER from .env as the initial PostgreSQL superuser; existing volumes keep their original initialized role.
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
$compose = Join-Path $root "infrastructure\docker-compose.yml"

if (!(Test-Path $envFile)) { throw ".env file not found at $envFile" }
$vars = @{}
Get-Content $envFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and !$line.StartsWith("#") -and $line.Contains("=")) {
        $parts = $line.Split("=", 2)
        $vars[$parts[0].Trim()] = $parts[1].Trim()
    }
}
$dbUser = $vars["DB_USER"]
$dbName = $vars["DB_NAME"]
$dbPassword = $vars["DB_PASSWORD"]
if (!$dbUser -or !$dbName -or !$dbPassword) { throw "DB_NAME, DB_USER and DB_PASSWORD must be set in .env" }
if ($dbUser -notmatch '^[A-Za-z_][A-Za-z0-9_]*$' -or $dbName -notmatch '^[A-Za-z_][A-Za-z0-9_]*$') {
    throw "For this helper, DB_NAME and DB_USER must contain only letters, numbers and underscores."
}
$sqlPassword = $dbPassword.Replace("'", "''")
Write-Host "Checking local PostgreSQL service..."
docker compose --env-file $envFile -f $compose up -d db
if ($LASTEXITCODE -ne 0) { throw "Could not start PostgreSQL container." }

$ready = $false
for ($i=0; $i -lt 40; $i++) {
    $health = docker compose --env-file $envFile -f $compose ps --format json db 2>$null
    if ($health -match '"Health":"healthy"') { $ready = $true; break }
    Start-Sleep -Seconds 2
}
if (!$ready) {
    Write-Warning "Health status was not reported as healthy yet; attempting local admin connection anyway."
}

# The official PostgreSQL image creates POSTGRES_USER as its initial
# database superuser. In this project that user is normally netflix_user,
# not the literal role name "postgres".
$roleSql = "ALTER ROLE `"$dbUser`" WITH LOGIN PASSWORD '$sqlPassword';"
docker compose --env-file $envFile -f $compose exec -T -u postgres db psql -U $dbUser -d $dbName -v ON_ERROR_STOP=1 -c $roleSql
if ($LASTEXITCODE -ne 0) { throw "Could not synchronize database user password. Confirm DB_USER and DB_NAME match the initialized PostgreSQL volume." }

docker compose --env-file $envFile -f $compose exec -T -u postgres db psql -U $dbUser -d $dbName -v ON_ERROR_STOP=1 -c "ALTER SCHEMA public OWNER TO `"$dbUser`"; GRANT ALL ON SCHEMA public TO `"$dbUser`";"
if ($LASTEXITCODE -ne 0) { throw "Could not grant schema privileges." }
Write-Host "Database credentials and schema permissions are synchronized with .env." -ForegroundColor Green
