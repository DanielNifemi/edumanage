from django.db import models
from django.contrib.auth import get_user_model
from staff.models import StaffProfile

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Teacher(models.Model):
    staff_profile = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    qualification = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return self.staff_profile.user.get_full_name()


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
