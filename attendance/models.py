from django.db import models
from django.conf import settings
from django.core.mail import send_mail


class SchoolCalendar(models.Model):
    date = models.DateField(unique=True)
    is_holiday = models.BooleanField(default=False)
    event_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {'Holiday' if self.is_holiday else 'School Day'}"


class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student.username} - {self.date} - {'Present' if self.is_present else 'Absent'}"

    @classmethod
    def mark_bulk_attendance(cls, date, student_data):
        attendances = []
        for student_id, is_present in student_data.items():
            attendance = cls(student_id=student_id, date=date, is_present=is_present)
            attendances.append(attendance)
        cls.objects.bulk_create(attendances)

    @classmethod
    def check_low_attendance(cls, student, threshold=0.75):
        total_days = cls.objects.filter(student=student).count()
        days_present = cls.objects.filter(student=student, is_present=True).count()

        if total_days > 0 and days_present / total_days < threshold:
            send_mail(
                'Low Attendance Alert',
                f'Your attendance is below {threshold * 100}%. Please improve your attendance.',
                'from@example.com',
                [student.email],
                fail_silently=False,
            )


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