#!/usr/bin/env python
"""Apply database migrations"""
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

print("Applying database migrations...")
call_command('migrate', verbosity=2)
print("\nMigrations applied successfully!")
