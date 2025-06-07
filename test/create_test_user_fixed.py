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
email = 'testuser@example.com'
password = 'testpass123'

user, created = User.objects.get_or_create(
    email=email,  # Use email as the unique identifier
    defaults={
        'username': username,
        'first_name': 'Test', 
        'last_name': 'User'
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f'Created user: {user.username}')
    
    # Create user profile
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
else:
    print(f'User already exists: {user.username}')

print(f'\nLogin credentials:')
print(f'Email: {email}')
print(f'Password: {password}')

# Also create admin user for testing
admin_user, admin_created = User.objects.get_or_create(
    email='admin@example.com',  # Use email as the unique identifier
    defaults={
        'username': 'admin',
        'first_name': 'Admin', 
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)

if admin_created:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f'\nCreated admin user: {admin_user.username}')
    
    # Create admin profile
    admin_profile, admin_profile_created = UserProfile.objects.get_or_create(
        user=admin_user, 
        defaults={
            'user_type': 'admin'
        }
    )
    if admin_profile_created:
        print(f'Created admin profile')
    
    print(f'\nAdmin credentials:')
    print(f'Email: admin@example.com')
    print(f'Password: admin123')
else:
    print(f'\nAdmin user already exists: {admin_user.username}')
