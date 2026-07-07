import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.chdir(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

from django.contrib.auth.models import User
from student_dashboard.models import UserRole

admins = [
    {'username': 'venkatram', 'email': 'venkatram@university.com', 'password': 'venkat@7702'},
    {'username': 'Admin1', 'email': 'admin1@university.com', 'password': 'AdminRAM'},
]

for admin in admins:
    username = admin['username']
    email = admin['email']
    password = admin['password']

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username, email, password)
        UserRole.objects.create(user=user, role='admin')
        print(f"Superuser '{username}' created successfully with admin role!")
    else:
        user = User.objects.get(username=username)
        if not UserRole.objects.filter(user=user).exists():
            UserRole.objects.create(user=user, role='admin')
            print(f"Superuser '{username}' already exists. Admin role assigned!")
        else:
            print(f"Superuser '{username}' already exists with role!")
