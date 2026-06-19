#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.chdir(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 50)
print("DATABASE SETUP AND MIGRATIONS")
print("=" * 50)

try:
    # Create migrations
    print("\n1. Creating migration files...")
    call_command('makemigrations', 'student_dashboard', verbosity=2)
    print("   [OK] Migrations created")
except Exception as e:
    print(f"   [ERROR] {e}")

try:
    # Apply migrations
    print("\n2. Applying migrations...")
    call_command('migrate', verbosity=2)
    print("   [OK] Migrations applied")
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "=" * 50)
print("Setup complete!")
print("=" * 50)
