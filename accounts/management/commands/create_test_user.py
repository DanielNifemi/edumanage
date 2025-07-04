from django.core.management.base import BaseCommand
from accounts.models import CustomUser, UserProfile

class Command(BaseCommand):
    help = 'Create test user for development'

    def handle(self, *args, **options):
        email = 'simple@test.com'
        password = 'test123'
        
        # Delete existing user if exists
        CustomUser.objects.filter(email=email).delete()
        
        # Create new user
        user = CustomUser.objects.create_user(
            email=email,
            username='simple_user',
            password=password,
            first_name='Simple',
            last_name='User',
            is_active=True
        )
        
        # Create UserProfile
        profile = UserProfile.objects.create(
            user=user,
            user_type='teacher'
        )
        
        # Create the specific teacher profile
        profile.create_specific_profile()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user: {user.email} (ID: {user.id})')
        )
