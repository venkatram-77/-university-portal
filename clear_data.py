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
from student_dashboard.models import Student, Faculty, UserRole

print("=" * 60)
print("CLEARING STUDENTS AND FACULTIES")
print("=" * 60)

# Count records to be deleted
students_count = Student.objects.count()
faculty_count = Faculty.objects.count()

print(f"\nFound {students_count} students to delete")
print(f"Found {faculty_count} faculty to delete")

if students_count > 0 or faculty_count > 0:
    confirm = input("\nAre you sure? This will delete all students and faculty users. Type 'YES' to confirm: ").strip()

    if confirm == 'YES':
        # Get all student users
        student_users = []
        for student in Student.objects.all():
            student_users.append(student.user)

        # Get all faculty users
        faculty_users = []
        for faculty in Faculty.objects.all():
            faculty_users.append(faculty.user)

        # Delete students
        Student.objects.all().delete()
        print(f"[+] Deleted {students_count} student records")

        # Delete faculty
        Faculty.objects.all().delete()
        print(f"[+] Deleted {faculty_count} faculty records")

        # Delete student users
        for user in student_users:
            user.delete()
        print(f"[+] Deleted {len(student_users)} student user accounts")

        # Delete faculty users
        for user in faculty_users:
            user.delete()
        print(f"[+] Deleted {len(faculty_users)} faculty user accounts")

        print("\n" + "=" * 60)
        print("CLEANUP COMPLETE!")
        print("=" * 60)

        # Show remaining users
        admin_users = User.objects.filter(is_superuser=True)
        print(f"\nRemaining admin users: {admin_users.count()}")
        for admin in admin_users:
            print(f"  - {admin.username} ({admin.email})")
    else:
        print("Cancelled!")
else:
    print("\nNo students or faculty to delete")
