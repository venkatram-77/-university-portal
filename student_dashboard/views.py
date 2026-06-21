import os
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Avg, Sum, Count, Q
from django.utils import timezone
from functools import wraps
from .models import (
    Student, Course, Branch, Grade, Attendance, Faculty, UserRole,
    FeePayment, Assignment, Timetable, ExamSchedule, Notice, Event, Fee
)


# ---------- Role Helpers ----------
def get_role(user):
    try:
        return user.role.role
    except Exception:
        if user.is_superuser:
            return 'admin'
        return 'student'


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if get_role(request.user) != 'admin':
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def faculty_or_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if get_role(request.user) not in ('admin', 'faculty'):
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ---------- Auth ----------
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        role_tab = request.POST.get('role_tab', 'student')
        user = authenticate(request, username=identifier, password=password)
        if user is None and identifier:
            if '@' in identifier:
                email_user = User.objects.filter(email__iexact=identifier).first()
                if email_user:
                    user = authenticate(request, username=email_user.username, password=password)
            if user is None:
                normalized = identifier.replace(' ', '').replace('-', '').replace('+', '')
                if normalized.isdigit():
                    student = Student.objects.filter(phone=identifier).first()
                    faculty = Faculty.objects.filter(phone=identifier).first()
                    if student:
                        user = authenticate(request, username=student.user.username, password=password)
                    elif faculty:
                        user = authenticate(request, username=faculty.user.username, password=password)
        if user is not None:
            actual_role = get_role(user)
            # Validate role tab matches actual role
            if role_tab == 'admin' and actual_role != 'admin':
                return render(request, 'login.html', {'error': 'You are not an admin.', 'active_tab': role_tab, 'username': identifier})
            if role_tab == 'faculty' and actual_role != 'faculty':
                return render(request, 'login.html', {'error': 'You are not registered as faculty.', 'active_tab': role_tab, 'username': identifier})
            if role_tab == 'student' and actual_role != 'student':
                return render(request, 'login.html', {'error': 'You are not registered as a student.', 'active_tab': role_tab, 'username': identifier})
            if actual_role == 'student':
                try:
                    student = Student.objects.get(user=user)
                    if not student.approved:
                        return render(request, 'login.html', {'error': 'Your student account is pending admin approval.', 'active_tab': role_tab, 'username': identifier})
                except Student.DoesNotExist:
                    pass
            if actual_role == 'faculty':
                try:
                    faculty = Faculty.objects.get(user=user)
                    if not faculty.approved:
                        return render(request, 'login.html', {'error': 'Your faculty account is pending admin approval.', 'active_tab': role_tab, 'username': identifier})
                except Faculty.DoesNotExist:
                    pass
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid username, email, phone or password.', 'username': identifier, 'active_tab': role_tab})
    return render(request, 'login.html', {'active_tab': 'student'})


