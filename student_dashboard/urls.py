from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # Faculty (admin only)
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_add, name='faculty_add'),
    path('faculty/<int:pk>/delete/', views.faculty_delete, name='faculty_delete'),

    # Students
    path('students/', views.students, name='students'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Academic
    path('courses/', views.courses, name='courses'),
    path('branches/', views.branches, name='branches'),
    path('timetable/', views.timetable, name='timetable'),
    path('timetable/add/', views.timetable_add, name='timetable_add'),
    path('exams/', views.exam_schedule, name='exam_schedule'),
    path('exams/add/', views.exam_add, name='exam_add'),
    path('assignments/', views.assignments, name='assignments'),
    path('assignments/add/', views.assignment_add, name='assignment_add'),

    # Grades
    path('grades/', views.grades, name='grades'),
    path('grades/add/', views.grade_add, name='grade_add'),

    # Attendance
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),

    # Fees
    path('fees/', views.fee_report, name='fee_report'),
    path('fees/pay/<int:pk>/', views.fee_pay, name='fee_pay'),

    # Communication
    path('notices/', views.notice_board, name='notice_board'),
    path('notices/add/', views.notice_add, name='notice_add'),
    path('events/', views.events, name='events'),
    path('events/add/', views.event_add, name='event_add'),
]
