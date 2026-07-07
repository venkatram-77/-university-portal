# University Portal - Production Deployment Guide

## Current Status
✓ Database cleaned (students & faculty removed)
✓ Admin account set to: **Admin1 / AdminRAM**
✓ Production settings configured
✓ Server stability improvements applied

## What Was Fixed

### 1. Server Stability Issues
- ✓ Changed DEBUG from True to False (production mode)
- ✓ Updated Gunicorn configuration with:
  - 4 worker processes
  - Max request limit (1000) with auto-restart
  - 90-second timeout per request
  - Proper error logging
  - Keep-alive connections

### 2. Production Security
- ✓ SSL redirect enabled (when deployed)
- ✓ Secure session cookies
- ✓ CSRF protection enhanced
- ✓ HSTS headers configured
- ✓ Database connection pooling

### 3. Database Improvements
- ✓ All student/faculty records cleared
- ✓ Only Admin1 admin account remains
- ✓ Session management configured
- ✓ Database pooling for concurrent connections

## Running Locally (Windows)

### Option 1: Using Batch Script (Recommended)
```bash
cd c:\Users\venka\Desktop\NEW PROJECT\university_portal
run_production.bat
```

### Option 2: Manual Start
```bash
cd c:\Users\venka\Desktop\NEW PROJECT\university_portal
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn university_portal.wsgi:application --bind 0.0.0.0:8000
```

Then open: **http://localhost:8000**

## Deployment Options

### Option A: Railway (Recommended - Easiest)
1. Push code to GitHub
2. Connect Railway to GitHub
3. Set environment variables in Railway
4. Deploy

### Option B: PythonAnywhere (Already Used)
1. Update source code
2. Reload web app
3. Configure to use Gunicorn

### Option C: Docker + Cloud (AWS/Azure/DigitalOcean)
1. Dockerfile already works with Procfile
2. Deploy to any containerized platform
3. Scale as needed

## Environment Variables Needed

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://...
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Admin Credentials
**Username:** Admin1
**Password:** AdminRAM

## Testing Commands

```bash
# Check database
python manage.py dbshell

# Create test data
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Check for errors
python manage.py check

# Run migrations
python manage.py migrate
```

## Monitoring 24/7 Uptime

### For Local/On-Premise:
- Use Windows Task Scheduler to restart if crashes
- Or use systemd (Linux) / launchd (Mac)

### For Cloud Deployment:
- Railway: Auto-restarts on crash
- PythonAnywhere: Always-on subscription
- Docker: Use restart policy

## Performance Tips

1. Enable database connection pooling ✓
2. Use Gunicorn with proper workers ✓
3. Compress static files ✓
4. Enable browser caching ✓
5. Use CDN for static files (optional)

## Troubleshooting

**Server keeps crashing:**
- Check logs: `tail -f logs/gunicorn.log`
- Increase timeout in Procfile
- Check memory usage

**Slow performance:**
- Check database queries
- Enable caching
- Increase Gunicorn workers

**Login issues:**
- Clear session cache: `python manage.py clearsessions`
- Check database connection
- Verify ALLOWED_HOSTS

---

**Last Updated:** 2026-06-23
**Version:** 1.0 Production Ready
