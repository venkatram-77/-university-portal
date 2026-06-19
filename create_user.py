#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
os.chdir(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

from django.contrib.auth.models import User

# Create user if doesn't exist
if not User.objects.filter(username='venkatram').exists():
    user = User.objects.create_user(
        username='venkatram',
        email='venkatram@university.edu',
        password='Vra@7702',
        first_name='Venkat',
        last_name='Ram'
    )
    print("✓ User 'venkatram' created successfully!")
    print(f"  Email: {user.email}")
    print(f"  Name: {user.first_name} {user.last_name}")
else:
    # Update password if user exists
    user = User.objects.get(username='venkatram')
    user.set_password('Vra@7702')
    user.save()
    print("✓ User 'venkatram' already exists. Password updated!")

print("\n✓ You can now login with:")
print("  Username: venkatram")
print("  Password: Vra@7702")