# ---------- Forgot Password ----------
def forgot_password(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        # Find user by email or username
        user = None
        if '@' in identifier:
            user = User.objects.filter(email=identifier).first()
        else:
            user = User.objects.filter(username=identifier).first()
            if not user:
                # try phone via student/faculty
                try:
                    s = Student.objects.get(phone=identifier)
                    user = s.user
                except Student.DoesNotExist:
                    try:
                        f = Faculty.objects.get(phone=identifier)
                        user = f.user
                    except Faculty.DoesNotExist:
                        pass
        if not user:
            return render(request, 'forgot_password.html', {'error': 'No account found with that email, username or phone number.'})
        otp = str(random.randint(100000, 999999))
        request.session['reset_otp'] = otp
        request.session['reset_user_id'] = user.id
        # Send OTP via email (prints to console in dev)
        send_mail(
            'University Portal - Password Reset OTP',
            f'Your OTP for password reset is: {otp}\n\nValid for this session only.',
            'noreply@university.com',
            [user.email],
            fail_silently=True,
        )
        print(f'\n[PASSWORD RESET OTP] User: {user.username} | OTP: {otp}\n')
        return redirect('verify_otp')
    return render(request, 'forgot_password.html')


def verify_otp(request):
    if 'reset_otp' not in request.session:
        return redirect('forgot_password')
    if request.method == 'POST':
        entered = request.POST.get('otp', '').strip()
        if entered == request.session.get('reset_otp'):
            request.session['otp_verified'] = True
            return redirect('reset_password')
        return render(request, 'verify_otp.html', {'error': 'Invalid OTP. Please try again.'})
    return render(request, 'verify_otp.html')


def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        if len(password) < 4:
            return render(request, 'reset_password.html', {'error': 'Password must be at least 4 characters.'})
        if password != confirm:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})
        user = User.objects.get(id=request.session['reset_user_id'])
        user.set_password(password)
        user.save()
        del request.session['reset_otp']
        del request.session['reset_user_id']
        del request.session['otp_verified']
        return render(request, 'reset_password.html', {'success': True})
    return render(request, 'reset_password.html')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', 'student')
        secret_code = request.POST.get('secret_code', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        base_ctx = {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name, 'phone': phone, 'role': role, 'secret_code': secret_code}

        valid_roles = ('student', 'faculty', 'admin')
        if role not in valid_roles:
            return render(request, 'signup.html', {**base_ctx, 'error': 'Invalid role selected'})

        if not all([username, email, password, confirm_password]):
            return render(request, 'signup.html', {**base_ctx, 'error': 'All fields are required'})
        if password != confirm_password:
            return render(request, 'signup.html', {**base_ctx, 'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {**base_ctx, 'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {**base_ctx, 'error': 'Email already registered'})
        if phone and (Student.objects.filter(phone=phone).exists() or Faculty.objects.filter(phone=phone).exists()):
            return render(request, 'signup.html', {**base_ctx, 'error': 'Phone number already registered'})

        faculty_secret = os.getenv('FACULTY_SIGNUP_SECRET', 'FACULTY2026')
        admin_secret = os.getenv('ADMIN_SIGNUP_SECRET', 'ADMIN2026')
        if role == 'faculty' and secret_code != faculty_secret:
            return render(request, 'signup.html', {**base_ctx, 'error': 'Invalid faculty setup code'})
        if role == 'admin' and secret_code != admin_secret:
            return render(request, 'signup.html', {**base_ctx, 'error': 'Invalid admin setup code'})

        try:
            if role == 'admin':
                user = User.objects.create_superuser(username=username, email=email, password=password,
                                                     first_name=first_name, last_name=last_name)
                UserRole.objects.create(user=user, role='admin')
                login(request, user)
                return redirect('dashboard')
            user = User.objects.create_user(username=username, email=email, password=password,
                                            first_name=first_name, last_name=last_name)
            UserRole.objects.create(user=user, role=role)
            if role == 'faculty':
                Faculty.objects.create(user=user, phone=phone, approved=False)
                success = 'Faculty account created and is pending admin approval.'
            else:
                Student.objects.create(user=user, phone=phone, approved=False)
                success = 'Student account created and is pending admin approval.'
            return render(request, 'signup.html', {**base_ctx, 'success': success})
        except Exception as e:
            return render(request, 'signup.html', {**base_ctx, 'error': f'Error: {str(e)}'})
    return render(request, 'signup.html', {'role': 'student'})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# ---------- Dashboard (role-based) ----------
@login_required
def dashboard(request):
    role = get_role(request.user)

    if role == 'admin':
        total_students = Student.objects.count()
        total_courses = Course.objects.count()
        total_branches = Branch.objects.count()
        total_faculty = Faculty.objects.count()
        fee_paid_count = Student.objects.filter(fee_paid=True).count()
        fee_pending_count = total_students - fee_paid_count
        recent_students = Student.objects.select_related('user', 'branch').all()[:5]
        recent_notices = Notice.objects.filter(is_active=True).order_by('-posted_at')[:3]
        upcoming_events = Event.objects.filter(event_date__gte=timezone.now().date()).order_by('event_date')[:3]
        upcoming_exams = ExamSchedule.objects.filter(exam_date__gte=timezone.now().date()).order_by('exam_date')[:3]
        pending_assignments = Assignment.objects.filter(due_date__gte=timezone.now().date()).order_by('due_date')[:3]
        avg_score = Grade.objects.aggregate(avg=Avg('score'))['avg'] or 0
        branch_data = list(Branch.objects.annotate(student_count=Count('student')).values('name', 'student_count'))
        return render(request, 'dashboard_admin.html', {
            'total_students': total_students, 'total_courses': total_courses,
            'total_branches': total_branches, 'total_faculty': total_faculty,
            'fee_paid_count': fee_paid_count, 'fee_pending_count': fee_pending_count,
            'recent_students': recent_students, 'recent_notices': recent_notices,
            'upcoming_events': upcoming_events, 'upcoming_exams': upcoming_exams,
            'pending_assignments': pending_assignments, 'avg_score': round(avg_score, 1),
            'branch_data': branch_data,
        })

    elif role == 'faculty':
        try:
            faculty = Faculty.objects.get(user=request.user)
        except Faculty.DoesNotExist:
            faculty = None
        students = Student.objects.select_related('user', 'branch').all()
        recent_grades = Grade.objects.filter(entered_by=request.user).select_related('student__user').order_by('-date_recorded')[:5]
        recent_attendance = Attendance.objects.filter(marked_by=request.user).select_related('student__user', 'course').order_by('-date')[:5]
        upcoming_exams = ExamSchedule.objects.filter(exam_date__gte=timezone.now().date()).order_by('exam_date')[:3]
        pending_assignments = Assignment.objects.filter(
            created_by=request.user, due_date__gte=timezone.now().date()
        ).order_by('due_date')[:3]
        return render(request, 'dashboard_faculty.html', {
            'faculty': faculty,
            'total_students': students.count(),
            'recent_grades': recent_grades,
            'recent_attendance': recent_attendance,
            'upcoming_exams': upcoming_exams,
            'pending_assignments': pending_assignments,
        })

    else:  # student
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        grades = student.grades.all() if student else []
        attendances = student.attendances.select_related('course').all() if student else []
        fee_payments = student.fee_payments.all() if student else []
        avg_score = student.grades.aggregate(avg=Avg('score'))['avg'] or 0 if student else 0
        present_count = student.attendances.filter(status='present').count() if student else 0
        total_att = student.attendances.count() if student else 0
        att_pct = round(present_count / total_att * 100, 1) if total_att > 0 else 0
        upcoming_exams = ExamSchedule.objects.filter(exam_date__gte=timezone.now().date()).order_by('exam_date')[:3]
        notices = Notice.objects.filter(is_active=True).order_by('-posted_at')[:3]
        events = Event.objects.filter(event_date__gte=timezone.now().date()).order_by('event_date')[:3]
        assignments = Assignment.objects.filter(due_date__gte=timezone.now().date()).order_by('due_date')[:5]
        timetables = Timetable.objects.filter(branch=student.branch).select_related('course').order_by('day', 'start_time') if student and student.branch else []
        return render(request, 'dashboard_student.html', {
            'student': student, 'grades': grades, 'attendances': attendances,
            'fee_payments': fee_payments, 'avg_score': round(avg_score, 1),
            'att_pct': att_pct, 'upcoming_exams': upcoming_exams,
            'notices': notices, 'events': events, 'assignments': assignments,
            'timetables': timetables,
        })


# ---------- Admin: Faculty Management ----------
@admin_required
def faculty_list(request):
    faculty_list = Faculty.objects.select_related('user').all()
    return render(request, 'faculty_list.html', {'faculty_list': faculty_list})


@admin_required
def faculty_add(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        employee_id = request.POST.get('employee_id', '')
        department = request.POST.get('department', '')
        phone = request.POST.get('phone', '')
        if User.objects.filter(username=username).exists():
            return render(request, 'faculty_form.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        UserRole.objects.create(user=user, role='faculty')
        Faculty.objects.create(user=user, employee_id=employee_id, department=department, phone=phone, approved=True)
        return redirect('faculty_list')
    return render(request, 'faculty_form.html')


@admin_required
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.user.delete()
        return redirect('faculty_list')
    return render(request, 'faculty_confirm_delete.html', {'faculty': faculty})


@admin_required
def faculty_approve(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    faculty.approved = True
    faculty.save()
    return redirect('faculty_list')


@admin_required
def student_approve(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.approved = True
    student.save()
    return redirect('students')


# ---------- Students (all roles can view) ----------
@login_required
def students(request):
    students_list = Student.objects.all().select_related('user', 'branch')
    query = request.GET.get('q', '')
    branch_id = request.GET.get('branch')
    fee_status = request.GET.get('fee_status')
    if query:
        students_list = students_list.filter(
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) | Q(student_id__icontains=query)
        )
    if branch_id:
        students_list = students_list.filter(branch_id=branch_id)
    if fee_status == 'paid':
        students_list = students_list.filter(fee_paid=True)
    elif fee_status == 'pending':
        students_list = students_list.filter(fee_paid=False)
    return render(request, 'students.html', {
        'students': students_list, 'branches': Branch.objects.all(),
        'selected_branch': branch_id, 'selected_fee_status': fee_status, 'query': query,
    })


@admin_required
def student_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        branch_id = request.POST.get('branch')
        student_id = request.POST.get('student_id', '')
        phone = request.POST.get('phone', '')
        enrollment_date = request.POST.get('enrollment_date') or None
        fee_paid = request.POST.get('fee_paid') == 'on'
        if User.objects.filter(username=username).exists():
            return render(request, 'student_form.html', {'branches': Branch.objects.all(), 'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        UserRole.objects.create(user=user, role='student')
        branch = Branch.objects.get(id=branch_id) if branch_id else None
        Student.objects.create(user=user, branch=branch, student_id=student_id,
                               phone=phone, enrollment_date=enrollment_date, fee_paid=fee_paid, approved=True)
        return redirect('students')
    return render(request, 'student_form.html', {'branches': Branch.objects.all()})


@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.user.first_name = request.POST.get('first_name')
        student.user.last_name = request.POST.get('last_name')
        student.user.email = request.POST.get('email')
        student.user.save()
        branch_id = request.POST.get('branch')
        student.branch = Branch.objects.get(id=branch_id) if branch_id else None
        student.student_id = request.POST.get('student_id', '')
        student.phone = request.POST.get('phone', '')
        student.enrollment_date = request.POST.get('enrollment_date') or None
        student.fee_paid = request.POST.get('fee_paid') == 'on'
        student.save()
        return redirect('student_detail', pk=pk)
    return render(request, 'student_form.html', {'branches': Branch.objects.all(), 'student': student})


@admin_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.user.delete()
        return redirect('students')
    return render(request, 'student_confirm_delete.html', {'student': student})


@faculty_or_admin_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = student.grades.all()
    attendances = student.attendances.select_related('course').all()
    fee_payments = student.fee_payments.all()
    avg_score = grades.aggregate(avg=Avg('score'))['avg'] or 0
    total_paid = fee_payments.aggregate(total=Sum('amount'))['total'] or 0
    present_count = attendances.filter(status='present').count()
    total_count = attendances.count()
    attendance_pct = round((present_count / total_count * 100), 1) if total_count > 0 else 0
    return render(request, 'student_detail.html', {
        'student': student, 'grades': grades, 'attendances': attendances,
        'fee_payments': fee_payments, 'avg_score': round(avg_score, 1),
        'total_paid': total_paid, 'attendance_pct': attendance_pct,
    })


@login_required
def profile(request):
    role = get_role(request.user)
    student = None
    faculty = None
    if role == 'student':
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            pass
    elif role == 'faculty':
        try:
            faculty = Faculty.objects.get(user=request.user)
        except Faculty.DoesNotExist:
            pass
    return render(request, 'profile.html', {'student': student, 'faculty': faculty, 'role': role})


# ---------- Grades (faculty/admin enter, student views own) ----------
@faculty_or_admin_required
def grades(request):
    grades_list = Grade.objects.select_related('student__user').all()
    student_id = request.GET.get('student')
    if student_id:
        grades_list = grades_list.filter(student_id=student_id)
    return render(request, 'grades.html', {
        'grades': grades_list,
        'students': Student.objects.select_related('user').all(),
        'selected_student': student_id,
    })


@faculty_or_admin_required
def grade_add(request):
    if request.method == 'POST':
        Grade.objects.create(
            student_id=request.POST.get('student'),
            subject=request.POST.get('subject'),
            score=request.POST.get('score'),
            max_score=request.POST.get('max_score', 100),
            entered_by=request.user,
        )
        return redirect('grades')
    return render(request, 'grade_form.html', {'students': Student.objects.select_related('user').all()})


# ---------- Attendance (faculty/admin mark, student views own) ----------
@faculty_or_admin_required
def attendance(request):
    attendance_list = Attendance.objects.select_related('student__user', 'course').all()
    course_id = request.GET.get('course')
    date = request.GET.get('date')
    if course_id:
        attendance_list = attendance_list.filter(course_id=course_id)
    if date:
        attendance_list = attendance_list.filter(date=date)
    return render(request, 'attendance.html', {
        'attendance_list': attendance_list,
        'courses': Course.objects.all(),
        'selected_course': course_id,
        'selected_date': date,
    })


@faculty_or_admin_required
def attendance_mark(request):
    if request.method == 'POST':
        Attendance.objects.update_or_create(
            student_id=request.POST.get('student'),
            course_id=request.POST.get('course'),
            date=request.POST.get('date'),
            defaults={'status': request.POST.get('status', 'present'), 'marked_by': request.user}
        )
        return redirect('attendance')
    return render(request, 'attendance_form.html', {
        'students': Student.objects.select_related('user').all(),
        'courses': Course.objects.all(),
        'today': timezone.now().date(),
    })


# ---------- Fee ----------
@login_required
def fee_report(request):
    role = get_role(request.user)
    # Students see only their own fee page
    if role == 'student':
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        fee_payments = student.fee_payments.order_by('-payment_date') if student else []
        total_paid = fee_payments.aggregate(total=Sum('amount'))['total'] if student else 0
        return render(request, 'fee_student.html', {
            'student': student,
            'fee_payments': fee_payments,
            'total_paid': total_paid or 0,
        })
    # Admin / Faculty see full report
    total_students = Student.objects.count()
    fee_paid = Student.objects.filter(fee_paid=True).count()
    fee_pending = total_students - fee_paid
    pending_students = Student.objects.filter(fee_paid=False).select_related('user', 'branch')
    fee_payments = FeePayment.objects.select_related('student__user').order_by('-payment_date')[:20]
    total_collected = FeePayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'fee_report.html', {
        'fee_paid': fee_paid, 'fee_pending': fee_pending, 'total_students': total_students,
        'pending_students': pending_students, 'fee_payments': fee_payments,
        'total_collected': total_collected, 'role': role,
    })


@login_required
def fee_pay(request, pk):
    role = get_role(request.user)
    student = get_object_or_404(Student, pk=pk)
    # Students can only pay their own fee
    if role == 'student':
        try:
            own_student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return redirect('dashboard')
        if own_student.pk != student.pk:
            return redirect('fee_report')
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')
        FeePayment.objects.create(student=student, amount=amount, description=description)
        student.fee_paid = True
        student.save()
        return redirect('fee_report')
    return render(request, 'fee_pay.html', {'student': student, 'role': role})


# ---------- Courses & Branches ----------
@login_required
def courses(request):
    courses_list = Course.objects.all()
    branch_id = request.GET.get('branch')
    if branch_id:
        courses_list = courses_list.filter(branch_id=branch_id)
    return render(request, 'courses.html', {
        'courses': courses_list, 'branches': Branch.objects.all(), 'selected_branch': branch_id,
    })


@login_required
def branches(request):
    return render(request, 'branches.html', {'branches': Branch.objects.all().prefetch_related('courses')})


# ---------- Assignments ----------
@login_required
def assignments(request):
    if get_role(request.user) in ('admin', 'faculty'):
        assignments_list = Assignment.objects.select_related('course').order_by('due_date')
    else:
        try:
            student = Student.objects.get(user=request.user)
            course_ids = student.courses.values_list('id', flat=True)
            assignments_list = Assignment.objects.filter(
                Q(course__in=course_ids) | Q(course__isnull=True)
            ).order_by('due_date')
        except Student.DoesNotExist:
            assignments_list = Assignment.objects.none()
    return render(request, 'assignments.html', {'assignments': assignments_list, 'today': timezone.now().date()})


@faculty_or_admin_required
def assignment_add(request):
    if request.method == 'POST':
        Assignment.objects.create(
            title=request.POST.get('title'),
            course_id=request.POST.get('course') or None,
            description=request.POST.get('description', ''),
            due_date=request.POST.get('due_date'),
            created_by=request.user,
        )
        return redirect('assignments')
    return render(request, 'assignment_form.html', {'courses': Course.objects.all()})


# ---------- Timetable ----------
@login_required
def timetable(request):
    branch_id = request.GET.get('branch')
    timetables = Timetable.objects.select_related('branch', 'course').order_by('day', 'start_time')
    if branch_id:
        timetables = timetables.filter(branch_id=branch_id)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return render(request, 'timetable.html', {
        'timetables': timetables, 'branches': Branch.objects.all(),
        'selected_branch': branch_id, 'days': days,
    })


@faculty_or_admin_required
def timetable_add(request):
    if request.method == 'POST':
        Timetable.objects.create(
            branch_id=request.POST.get('branch'), course_id=request.POST.get('course'),
            day=request.POST.get('day'), start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'), room=request.POST.get('room', ''),
        )
        return redirect('timetable')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return render(request, 'timetable_form.html', {
        'branches': Branch.objects.all(), 'courses': Course.objects.all(), 'days': days,
    })


# ---------- Exam ----------
@login_required
def exam_schedule(request):
    exams = ExamSchedule.objects.select_related('course').order_by('exam_date')
    return render(request, 'exam_schedule.html', {'exams': exams, 'today': timezone.now().date()})


@faculty_or_admin_required
def exam_add(request):
    if request.method == 'POST':
        ExamSchedule.objects.create(
            course_id=request.POST.get('course'), exam_name=request.POST.get('exam_name'),
            exam_date=request.POST.get('exam_date'), start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'), room=request.POST.get('room', ''),
        )
        return redirect('exam_schedule')
    return render(request, 'exam_form.html', {'courses': Course.objects.all()})


# ---------- Notice ----------
@login_required
def notice_board(request):
    notices = Notice.objects.filter(is_active=True).order_by('-posted_at')
    return render(request, 'notice_board.html', {'notices': notices})


@faculty_or_admin_required
def notice_add(request):
    if request.method == 'POST':
        Notice.objects.create(title=request.POST.get('title'),
                              content=request.POST.get('content'), posted_by=request.user)
        return redirect('notice_board')
    return render(request, 'notice_form.html')


# ---------- Events ----------
@login_required
def events(request):
    return render(request, 'events.html', {
        'events': Event.objects.order_by('event_date'),
        'today': timezone.now().date(),
    })


@faculty_or_admin_required
def event_add(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'), description=request.POST.get('description', ''),
            event_date=request.POST.get('event_date'), location=request.POST.get('location', ''),
            created_by=request.user,
        )
        return redirect('events')
    return render(request, 'event_form.html')
