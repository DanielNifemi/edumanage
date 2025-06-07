#!/usr/bin/env python
"""
Simple test script for role-based permissions across EduManage API modules.
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
import uuid

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

# Import models for testing
from accounts.models import UserProfile

User = get_user_model()


def main():
    """Main test runner"""
    print("Starting EduManage Role-Based Permissions Test...")
    print("=" * 60)
    print("EDUMANAGE ROLE-BASED PERMISSIONS TEST SUITE")
    print("=" * 60)
    
    client = APIClient()
    
    try:
        # Create unique test users to avoid conflicts
        timestamp = datetime.now().strftime("%H%M%S")
        
        # Clean up any existing test users
        User.objects.filter(email__contains='test_perms').delete()
        
        print("Setting up test users...")
        
        # Create test users for each role
        users = {}
        roles = ['student', 'teacher', 'staff', 'admin']
        
        for role in roles:
            # Create user
            user = User.objects.create_user(
                username=f'test_perms_{role}_{timestamp}',
                email=f'test_perms_{role}_{timestamp}@example.com',
                password='testpass123',
                first_name='Test',
                last_name=role.title()
            )
            
            # Set admin privileges for admin role
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                user_type = 'staff'  # Admin uses staff type with superuser privileges
            else:
                user_type = role
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                user_type=user_type
            )
            
            users[role] = user
            print(f"✓ Created {role} user: {user.username}")
        
        print(f"\nCreated {len(users)} test users successfully")
        
        # Test API endpoints
        print("\nTesting API Permissions...")
        print("-" * 50)
        
        # Define test cases: (role, endpoint, method, expected_status)
        test_cases = [
            # Courses API
            ('student', '/api/courses/courses/', 'GET', 200),
            ('student', '/api/courses/courses/', 'POST', 403),
            ('teacher', '/api/courses/courses/', 'GET', 200),
            ('teacher', '/api/courses/courses/', 'POST', 201),
            ('staff', '/api/courses/courses/', 'GET', 200),
            ('admin', '/api/courses/courses/', 'GET', 200),
            
            # Attendance API  
            ('student', '/api/attendance/attendance/', 'GET', 200),
            ('student', '/api/attendance/attendance/', 'POST', 403),
            ('teacher', '/api/attendance/attendance/', 'GET', 200),
            ('staff', '/api/attendance/attendance/', 'GET', 200),
            ('admin', '/api/attendance/attendance/', 'GET', 200),
            
            # Communication API
            ('student', '/api/communication/messages/', 'GET', 200),
            ('teacher', '/api/communication/messages/', 'GET', 200),
            ('staff', '/api/communication/messages/', 'GET', 200),
            ('admin', '/api/communication/messages/', 'GET', 200),
        ]
        
        passed = 0
        failed = 0
        
        for role, endpoint, method, expected_status in test_cases:
            try:
                # Authenticate as the test user
                user = users[role]
                client.force_authenticate(user=user)
                
                # Make the API request
                if method == 'GET':
                    response = client.get(endpoint)
                elif method == 'POST':
                    # Use minimal test data for POST requests
                    test_data = {}
                    if 'courses' in endpoint:
                        test_data = {
                            'name': f'Test Course {timestamp}',
                            'code': f'TEST{timestamp}',
                            'description': 'Test course description'
                        }
                    response = client.post(endpoint, test_data, format='json')
                
                # Check if status matches expected
                if response.status_code == expected_status:
                    print(f"✓ {role.upper()} {method} {endpoint} -> {response.status_code}")
                    passed += 1
                else:
                    print(f"✗ {role.upper()} {method} {endpoint} -> {response.status_code} (Expected: {expected_status})")
                    failed += 1
                    
            except Exception as e:
                print(f"✗ {role.upper()} {method} {endpoint} -> ERROR: {str(e)}")
                failed += 1
            
            finally:
                # Clear authentication
                client.force_authenticate(user=None)
        
        # Summary
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(f"Total Tests Passed: {passed}")
        print(f"Total Tests Failed: {failed}")
        print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%" if (passed + failed) > 0 else "No tests run")
        
        if failed == 0:
            print("\n🎉 ALL ROLE-BASED PERMISSIONS WORKING CORRECTLY!")
        else:
            print(f"\n⚠️  {failed} permission issues need attention")
        
        # Clean up test users
        print("\nCleaning up test users...")
        for user in users.values():
            user.delete()
        print("Test users cleaned up.")
        
        return failed == 0
        
    except Exception as e:
        print(f"Test suite error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    if success:
        print("\n✅ All permission tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some permission tests failed!")
        sys.exit(1)
