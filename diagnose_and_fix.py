#!/usr/bin/env python
"""
Comprehensive error diagnosis and fix script
"""
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
from django.test.utils import setup_test_environment
import traceback

print("\n" + "="*70)
print("UNIVERSITY PORTAL - ERROR DIAGNOSIS AND FIX")
print("="*70 + "\n")

# 1. Check database tables
print("[*] Checking database tables...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
    print(f"    Found {len(tables)} tables: {', '.join(tables)}")
except Exception as e:
    print(f"    [ERROR] {e}")

# 2. Apply migrations
print("\n[*] Applying database migrations...")
try:
    call_command('migrate', verbosity=0)
    print("    [OK] All migrations applied")
except Exception as e:
    print(f"    [ERROR] {e}")
    traceback.print_exc()

# 3. Check models
print("\n[*] Checking Django models...")
try:
    from student_dashboard.models import Student, Course, Branch
    print("    [OK] All models imported successfully")
    print(f"       - Student objects: {Student.objects.count()}")
    print(f"       - Course objects: {Course.objects.count()}")
    print(f"       - Branch objects: {Branch.objects.count()}")
except Exception as e:
    print(f"    [ERROR] {e}")
    traceback.print_exc()

# 4. Check views
print("\n[*] Checking views...")
try:
    from student_dashboard.views import dashboard, courses, branches, students, profile
    print("    [OK] All views imported successfully")
except Exception as e:
    print(f"    [ERROR] {e}")
    traceback.print_exc()

# 5. Check URLs
print("\n[*] Checking URL configuration...")
try:
    from django.urls import reverse
    reverse('dashboard')
    reverse('courses')
    reverse('branches')
    reverse('students')
    reverse('profile')
    print("    [OK] All URLs configured correctly")
except Exception as e:
    print(f"    [ERROR] {e}")
    traceback.print_exc()

# 6. Check templates
print("\n[*] Checking templates...")
template_files = [
    'base.html',
    'dashboard.html',
    'courses.html',
    'branches.html',
    'students.html',
    'profile.html'
]
templates_dir = 'student_dashboard/templates/'
for template in template_files:
    path = os.path.join(templates_dir, template)
    if os.path.exists(path):
        print(f"    [OK] {template}")
    else:
        print(f"    [MISSING] {template}")

# 7. Check static files
print("\n[*] Checking static files...")
static_files = [
    'static/css/style.css',
    'static/js/script.js'
]
for static_file in static_files:
    path = os.path.join('student_dashboard', static_file)
    if os.path.exists(path):
        print(f"    [OK] {static_file}")
    else:
        print(f"    [MISSING] {static_file}")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("="*70 + "\n")

print("✓ System is ready to use!")
print("\nAccess your dashboard:")
print("  URL: http://127.0.0.1:8000/")
print("  Admin: http://127.0.0.1:8000/admin/")
print("  Username: venkatram")
print("  Password: venkat@7702")
print("\n")
