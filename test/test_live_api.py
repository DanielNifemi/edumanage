#!/usr/bin/env python
"""
Live API test for role-based permissions - tests actual running server.
"""

import os
import sys
import django
import requests
from datetime import datetime
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


def test_api_endpoints():
    """Test API endpoints with actual HTTP requests"""
    print("=" * 60)
    print("EDUMANAGE API LIVE TEST")
    print("=" * 60)
    
    # Base URL - assuming Django dev server is running on port 8000
    base_url = "http://localhost:8000"
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print(f"✓ Server is responding (status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running!")
        print("Please start the Django development server with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Create test users if they don't exist
    timestamp = datetime.now().strftime("%H%M%S")
    
    # Clean up any existing test users
    User.objects.filter(email__contains='live_test').delete()
    
    print("\nSetting up test users...")
    
    users = {}
    credentials = {}
    
    roles = ['student', 'teacher', 'staff', 'admin']
    
    for role in roles:
        username = f'live_test_{role}_{timestamp}'
        email = f'live_test_{role}_{timestamp}@example.com'
        password = 'testpass123'
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Live',
            last_name=role.title()
        )
        
        # Set admin privileges for admin role
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()
            user_type = 'staff'
        else:
            user_type = role
        
        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            user_type=user_type
        )
        
        users[role] = user
        credentials[role] = {'username': username, 'password': password}
        print(f"✓ Created {role} user: {username}")
    
    print(f"\nCreated {len(users)} test users")
    
    # Test authentication and API access
    print("\nTesting API Authentication and Permissions...")
    print("-" * 50)
    
    session = requests.Session()
    
    # Test cases: (role, endpoint, method, should_succeed)
    test_cases = [
        ('student', '/api/courses/courses/', 'GET', True),
        ('student', '/api/courses/courses/', 'POST', False),
        ('teacher', '/api/courses/courses/', 'GET', True),
        ('teacher', '/api/courses/courses/', 'POST', True),
        ('staff', '/api/courses/courses/', 'GET', True),
        ('admin', '/api/courses/courses/', 'GET', True),
        
        ('student', '/api/attendance/attendance/', 'GET', True),
        ('student', '/api/attendance/attendance/', 'POST', False),
        ('teacher', '/api/attendance/attendance/', 'GET', True),
        ('staff', '/api/attendance/attendance/', 'GET', True),
        
        ('student', '/api/communication/messages/', 'GET', True),
        ('teacher', '/api/communication/messages/', 'GET', True),
        ('staff', '/api/communication/messages/', 'GET', True),
    ]
    
    passed = 0
    failed = 0
    
    for role, endpoint, method, should_succeed in test_cases:
        try:
            # First, get CSRF token
            csrf_response = session.get(f"{base_url}/admin/login/")
            csrf_token = None
            if 'csrftoken' in session.cookies:
                csrf_token = session.cookies['csrftoken']
            
            # Login as the user
            login_data = {
                'username': credentials[role]['username'],
                'password': credentials[role]['password'],
                'csrfmiddlewaretoken': csrf_token
            }
            
            login_response = session.post(f"{base_url}/admin/login/", data=login_data)
            
            # Set headers for API request
            headers = {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json'
            }
            
            # Make API request
            if method == 'GET':
                response = session.get(f"{base_url}{endpoint}", headers=headers)
            elif method == 'POST':
                test_data = {}
                if 'courses' in endpoint:
                    test_data = {
                        'name': f'Live Test Course {timestamp}',
                        'code': f'LIVE{timestamp}',
                        'description': 'Live test course'
                    }
                response = session.post(f"{base_url}{endpoint}", 
                                      json=test_data, headers=headers)
            
            # Check result
            is_success = response.status_code in [200, 201]
            
            if should_succeed and is_success:
                print(f"✓ {role.upper()} {method} {endpoint} -> {response.status_code} (SUCCESS as expected)")
                passed += 1
            elif not should_succeed and not is_success:
                print(f"✓ {role.upper()} {method} {endpoint} -> {response.status_code} (BLOCKED as expected)")
                passed += 1
            else:
                expected = "SUCCESS" if should_succeed else "BLOCKED"
                actual = "SUCCESS" if is_success else "BLOCKED"
                print(f"✗ {role.upper()} {method} {endpoint} -> {response.status_code} (Expected: {expected}, Got: {actual})")
                failed += 1
            
            # Logout
            session.get(f"{base_url}/admin/logout/")
            
        except Exception as e:
            print(f"✗ {role.upper()} {method} {endpoint} -> ERROR: {str(e)}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("LIVE API TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests Passed: {passed}")
    print(f"Total Tests Failed: {failed}")
    print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%" if (passed + failed) > 0 else "No tests run")
    
    # Clean up test users
    print("\nCleaning up test users...")
    for user in users.values():
        user.delete()
    print("Test users cleaned up.")
    
    if failed == 0:
        print("\n🎉 ALL LIVE API PERMISSIONS WORKING CORRECTLY!")
        return True
    else:
        print(f"\n⚠️  {failed} API permission issues need attention")
        return False


def main():
    """Main test runner"""
    print("Starting EduManage Live API Permissions Test...")
    
    try:
        success = test_api_endpoints()
        return success
    except Exception as e:
        print(f"Live test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    if success:
        print("\n✅ Live API tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some live API tests failed!")
        sys.exit(1)
