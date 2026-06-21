from django.db import models
from django.contrib.auth.models import User


class Branch(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True, default='')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True)
    credits = models.IntegerField(default=0)
    def __str__(self):
        return self.name
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fee_paid = models.BooleanField(default=False)
    student_id = models.CharField(max_length=20, blank=True, default='')
    enrollment_date = models.DateField(null=True, blank=True, default=None)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    max_score = models.FloatField(default=100)
    date_recorded = models.DateField(auto_now_add=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"


class Attendance(models.Model):
    STATUS_CHOICES = [('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status}"


class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.student} - {self.amount}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Timetable(models.Model):
    DAYS = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
    ]
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='timetables')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.branch} - {self.course} - {self.day}"


class ExamSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_name = models.CharField(max_length=200)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.course} - {self.exam_name} - {self.exam_date}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.amount_due}"


class UserRole(models.Model):
    ROLE_CHOICES = [('admin', 'Admin'), ('faculty', 'Faculty'), ('student', 'Student')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty')
    employee_id = models.CharField(max_length=20, blank=True, default='')
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    joined_date = models.DateField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    courses = models.ManyToManyField(Course, blank=True, related_name='faculty_members')

    def __str__(self):
        return self.user.username
