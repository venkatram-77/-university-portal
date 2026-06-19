#!/usr/bin/env python
"""
Comprehensive setup and error fix script for University Portal Django project
"""
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

from django.core.management import call_command
from django.db import connection
import traceback

def run_setup():
    print("\n" + "="*60)
    print("UNIVERSITY PORTAL - DATABASE & SETUP FIX")
    print("="*60 + "\n")

    tasks = [
        ("Creating migrations", lambda: call_command('makemigrations', 'student_dashboard', verbosity=1)),
        ("Applying migrations", lambda: call_command('migrate', verbosity=1)),
        ("Collecting static files", lambda: call_command('collectstatic', '--noinput', verbosity=1)),
    ]

    completed = 0
    failed = 0

    for task_name, task_func in tasks:
        try:
            print(f"[*] {task_name}...", end=" ", flush=True)
            task_func()
            print("[OK]")
            completed += 1
        except Exception as e:
            print(f"[ERROR]\n    {type(e).__name__}: {str(e)}")
            failed += 1
            traceback.print_exc()

    print("\n" + "="*60)
    print(f"Results: {completed} completed, {failed} failed")
    print("="*60 + "\n")

    if failed == 0:
        print("SUCCESS! All setup tasks completed.")
        print("\nYour dashboard is ready:")
        print("  - Dashboard: http://127.0.0.1:8000/")
        print("  - Admin: http://127.0.0.1:8000/admin/")
        print("  - Login: admin username 'venkatram' / password 'venkat@7702'")
    else:
        print("Some tasks failed. Please review the errors above.")

if __name__ == '__main__':
    try:
        run_setup()
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
