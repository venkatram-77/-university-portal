import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from student_dashboard.models import UserRole, Student, Faculty, Branch, Course

print("Running migrations...")
call_command('migrate', '--run-syncdb', verbosity=0)
print("Migrations done.")

# Admin
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@university.com', 'admin123')
    UserRole.objects.get_or_create(user=u, defaults={'role': 'admin'})
    print("Admin:   admin / admin123")
else:
    print("Admin already exists.")

# Branch + Course
branch, _ = Branch.objects.get_or_create(name='Computer Science', defaults={'description': 'CS Department'})
course, _ = Course.objects.get_or_create(name='Data Structures', defaults={'code': 'CS101', 'branch': branch, 'credits': 4})

# Faculty
if not User.objects.filter(username='faculty1').exists():
    u = User.objects.create_user('faculty1', 'faculty@university.com', 'faculty123',
                                 first_name='Dr. John', last_name='Smith')
    UserRole.objects.create(user=u, role='faculty')
    Faculty.objects.create(user=u, employee_id='FAC001', department='Computer Science', phone='9876543210')
    print("Faculty: faculty1 / faculty123")
else:
    print("Faculty already exists.")

# Student
if not User.objects.filter(username='student1').exists():
    u = User.objects.create_user('student1', 'student@university.com', 'student123',
                                 first_name='Alice', last_name='Johnson')
    UserRole.objects.create(user=u, role='student')
    s = Student.objects.create(user=u, branch=branch, student_id='STU001', phone='9123456789')
    s.courses.add(course)
    print("Student: student1 / student123")
else:
    print("Student already exists.")

print("\nSetup complete! Run: python manage.py runserver")
print("Open: http://127.0.0.1:8000/login/")
