# University Portal

A full-featured **University Management System** built with **Django**, providing role-based access for **Admin**, **Faculty**, and **Students** to manage academics, attendance, grades, fees, and communication all in one place.

## Features

### Role-Based Access
- Separate login tabs for Admin, Faculty, and Student
- Admin approval workflow for new student & faculty accounts
- Role-specific dashboards and menus

### Academic Management
- Student & Faculty management
- Courses, Branches, and Departments
- Timetable & Exam schedules
- Assignments
- Grades & Attendance tracking

### Finance
- Fee management for students
- Fee payment tracking & reports (paid / pending)

### Communication
- Notice board
- Events
- Leave requests (apply / approve / reject)
- Forgot password with OTP verification

### User Experience
- Responsive, mobile-friendly UI
- Dashboard statistics and charts (Chart.js)
- Login via username, email, or phone number

## Tech Stack

- **Backend:** Python 3.13, Django 6.0.6
- **Web Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Database:** SQLite (default / dev) with PostgreSQL support via `DATABASE_URL`
- **Frontend:** Bootstrap 5, Font Awesome, Chart.js

## Demo / Default Accounts

| Role    | Username     | Password    |
|---------|--------------|-------------|
| Admin   | `venkatram`  | `venkat95`  |
| Faculty | `faculty1`   | `faculty123`|
| Student | `student1`   | `student123`|

> On Render, run `setup.py` or `python create_admin.py` during the build to create/reset default accounts.

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/venkatram-77/-university-portal.git
cd university-portal/university_portal
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
```

### 3. Apply migrations & load default data
```bash
python manage.py migrate
python setup.py
```

### 4. Run the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Environment Variables

Copy `.env.example` to `.env` and update the values before running:

| Variable                 | Description                                   |
|--------------------------|-----------------------------------------------|
| `DJANGO_SECRET_KEY`      | Secret key for Django (keep secret)           |
| `DJANGO_DEBUG`           | `True` for dev, `False` for production        |
| `DJANGO_ALLOWED_HOSTS`   | Comma-separated allowed hosts                 |
| `DATABASE_URL`           | PostgreSQL connection URL (optional)          |
| `EMAIL_HOST`             | SMTP host                                     |
| `EMAIL_PORT`             | SMTP port                                     |
| `EMAIL_USE_TLS`          | `True` / `False`                              |
| `EMAIL_HOST_USER`        | SMTP username                                 |
| `EMAIL_HOST_PASSWORD`    | SMTP password                                 |
| `FACULTY_SIGNUP_SECRET`  | Setup code required for faculty signup        |
| `ADMIN_SIGNUP_SECRET`    | Setup code required for admin signup          |

## Deployment

The project is pre-configured for **Render** via `render.yaml` (Blueprints) and also works on **Railway** and **PythonAnywhere**.

### Render (recommended)
1. Push this repository to GitHub.
2. Create a new **Blueprint** in Render and connect your GitHub repo.
3. Render picks up `render.yaml`, installs dependencies, runs migrations, and collects static files.
4. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and `DATABASE_URL` (use a free Render Postgres) in the service environment.

### Railway
Use the existing `Procfile`:
```
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn university_portal.wsgi:application --bind 0.0.0.0:$PORT
```
Set the same environment variables and a managed PostgreSQL database.

> **Important:** SQLite stores data in a local file. On free hosts the disk is ephemeral, so the database is **erased on every restart/redeploy**. For production, configure **PostgreSQL** via `DATABASE_URL`.

## Project Structure

```
university_portal/
├── university_portal/        # Project settings, URLs, WSGI/ASGI
├── student_dashboard/        # Core app (models, views, urls, templates, static)
├── templates/                # HTML templates
├── static/                   # Static assets (CSS/JS)
├── render.yaml               # Render Blueprint config
├── Procfile                  # Railway process config
├── requirements.txt          # Python dependencies
└── manage.py                 # Django management script
```

## License

This project is for educational/demonstration purposes.
