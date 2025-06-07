from django.db import models
from django.conf import settings


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=10)
    address = models.TextField()
    parent_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"


class AcademicRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    subject = models.CharField(max_length=50)
    grade = models.CharField(max_length=2)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject} ({self.semester}, {self.year})"
