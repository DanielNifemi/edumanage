from django.db import models
from accounts.models import CustomUser
from students.models import Student
from teachers.models import Teacher


class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    subject = models.CharField(max_length=100)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='ExamResult')


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()
    is_graded = models.BooleanField(default=False)
    graded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    grade_comment = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            # Prevent students from changing their exam scores
            original_instance = ExamResult.objects.get(pk=self.pk)
            if original_instance.score != self.score:
                self.score = original_instance.score
        super().save(*args, **kwargs)
