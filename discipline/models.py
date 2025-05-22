from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()


class InfractionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.IntegerField(choices=[(1, 'Minor'), (2, 'Moderate'), (3, 'Severe')])

    def __str__(self):
        return self.name


class DisciplinaryAction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class DisciplinaryRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='disciplinary_records')
    infraction_type = models.ForeignKey(InfractionType, on_delete=models.CASCADE)
    date = models.DateField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_infractions')
    description = models.TextField()
    action_taken = models.ForeignKey(DisciplinaryAction, on_delete=models.SET_NULL, null=True, blank=True)
    action_date = models.DateField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.infraction_type} - {self.date}"


class BehaviorNote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='behavior_notes')
    date = models.DateField()
    noted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return f"{self.student} - {self.date}"
