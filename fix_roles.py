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
from student_dashboard.models import UserRole, Student, Faculty

print("=" * 60)
print("FIXING ROLE ASSIGNMENTS FOR ALL USERS")
print("=" * 60)

# 1. Fix superusers - should all be admin
superusers = User.objects.filter(is_superuser=True)
print(f"\nFound {superusers.count()} superusers")
for user in superusers:
    role_entry, created = UserRole.objects.get_or_create(user=user, defaults={'role': 'admin'})
    if created:
        print(f"  [+] Created admin role for {user.username}")
    elif role_entry.role != 'admin':
        role_entry.role = 'admin'
        role_entry.save()
        print(f"  [+] Updated {user.username} role to admin")
    else:
        print(f"  [OK] {user.username} already has admin role")

# 2. Fix students - should have 'student' role
students = Student.objects.all()
print(f"\nFound {students.count()} students")
for student in students:
    role_entry, created = UserRole.objects.get_or_create(user=student.user, defaults={'role': 'student'})
    if created:
        print(f"  [+] Created student role for {student.user.username}")
    elif role_entry.role != 'student':
        role_entry.role = 'student'
        role_entry.save()
        print(f"  [+] Updated {student.user.username} role to student")

# 3. Fix faculty - should have 'faculty' role
faculty_list = Faculty.objects.all()
print(f"\nFound {faculty_list.count()} faculty")
for faculty in faculty_list:
    role_entry, created = UserRole.objects.get_or_create(user=faculty.user, defaults={'role': 'faculty'})
    if created:
        print(f"  [+] Created faculty role for {faculty.user.username}")
    elif role_entry.role != 'faculty':
        role_entry.role = 'faculty'
        role_entry.save()
        print(f"  [+] Updated {faculty.user.username} role to faculty")

# 4. Find orphaned users (no Student/Faculty profile)
print("\nChecking for orphaned users...")
users_with_role = User.objects.filter(role__isnull=False)
students_set = set(Student.objects.values_list('user_id', flat=True))
faculty_set = set(Faculty.objects.values_list('user_id', flat=True))
superuser_set = set(User.objects.filter(is_superuser=True).values_list('id', flat=True))

for user_id, role_str in users_with_role.values_list('id', 'role__role'):
    if role_str == 'student' and user_id not in students_set and user_id not in superuser_set:
        user = User.objects.get(id=user_id)
        print(f"  [!] Orphaned student user: {user.username} (no Student profile)")
    elif role_str == 'faculty' and user_id not in faculty_set and user_id not in superuser_set:
        user = User.objects.get(id=user_id)
        print(f"  [!] Orphaned faculty user: {user.username} (no Faculty profile)")

print("\n" + "=" * 60)
print("ROLE ASSIGNMENT COMPLETE!")
print("=" * 60)
