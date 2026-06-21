# University Portal

A Django-based university management system with role-based access for Admin, Faculty, and Students.

## Features

- Role-based login (Admin / Faculty / Student)
- Student & Faculty management
- Courses, Branches, Timetable
- Grades & Attendance tracking
- Fee management & payments
- Exam schedule
- Assignments
- Notice board & Events
- Forgot password with OTP (prints to console in dev)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/university-portal.git
cd university-portal/university_portal
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Create admin user
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Environment variables
Create a `.env` file in the `university_portal` folder or copy `.env.example` to `.env`:
```bash
cd university_portal
copy .env.example .env
```
Then update the values before running the app.

## Production / 24x7 Hosting
This project is ready for deployment on free hosts like Railway and PythonAnywhere.

### Recommended host: Railway (free tier)
1. Push your project to GitHub.
2. Go to https://railway.app and sign up or log in.
3. Create a new project and connect your GitHub repository.
4. For the service, use the existing `Procfile`:
   ```text
   web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn university_portal.wsgi:application --bind 0.0.0.0:$PORT
   ```
5. Set environment variables in Railway:
   - `DJANGO_SECRET_KEY` (a secure secret)
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<your-railway-domain>`
   - `RAILWAY_PUBLIC_DOMAIN=<your-railway-domain>`
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (optional for production email)
6. Deploy the project. Railway will install dependencies from `requirements.txt` and use `runtime.txt` to pick Python 3.13.

> Note: SQLite works for simple demos, but Railway's disk is ephemeral. For longer-term use, configure PostgreSQL with a managed database.

### Alternative free host: PythonAnywhere
1. Sign up at https://www.pythonanywhere.com/.
2. Clone your GitHub repo into your PythonAnywhere home directory.
3. Create a virtualenv with a supported Python version and install dependencies:
   ```bash
   python -m venv ~/myvenv
   source ~/myvenv/bin/activate
   pip install -r requirements.txt
   ```
4. In the PythonAnywhere web app settings, set:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<your-username>.pythonanywhere.com`
5. Set the web app entry point to `university_portal.wsgi:application`.
6. Run migrations and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
7. Create a superuser on PythonAnywhere if needed:
   ```bash
   python manage.py createsuperuser
   ```

### What is needed for 24/7 availability
- The app must be hosted on a server that stays online.
- Your local computer with `runserver` is not 24/7.
- Railway and PythonAnywhere can host the app continuously for free, as long as their free tier limits are acceptable.

## Live Website URL
- Local development: http://127.0.0.1:8000/
- Railway production: the URL Railway shows after deployment.
- PythonAnywhere production: `https://<your-username>.pythonanywhere.com`.

## Default Admin Login
- Username: `admin`
- Password: `admin123`

## Tech Stack
- Python 3.13
- Django 6.0.6
- SQLite (development)
