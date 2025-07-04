#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.models import CustomUser, UserProfile

def create_test_user():
    email = "simple@test.com"
    password = "test123"
    
    try:
        # Check if user already exists
        user = CustomUser.objects.get(email=email)
        print(f"User {email} already exists with ID: {user.id}")
        
        # Check if password works
        if user.check_password(password):
            print("Password is correct")
        else:
            print("Password is incorrect - updating password")
            user.set_password(password)
            user.save()
            print("Password updated")
            
    except CustomUser.DoesNotExist:
        print(f"Creating new user: {email}")
        user = CustomUser.objects.create_user(
            email=email,
            username="simple_user",
            password=password,
            first_name="Simple",
            last_name="User",
            is_active=True,
            role='teacher'  # Set as teacher to test schedule endpoints
        )
        print(f"User created with ID: {user.id}")
    
    # Ensure UserProfile exists
    try:
        profile = UserProfile.objects.get(user=user)
        print(f"UserProfile exists for user {user.email}")
    except UserProfile.DoesNotExist:
        print(f"Creating UserProfile for user {user.email}")
        profile = UserProfile.objects.create(
            user=user,
            phone_number="+1234567890",
            address="123 Test Street"
        )
        print(f"UserProfile created")
    
    print(f"User details:")
    print(f"  ID: {user.id}")
    print(f"  Email: {user.email}")
    print(f"  Username: {user.username}")
    print(f"  Role: {user.role}")
    print(f"  Is Active: {user.is_active}")
    print(f"  Profile ID: {profile.id if profile else 'None'}")

if __name__ == "__main__":
    create_test_user()
