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

print("=" * 60)
print("KEEPING ONLY Admin1 ACCOUNT")
print("=" * 60)

admin_accounts = User.objects.filter(is_superuser=True)
print(f"\nFound {admin_accounts.count()} admin accounts:")
for admin in admin_accounts:
    print(f"  - {admin.username} ({admin.email})")

admin1 = User.objects.filter(username='Admin1').first()
if not admin1:
    print("\n[ERROR] Admin1 account not found!")
    sys.exit(1)

print(f"\nKeeping: Admin1 ({admin1.email})")
print("Deleting other admin accounts...")

for admin in admin_accounts:
    if admin.username != 'Admin1':
        print(f"  [-] Deleting {admin.username}...")
        admin.delete()

print("\n" + "=" * 60)
print("COMPLETE! Only Admin1 remains")
print("=" * 60)

remaining = User.objects.filter(is_superuser=True)
print(f"\nRemaining admin users: {remaining.count()}")
for admin in remaining:
    print(f"  - {admin.username} ({admin.email})")
