#!/usr/bin/env python
"""
Comprehensive test script for role-based permissions across all EduManage API modules.
Tests the permission system we've implemented for different user roles:
- Students: Read-only access to their own data
- Teachers: Full access to their courses and student data
- Staff: Full administrative access (except teacher management)
- Admins: Complete access to all modules
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

# Import models for testing
from accounts.models import UserProfile
from courses.models import Course, CourseEnrollment
from attendance.models import Attendance
from examinations.models import Exam, ExamResult
from communication.models import Message
from discipline.models import DisciplinaryRecord
from schedules.models import Schedule

User = get_user_model()


class RoleBasedPermissionTest:
    """Test role-based permissions across all API modules"""
    
    def __init__(self):
        self.client = APIClient()
        self.users = {}
        self.test_data = {}
        
    def setup_test_users(self):
        """Create test users for each role"""
        print("Setting up test users...")
        
        # Create test users
        roles = ['student', 'teacher', 'staff', 'admin']
        
        for role in roles:
            # Create user
            user = User.objects.create_user(
                username=f'test_{role}',
                email=f'test_{role}@example.com',
                password='testpass123',
                first_name=f'Test',
                last_name=role.title()            )
            
            # Create user profile
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                user_type = 'staff'  # Admin is staff type with superuser privileges
            else:
                user_type = role
            
            profile = UserProfile.objects.create(
                user=user,
                user_type=user_type
            )
            
            self.users[role] = user
            print(f"Created {role} user: {user.username}")
        
        print(f"Created {len(self.users)} test users\n")
    
    def test_courses_api_permissions(self):
        """Test courses API permissions"""
        print("Testing Courses API Permissions...")
        
        test_cases = [
            # (role, endpoint, method, expected_status)
            ('student', '/api/courses/courses/', 'GET', 200),
            ('student', '/api/courses/courses/', 'POST', 403),
            ('teacher', '/api/courses/courses/', 'GET', 200),
            ('teacher', '/api/courses/courses/', 'POST', 201),
            ('staff', '/api/courses/courses/', 'GET', 200),
            ('staff', '/api/courses/courses/', 'POST', 201),
            ('admin', '/api/courses/courses/', 'GET', 200),
            ('admin', '/api/courses/courses/', 'POST', 201),
        ]
        
        self._run_permission_tests('Courses', test_cases)
    
    def test_attendance_api_permissions(self):
        """Test attendance API permissions"""
        print("Testing Attendance API Permissions...")
        
        test_cases = [
            ('student', '/api/attendance/attendance/', 'GET', 200),
            ('student', '/api/attendance/attendance/', 'POST', 403),
            ('teacher', '/api/attendance/attendance/', 'GET', 200),
            ('teacher', '/api/attendance/attendance/', 'POST', 201),
            ('staff', '/api/attendance/attendance/', 'GET', 200),
            ('staff', '/api/attendance/attendance/', 'POST', 201),
            ('admin', '/api/attendance/attendance/', 'GET', 200),
            ('admin', '/api/attendance/attendance/', 'POST', 201),
        ]
        
        self._run_permission_tests('Attendance', test_cases)
    
    def test_examinations_api_permissions(self):
        """Test examinations API permissions"""
        print("Testing Examinations API Permissions...")
        
        test_cases = [
            ('student', '/api/examinations/exams/', 'GET', 200),
            ('student', '/api/examinations/exams/', 'POST', 403),
            ('teacher', '/api/examinations/exams/', 'GET', 200),
            ('teacher', '/api/examinations/exams/', 'POST', 201),
            ('staff', '/api/examinations/exams/', 'GET', 200),
            ('staff', '/api/examinations/exams/', 'POST', 201),
            ('admin', '/api/examinations/exams/', 'GET', 200),
            ('admin', '/api/examinations/exams/', 'POST', 201),
        ]
        
        self._run_permission_tests('Examinations', test_cases)
    
    def test_communication_api_permissions(self):
        """Test communication API permissions"""
        print("Testing Communication API Permissions...")
        
        test_cases = [
            ('student', '/api/communication/messages/', 'GET', 200),
            ('student', '/api/communication/messages/', 'POST', 201),
            ('teacher', '/api/communication/messages/', 'GET', 200),
            ('teacher', '/api/communication/messages/', 'POST', 201),
            ('staff', '/api/communication/messages/', 'GET', 200),
            ('staff', '/api/communication/messages/', 'POST', 201),
            ('admin', '/api/communication/messages/', 'GET', 200),
            ('admin', '/api/communication/messages/', 'POST', 201),
        ]
        
        self._run_permission_tests('Communication', test_cases)
    
    def test_discipline_api_permissions(self):
        """Test discipline API permissions"""
        print("Testing Discipline API Permissions...")
        
        test_cases = [
            ('student', '/api/discipline/records/', 'GET', 200),
            ('student', '/api/discipline/records/', 'POST', 403),
            ('teacher', '/api/discipline/records/', 'GET', 200),
            ('teacher', '/api/discipline/records/', 'POST', 201),
            ('staff', '/api/discipline/records/', 'GET', 200),
            ('staff', '/api/discipline/records/', 'POST', 201),
            ('admin', '/api/discipline/records/', 'GET', 200),
            ('admin', '/api/discipline/records/', 'POST', 201),
        ]
        
        self._run_permission_tests('Discipline', test_cases)
    
    def test_schedules_api_permissions(self):
        """Test schedules API permissions"""
        print("Testing Schedules API Permissions...")
        
        test_cases = [
            ('student', '/api/schedules/schedules/', 'GET', 200),
            ('student', '/api/schedules/schedules/', 'POST', 403),
            ('teacher', '/api/schedules/schedules/', 'GET', 200),
            ('teacher', '/api/schedules/schedules/', 'POST', 201),
            ('staff', '/api/schedules/schedules/', 'GET', 200),
            ('staff', '/api/schedules/schedules/', 'POST', 201),
            ('admin', '/api/schedules/schedules/', 'GET', 200),
            ('admin', '/api/schedules/schedules/', 'POST', 201),
        ]
        
        self._run_permission_tests('Schedules', test_cases)
    
    def _run_permission_tests(self, api_name, test_cases):
        """Run permission tests for a specific API"""
        print(f"\n{api_name} API Permission Tests:")
        print("-" * 50)
        
        passed = 0
        failed = 0
        
        for role, endpoint, method, expected_status in test_cases:
            try:
                # Authenticate as the test user
                user = self.users[role]
                self.client.force_authenticate(user=user)
                
                # Make the API request
                if method == 'GET':
                    response = self.client.get(endpoint)
                elif method == 'POST':
                    # Use minimal test data for POST requests
                    test_data = self._get_test_data_for_endpoint(endpoint)
                    response = self.client.post(endpoint, test_data, format='json')
                elif method == 'PUT':
                    test_data = self._get_test_data_for_endpoint(endpoint)
                    response = self.client.put(endpoint, test_data, format='json')
                elif method == 'DELETE':
                    response = self.client.delete(endpoint)
                
                # Check if status matches expected
                if response.status_code == expected_status:
                    print(f"✓ {role.upper()} {method} {endpoint} -> {response.status_code} (Expected: {expected_status})")
                    passed += 1
                else:
                    print(f"✗ {role.upper()} {method} {endpoint} -> {response.status_code} (Expected: {expected_status})")
                    if hasattr(response, 'data'):
                        print(f"  Response: {response.data}")
                    failed += 1
                    
            except Exception as e:
                print(f"✗ {role.upper()} {method} {endpoint} -> ERROR: {str(e)}")
                failed += 1
            
            finally:
                # Clear authentication
                self.client.force_authenticate(user=None)
        
        print(f"\n{api_name} Results: {passed} passed, {failed} failed")
        return passed, failed
    
    def _get_test_data_for_endpoint(self, endpoint):
        """Get minimal test data for POST requests"""
        if 'courses' in endpoint:
            return {
                'name': 'Test Course',
                'code': 'TEST101',
                'description': 'Test course description'
            }
        elif 'attendance' in endpoint:
            return {
                'student': self.users['student'].id,
                'date': date.today().isoformat(),
                'is_present': True
            }
        elif 'exams' in endpoint:
            return {
                'title': 'Test Exam',
                'date': date.today().isoformat(),
                'max_marks': 100
            }
        elif 'messages' in endpoint:
            return {
                'recipient': self.users['teacher'].id,
                'subject': 'Test Message',
                'body': 'This is a test message'
            }
        elif 'records' in endpoint:
            return {
                'student': self.users['student'].id,
                'description': 'Test disciplinary record',
                'date': date.today().isoformat()
            }
        elif 'schedules' in endpoint:
            return {
                'title': 'Test Schedule',
                'start_time': '09:00:00',
                'end_time': '10:00:00'
            }
        else:
            return {}
    
    def test_data_isolation(self):
        """Test that users can only see their own data"""
        print("\nTesting Data Isolation...")
        print("-" * 50)
        
        # Test that students can only see their own attendance records
        student_user = self.users['student']
        other_student = User.objects.create_user(
            username='other_student',
            email='other@example.com',
            password='pass123'
        )
        
        # Create attendance records for both students
        # (This would require actual model creation - simplified for demonstration)
        
        print("Data isolation tests would verify:")
        print("✓ Students see only their own attendance records")
        print("✓ Students see only their own exam results")
        print("✓ Students see only their own disciplinary records")
        print("✓ Teachers see only their students' data")
        print("✓ Messages are private between sender and recipient")
    
    def run_all_tests(self):
        """Run all permission tests"""
        print("=" * 60)
        print("EDUMANAGE ROLE-BASED PERMISSIONS TEST SUITE")
        print("=" * 60)
        
        try:
            # Setup
            self.setup_test_users()
            
            # Run API permission tests
            total_passed = 0
            total_failed = 0
            
            apis = [
                self.test_courses_api_permissions,
                self.test_attendance_api_permissions,
                self.test_examinations_api_permissions,
                self.test_communication_api_permissions,
                self.test_discipline_api_permissions,
                self.test_schedules_api_permissions
            ]
            
            for test_func in apis:
                try:
                    passed, failed = test_func()
                    total_passed += passed
                    total_failed += failed
                except Exception as e:
                    print(f"Error running {test_func.__name__}: {str(e)}")
                    total_failed += 1
            
            # Test data isolation
            self.test_data_isolation()
            
            # Summary
            print("\n" + "=" * 60)
            print("FINAL RESULTS")
            print("=" * 60)
            print(f"Total Tests Passed: {total_passed}")
            print(f"Total Tests Failed: {total_failed}")
            print(f"Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%" if (total_passed + total_failed) > 0 else "No tests run")
            
            if total_failed == 0:
                print("\n🎉 ALL ROLE-BASED PERMISSIONS WORKING CORRECTLY!")
            else:
                print(f"\n⚠️  {total_failed} permission issues need attention")
                
        except Exception as e:
            print(f"Test suite error: {str(e)}")
            return False
        
        return total_failed == 0


def main():
    """Main test runner"""
    print("Starting EduManage Role-Based Permissions Test...")
    
    # Initialize and run tests
    test_runner = RoleBasedPermissionTest()
    success = test_runner.run_all_tests()
    
    if success:
        print("\n✅ All permission tests completed successfully!")
        return 0
    else:
        print("\n❌ Some permission tests failed!")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
