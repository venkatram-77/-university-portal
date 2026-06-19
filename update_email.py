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

# Update email for venkatram user
try:
    user = User.objects.get(username='venkatram')
    old_email = user.email
    user.email = 'vra7702@gmail.com'
    user.save()
    print("✓ Email updated successfully!")
    print(f"  Username: venkatram")
    print(f"  Old Email: {old_email}")
    print(f"  New Email: {user.email}")
except User.DoesNotExist:
    print("✗ User 'venkatram' not found!")
except Exception as e:
    print(f"✗ Error: {str(e)}")
