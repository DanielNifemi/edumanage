from django.db import models
from django.conf import settings


class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.username} - {self.date} - {'Present' if self.is_present else 'Absent'}"


class AttendanceReport(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_reports')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    days_present = models.IntegerField()

    def __str__(self):
        return f"{self.student.username} - {self.start_date} to {self.end_date}"

    @classmethod
    def create_report(cls, student, start_date, end_date, total_days, days_present):
        return cls.objects.create(
            student=student,
            start_date=start_date,
            end_date=end_date,
            total_days=total_days,
            days_present=days_present
        )