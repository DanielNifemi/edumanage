#!/usr/bin/env python
"""
Debug script to test permission classes individually
"""

import os
import sys
import django
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from accounts.permissions import IsStudentUser, IsTeacherUser, IsStaffUser, IsAdminUser
from rest_framework.test import APIRequestFactory

User = get_user_model()

def test_permission_with_user():
    """Test a single user and permission"""
    print("Creating test student user...")
    
    # Clean up any existing test users
    User.objects.filter(username__startswith='debug_test').delete()
    
    # Create a test student user
    user = User.objects.create_user(
        username='debug_test_student',
        email='debug_test_student@example.com',
        password='testpass123'
    )
    
    # Create user profile
    profile = UserProfile.objects.create(
        user=user,
        user_type='student'
    )
    
    print(f"Created user: {user.username}")
    print(f"User profile type: {profile.user_type}")
    
    # Test the permission using APIRequestFactory
    factory = APIRequestFactory()
    request = factory.get('/')
    request.user = user
    
    print(f"\nRequest user: {request.user}")
    print(f"Request user type: {type(request.user)}")
    print(f"User is authenticated: {request.user.is_authenticated}")
    
    student_perm = IsStudentUser()
    result = student_perm.has_permission(request, None)
    
    print(f"\nIsStudentUser permission result: {result}")
    print(f"Expected: True")
    
    # Debug the permission logic
    print("\nDebugging permission logic:")
    print(f"request.user: {request.user}")
    print(f"request.user type: {type(request.user)}")
    print(f"user.is_authenticated: {request.user.is_authenticated}")
    
    try:
        user_profile = request.user.userprofile
        print(f"user.userprofile: {user_profile}")
        print(f"user.userprofile.user_type: {user_profile.user_type}")
        print(f"user_type == 'student': {user_profile.user_type == 'student'}")
    except Exception as e:
        print(f"Error accessing userprofile: {e}")
    
    # Clean up
    user.delete()
    
    return result

if __name__ == "__main__":
    test_permission_with_user()
