import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
django.setup()

import subprocess
import sys

# Run makemigrations
print("Running makemigrations...")
subprocess.run([sys.executable, 'manage.py', 'makemigrations'])

# Run migrate
print("\nRunning migrate...")
subprocess.run([sys.executable, 'manage.py', 'migrate'])

print("\nMigrations completed!")
