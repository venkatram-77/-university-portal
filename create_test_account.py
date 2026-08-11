#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

from django.contrib.auth.models import User
from student_dashboard.models import Student, UserRole

username = 'johnsmith2026'
email = 'vra7702@gmail.com'
phone = '7702347703'
password = 'SecurePass2026!'

try:
    if User.objects.filter(username=username).exists():
        print(f"❌ Username '{username}' already exists")
    elif User.objects.filter(email=email).exists():
        print(f"❌ Email '{email}' already registered")
    elif Student.objects.filter(phone=phone).exists():
        print(f"❌ Phone '{phone}' already registered")
    else:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='John',
            last_name='Smith'
        )
        
        # Create UserRole
        UserRole.objects.create(user=user, role='student')
        
        # Create Student profile
        student = Student.objects.create(
            user=user,
            phone=phone,
            approved=False
        )
        
        print(f"✅ Account created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Status: Pending admin approval")
except Exception as e:
    print(f"❌ Error: {str(e)}")
