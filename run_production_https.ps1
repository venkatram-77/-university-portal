param(
    [int]$Port = 8000,
    [string]$Host = "0.0.0.0"
)

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectDir "venv\Scripts\python.exe"
$CertFile = Join-Path $ProjectDir "cert.pem"
$KeyFile = Join-Path $ProjectDir "key.pem"

Set-Location -LiteralPath $ProjectDir

Write-Host "=== University Portal - Production HTTPS Server ===" -ForegroundColor Cyan
Write-Host "Starting..."

# Run migrations
Write-Host "[1/3] Running migrations..." -ForegroundColor Yellow
& $VenvPython manage.py migrate --noinput 2>&1 | Out-Null

# Collect static files
Write-Host "[2/3] Collecting static files..." -ForegroundColor Yellow
& $VenvPython manage.py collectstatic --noinput --clear 2>&1 | Out-Null

# Start uvicorn with SSL
Write-Host "[3/3] Starting uvicorn HTTPS server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Server: https://localhost:$Port/" -ForegroundColor Green
Write-Host "  Login:  Admin1 / AdminRAM" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

& $VenvPython -m uvicorn university_portal.asgi:application `
    --host $Host `
    --port $Port `
    --ssl-cert-file $CertFile `
    --ssl-key-file $KeyFile `
    --workers 4 `
    --loop auto `
    --http httptools `
    --log-level info `
    --access-log
