#!/usr/bin/env python
"""
Quick test script to verify registration fixes
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.api.serializers import RegisterSerializer
from accounts.models import CustomUser

print("Testing Registration Fix...")
print("=" * 50)

# Test data for different user types
test_users = [
    {
        'username': 'testst1',
        'email': 'teststudent1@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'Student',
        'user_type': 'student'
    },
    {
        'username': 'testtch1',
        'email': 'testteacher1@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'Teacher',
        'user_type': 'teacher',
        'employee_id': 'TCH001',
        'department': 'Mathematics'
    },
    {
        'username': 'teststaff1',
        'email': 'teststaff1@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'Staff',
        'user_type': 'staff',
        'employee_id': 'STF001'
    }
]

# Test 1: Serializer validation
print("1. Testing RegisterSerializer validation...")
for user_data in test_users:
    print(f"   Testing {user_data['user_type']} registration...")
    serializer = RegisterSerializer(data=user_data)
    
    if serializer.is_valid():
        print(f"   ✅ {user_data['user_type']} data is valid")
        try:
            # Try to create the user
            user = serializer.save()
            print(f"   ✅ {user_data['user_type']} user created successfully: {user.username}")
            
            # Check if profile was created
            if hasattr(user, 'userprofile'):
                print(f"   ✅ UserProfile created: {user.userprofile.user_type}")
                
                # Check role-specific profile
                if user_data['user_type'] == 'student' and hasattr(user, 'student'):
                    print(f"   ✅ Student profile created: {user.student.student_id}")
                elif user_data['user_type'] == 'teacher' and hasattr(user, 'teacher'):
                    print(f"   ✅ Teacher profile created: {user.teacher.teacher_id}")
                elif user_data['user_type'] == 'staff' and hasattr(user, 'staffprofile'):
                    print(f"   ✅ Staff profile created: {user.staffprofile.staff_id}")
                else:
                    print(f"   ⚠️  Role-specific profile not found for {user_data['user_type']}")
            else:
                print(f"   ❌ UserProfile not created")
                
        except Exception as e:
            print(f"   ❌ Error creating {user_data['user_type']}: {str(e)}")
    else:
        print(f"   ❌ {user_data['user_type']} validation failed: {serializer.errors}")

print("\n" + "=" * 50)

# Test 2: API endpoint test
print("2. Testing API endpoint...")
try:
    # Test with a simple student registration
    api_test_data = {
        'username': 'apitest1',
        'email': 'apitest1@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'API',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    response = requests.post(
        'http://localhost:8000/api/auth/register/',
        json=api_test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.text[:200]}...")
    
    if response.status_code == 201:
        print("   ✅ API registration successful!")
    elif response.status_code == 400:
        print("   ⚠️  Validation error (check response for details)")
    else:
        print("   ❌ API registration failed")
        
except requests.exceptions.ConnectionError:
    print("   ⚠️  Django server not running on localhost:8000")
except Exception as e:
    print(f"   ❌ API test error: {str(e)}")

print("\nTest completed!")
