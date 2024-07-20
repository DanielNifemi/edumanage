from django.db import models
from teachers.models import Teacher, Class, Subject


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class DayOfWeek(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return self.get_day_display()


class Schedule(models.Model):
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    day = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['class_group', 'day', 'time_slot']

    def __str__(self):
        return f"{self.class_group} - {self.subject} - {self.day} - {self.time_slot}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title
