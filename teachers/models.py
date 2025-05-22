from django.db import models
from django.contrib.auth import get_user_model
from staff.models import StaffProfile
from django.utils import timezone

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    qualification = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default='General')
    years_of_experience = models.PositiveIntegerField(default=0)
    date_joined = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"

    def save(self, *args, **kwargs):
        if self.teacher_id == 'TEMP000':
            # Generate teacher ID based on current year and count
            year = timezone.now().year
            count = Teacher.objects.count() + 1
            self.teacher_id = f'T{year}{count:04d}'
        super().save(*args, **kwargs)


class Class(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic = models.CharField(max_length=200)
    youtube_link = models.URLField(blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.subject} - {self.class_group} - {self.date}"
