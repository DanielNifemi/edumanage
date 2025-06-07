#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile

# Get the custom user model
User = get_user_model()

# Create test user
username = 'testuser'
email = 'test@example.com'
password = 'testpass123'

user, created = User.objects.get_or_create(
    username=username, 
    defaults={
        'email': email, 
        'first_name': 'Test', 
        'last_name': 'User'
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f'Created user: {user.username}')
    
    # Create user profile
    try:
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user, 
            defaults={
                'user_type': 'student'
            }
        )
        if profile_created:
            print(f'Created profile for user: {user.username}')
        else:
            print(f'Profile already exists for user: {user.username}')
    except Exception as e:
        print(f'Error creating profile: {e}')
        print('User created without profile')
else:
    print(f'User already exists: {user.username}')

print(f'\nLogin credentials:')
print(f'Username: {username}')
print(f'Password: {password}')
