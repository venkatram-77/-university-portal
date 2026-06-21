#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_portal.settings')
import django
django.setup()

from django.contrib.auth.models import User
from student_dashboard.models import UserRole, Student, Faculty, Branch, Course

def create_user(username, email, password, role, approved=True, branch_name=None, course_codes=None):
    if User.objects.filter(username=username).exists():
        print(f"{username} already exists — skipping")
        user = User.objects.get(username=username)
        if role == 'student':
            assign_student_branch_and_courses(user, branch_name, course_codes)
        return
    if role == 'admin':
        user = User.objects.create_superuser(username=username, email=email, password=password,
                                             first_name=username)
    else:
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=username)
    UserRole.objects.create(user=user, role=role)
    if role == 'faculty':
        Faculty.objects.create(user=user, phone='', approved=approved)
    elif role == 'student':
        student = Student.objects.create(user=user, phone='', approved=approved)
        assign_student_branch_and_courses(user, branch_name, course_codes)
    print(f"Created {role}: {username} / {password} (approved={approved})")

def assign_student_branch_and_courses(user, branch_name, course_codes):
    if not branch_name and not course_codes:
        return
    try:
        student = user.student
    except Student.DoesNotExist:
        return
    if branch_name:
        branch = Branch.objects.filter(name=branch_name).first()
        if branch:
            student.branch = branch
        else:
            print(f"Warning: branch '{branch_name}' not found for student {user.username}")
    if course_codes:
        student.courses.clear()
        for code in course_codes:
            course = Course.objects.filter(code=code).first()
            if course:
                student.courses.add(course)
            else:
                print(f"Warning: course code '{code}' not found for student {user.username}")
    student.save()


def main():
    print("Creating demo branches and courses...")
    demo_branches = [
        ('Computer Science', 'Computer Science Department'),
        ('Mechanical Engineering', 'Mechanical Engineering Department'),
        ('Civil Engineering', 'Civil Engineering Department'),
    ]
    for name, desc in demo_branches:
        branch, created = Branch.objects.get_or_create(name=name, defaults={'description': desc})
        if created:
            print(f"Created branch: {name}")
        else:
            print(f"Branch already exists: {name} — skipping")

    demo_courses = [
        ('Intro to Programming', 'CS101', 'Computer Science', 'Basics of programming using Python', 4),
        ('Data Structures', 'CS201', 'Computer Science', 'Core data structures and algorithms', 4),
        ('Database Systems', 'CS301', 'Computer Science', 'Database design and SQL', 4),
        ('Thermodynamics', 'ME101', 'Mechanical Engineering', 'Introduction to thermodynamics', 3),
        ('Fluid Mechanics', 'CE201', 'Civil Engineering', 'Basics of fluid mechanics', 3),
    ]
    for name, code, branch_name, desc, credits in demo_courses:
        try:
            branch = Branch.objects.get(name=branch_name)
        except Branch.DoesNotExist:
            print(f"Branch {branch_name} not found for course {name}; skipping")
            continue
        course, created = Course.objects.get_or_create(name=name, branch=branch, defaults={'code': code, 'description': desc, 'credits': credits})
        if created:
            print(f"Created course: {name} ({code}) in {branch_name}")
        else:
            print(f"Course already exists: {name} — skipping")

    print("Creating demo users...")
    demo_accounts = [
        ('demo_admin', 'admin@example.com', 'AdminPass123!', 'admin', True, None, None),
        ('demo_faculty', 'faculty@example.com', 'FacPass123!', 'faculty', True, None, None),
        ('demo_faculty_pending', 'facpend@example.com', 'FacPend123!', 'faculty', False, None, None),
        ('demo_student_cs', 'student_cs@example.com', 'StuCS123!', 'student', True, 'Computer Science', ['CS101', 'CS201']),
        ('demo_student_db', 'student_db@example.com', 'StuDB123!', 'student', True, 'Computer Science', ['CS301']),
        ('demo_student_me', 'student_me@example.com', 'StuME123!', 'student', True, 'Mechanical Engineering', ['ME101']),
        ('demo_student_ce', 'student_ce@example.com', 'StuCE123!', 'student', True, 'Civil Engineering', ['CE201']),
        ('demo_student_cross', 'student_cross@example.com', 'StuCross123!', 'student', True, 'Mechanical Engineering', ['ME101', 'CS101']),
    ]
    for username, email, password, role, approved, branch_name, course_codes in demo_accounts:
        create_user(username, email, password, role, approved, branch_name, course_codes)
    print('Done creating demo data.')


if __name__ == '__main__':
    main()
