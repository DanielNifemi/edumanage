from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')  # Added default back
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.user_type}"

    def create_specific_profile(self):
        """
        Creates the specific profile (Student, Teacher, Staff) based on user_type
        """
        # Import models here to avoid circular imports
        from students.models import Student
        from teachers.models import Teacher
        from staff.models import StaffProfile

        if self.user_type == 'student':
            Student.objects.get_or_create(
                user=self.user,
                defaults={
                    'student_id': f"STU{self.user.id:06d}",
                    'date_joined': timezone.now().date()
                }
            )
        elif self.user_type == 'teacher':
            Teacher.objects.get_or_create(
                user=self.user,
                defaults={
                    'teacher_id': f"TCH{self.user.id:06d}",
                    'date_joined': timezone.now().date()
                }
            )
        elif self.user_type == 'staff':
            StaffProfile.objects.get_or_create(
                user=self.user,
                defaults={
                    'staff_id': f"STF{self.user.id:06d}",
                    'date_joined': timezone.now().date()
                }
            )
