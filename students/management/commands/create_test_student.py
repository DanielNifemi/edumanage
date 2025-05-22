from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student
from accounts.models import UserProfile
from django.utils import timezone

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Creates a test student for development'

    def handle(self, *args, **kwargs):
        # Create user
        user, created = CustomUser.objects.get_or_create(
            username='teststudent',
            email='teststudent@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'Student',
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created new user'))
        
        # Create or get user profile
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'user_type': 'student'
            }
        )
        if profile_created:
            self.stdout.write(self.style.SUCCESS('Created user profile'))
        
        # Create student profile
        student, student_created = Student.objects.get_or_create(
            user=user,
            defaults={
                'student_id': 'STU001',
                'date_of_birth': timezone.now().date(),
                'grade': '10th',
                'address': 'Test Address',
                'parent_name': 'Test Parent',
                'parent_contact': '1234567890'
            }
        )
        if student_created:
            self.stdout.write(self.style.SUCCESS('Created student profile'))
        else:
            self.stdout.write(self.style.SUCCESS('Student already exists'))
