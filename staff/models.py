from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"


class LeaveRequest(models.Model):
    LEAVE_TYPES = (
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal Leave'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


class PerformanceEvaluation(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_given')
    date = models.DateField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField()
