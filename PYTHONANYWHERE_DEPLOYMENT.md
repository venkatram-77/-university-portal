# PythonAnywhere Deployment Instructions

## Current Status
✓ Production-ready code ready for deployment
✓ Admin account: Admin1 / AdminRAM
✓ All students and faculty data cleared
✓ Server stability improved

## Step-by-Step Deployment

### 1. Update Code on PythonAnywhere

SSH into PythonAnywhere and update:

```bash
cd /home/[your_username]/NEW_PROJECT/university_portal

# Pull latest code from git (if using git)
git pull origin main

# Or manually upload files

# Create logs directory
mkdir -p logs

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

### 2. Update Web App Configuration

1. Go to: https://www.pythonanywhere.com/web_app_setup/
2. Select your web app
3. Click "Reload" button (this restarts the app)

### 3. Update WSGI Configuration

In PythonAnywhere Web app settings, use this WSGI file:

```python
# /var/www/[username]_pythonanywhere_com_wsgi.py
import sys
import os

path = '/home/[username]/NEW_PROJECT/university_portal'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'university_portal.settings'

# Load environment variables from .env
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(path)
load_dotenv(BASE_DIR / '.env')

# Set required environment variables for PythonAnywhere
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '.pythonanywhere.com')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 4. Set Environment Variables

In PythonAnywhere Web app settings, add to "Environment variables":

```
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
DJANGO_SECRET_KEY=[your_secret_key]
```

### 5. Database Configuration

PythonAnywhere uses MySQL by default. Update your .env:

```
DATABASE_URL=mysql://[username]:[password]@[username].mysql.pythonanywhere.com/[username]$database_name
```

Or add to settings.py:

```python
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
```

### 6. Static Files Configuration

In PythonAnywhere Web app settings:

```
URL: /static/
Directory: /home/[username]/NEW_PROJECT/university_portal/staticfiles
```

### 7. Test the Deployment

1. Visit: `https://yourusername.pythonanywhere.com`
2. Login with: Admin1 / AdminRAM
3. Check the admin dashboard

### 8. Enable Always-On (24/7 Uptime)

- Purchase "Always-on" subscription on PythonAnywhere
- Web apps will run 24/7 without sleeping
- Automatic restarts on errors

## Troubleshooting

### 500 Error
- Check error log: `/var/log/[username].pythonanywhere.com.error.log`
- Verify database connection
- Run migrations: `python manage.py migrate`

### Login Not Working
- Clear sessions: `python manage.py clearsessions`
- Check User table: `python manage.py dbshell`

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Check static URL and directory in Web app settings

## Quick Start Commands

```bash
# SSH into PythonAnywhere
ssh [username]@ssh.pythonanywhere.com

# Navigate to project
cd /home/[username]/NEW_PROJECT/university_portal

# Activate virtual environment (if using one)
source /home/[username]/.virtualenvs/[env_name]/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create admin if needed
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('Admin1', 'admin1@university.com', 'AdminRAM')
>>> exit()

# Check logs
tail -f /var/log/[username].pythonanywhere.com.error.log
```

## Final URL Structure

Your site will be available at:
- **URL:** https://yourusername.pythonanywhere.com
- **Admin URL:** https://yourusername.pythonanywhere.com/admin/
- **Login:** https://yourusername.pythonanywhere.com/login/

## Support

For PythonAnywhere issues:
- Help: https://www.pythonanywhere.com/help/
- Forums: https://www.pythonanywhere.com/community/

---
**Last Updated:** 2026-06-23
