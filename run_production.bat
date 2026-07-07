@echo off
REM Production-ready server startup script for Windows

echo Starting University Portal Production Server...
echo.
echo ============================================

REM Create necessary directories
if not exist staticfiles mkdir staticfiles
if not exist media mkdir media
if not exist logs mkdir logs

REM Clean old pyc files
for /d /r . %%d in (__pycache__) do if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do del /q "%%f"

REM Run migrations
echo [1/4] Running database migrations...
python manage.py migrate --noinput

REM Collect static files
echo [2/4] Collecting static files...
python manage.py collectstatic --noinput --clear

REM Create superuser if needed
echo [3/4] Verifying admin account...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='Admin1').exists() or User.objects.create_superuser('Admin1', 'admin1@university.com', 'AdminRAM')"

REM Start Gunicorn
echo [4/4] Starting Gunicorn server...
echo.
echo ============================================
echo Server running on: http://0.0.0.0:8000
echo Login: Admin1 / AdminRAM
echo ============================================
echo.

REM Run Gunicorn
gunicorn university_portal.wsgi:application ^
    --bind 0.0.0.0:8000 ^
    --workers 4 ^
    --worker-class sync ^
    --timeout 90 ^
    --max-requests 1000 ^
    --max-requests-jitter 50 ^
    --keep-alive 5 ^
    --access-logfile - ^
    --error-logfile - ^
    --log-level info

pause
