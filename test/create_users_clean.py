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
email = 'testuser@example.com'
password = 'testpass123'

user, created = User.objects.get_or_create(
    email=email,
    defaults={
        'username': 'testuser',
        'first_name': 'Test', 
        'last_name': 'User'
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f'Created user: {user.email}')
    
    # Create user profile
    profile, profile_created = UserProfile.objects.get_or_create(
        user=user, 
        defaults={
            'user_type': 'student'
        }
    )
    if profile_created:
        print(f'Created profile for user: {user.email}')
    else:
        print(f'Profile already exists for user: {user.email}')
else:
    print(f'User already exists: {user.email}')

print(f'\nStudent Login credentials:')
print(f'Email: {email}')
print(f'Password: {password}')

# Also create admin user for testing
admin_email = 'admin@example.com'
admin_password = 'admin123'

admin_user, admin_created = User.objects.get_or_create(
    email=admin_email,
    defaults={
        'username': 'admin',
        'first_name': 'Admin', 
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)

if admin_created:
    admin_user.set_password(admin_password)
    admin_user.save()
    print(f'\nCreated admin user: {admin_user.email}')
    
    # Create admin profile
    admin_profile, admin_profile_created = UserProfile.objects.get_or_create(
        user=admin_user, 
        defaults={
            'user_type': 'admin'
        }
    )
    if admin_profile_created:
        print(f'Created admin profile')
else:
    print(f'\nAdmin user already exists: {admin_user.email}')

print(f'\nAdmin Login credentials:')
print(f'Email: {admin_email}')
print(f'Password: {admin_password}')
