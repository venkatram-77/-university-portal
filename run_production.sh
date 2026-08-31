#!/bin/bash
# Production-ready server startup script

echo "Starting University Portal Production Server..."
echo "=============================================="

# Create necessary directories
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# Clean old pyc files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Run migrations
echo "[1/4] Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "[2/4] Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if needed
echo "[3/4] Verifying admin account..."
python manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from student_dashboard.models import UserRole
admin, created = User.objects.get_or_create(username='Admin1')
if created or not admin.is_superuser:
    admin.is_superuser = True
    admin.is_staff = True
    admin.email = 'admin1@university.com'
    admin.set_password('AdminRAM')
    admin.save()
    print("Created/updated Admin1")
else:
    print("Admin1 already exists")
UserRole.objects.get_or_create(user=admin, defaults={'role': 'admin'})
PYEOF

# Start Gunicorn with error handling
echo "[4/4] Starting Gunicorn server..."
echo ""
echo "=============================================="
echo "Server running on: 0.0.0.0:8000"
echo "=============================================="
echo ""

# Run Gunicorn with restart on crash
exec gunicorn university_portal.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 90 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --reload \
    --reload-extra-file "/app/student_dashboard/templates"
