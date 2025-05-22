from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
    staff_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100, default='Staff Member')
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)  # Making this optional
    date_joined = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True)  # Making this optional
    address = models.TextField(blank=True)  # Making this optional
    created_at = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add to use default
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.staff_id}"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = f"STF{self.user.id:06d}"
        super().save(*args, **kwargs)


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
