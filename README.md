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

## Default Admin Login
- Username: `admin`
- Password: `admin123`

## Tech Stack
- Python 3.13
- Django 6.0.6
- SQLite (development)
