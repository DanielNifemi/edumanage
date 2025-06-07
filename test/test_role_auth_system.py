#!/usr/bin/env python3
"""
Test script for role-based authentication system
Tests both Django backend API and React frontend integration
"""

import os
import django
import requests
import json
import time
from django.test import TestCase
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.models import CustomUser, UserProfile
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile

def test_api_endpoints():
    """Test Django API endpoints for role-based authentication"""
    
    base_url = 'http://localhost:8000/api'
    
    print("🔧 Testing Django API Endpoints...")
    
    # Test 1: Check if backend is running
    try:
        response = requests.get(f"{base_url}/auth/csrf/", timeout=5)
        print(f"✅ Backend server is running: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend server not accessible: {e}")
        return False
    
    # Test 2: Test registration for each role
    test_users = [
        {
            "role": "student",
            "data": {
                "username": "test_student@example.com",
                "email": "test_student@example.com",
                "password": "TestPass123!",
                "password_confirm": "TestPass123!",
                "first_name": "Test",
                "last_name": "Student",
                "user_type": "student",
                "student_id": "STU001"
            }
        },
        {
            "role": "teacher",
            "data": {
                "username": "test_teacher@example.com",
                "email": "test_teacher@example.com",
                "password": "TestPass123!",
                "password_confirm": "TestPass123!",
                "first_name": "Test",
                "last_name": "Teacher",
                "user_type": "teacher",
                "employee_id": "TCH001",
                "department": "Mathematics"
            }
        },
        {
            "role": "staff",
            "data": {
                "username": "test_staff@example.com",
                "email": "test_staff@example.com", 
                "password": "TestPass123!",
                "password_confirm": "TestPass123!",
                "first_name": "Test",
                "last_name": "Staff",
                "user_type": "staff",
                "employee_id": "STF001",
                "department": "Administration"
            }
        },
        {
            "role": "admin",
            "data": {
                "username": "test_admin@example.com",
                "email": "test_admin@example.com",
                "password": "TestPass123!",
                "password_confirm": "TestPass123!",
                "first_name": "Test",
                "last_name": "Admin",
                "user_type": "admin",
                "admin_code": "ADMIN123"
            }
        }
    ]
    
    # Clean up any existing test users
    for test_user in test_users:
        try:
            user = CustomUser.objects.get(email=test_user["data"]["email"])
            user.delete()
            print(f"🧹 Cleaned up existing {test_user['role']} user")
        except CustomUser.DoesNotExist:
            pass
    
    # Test registration for each role
    registered_users = []
    for test_user in test_users:
        try:
            response = requests.post(
                f"{base_url}/auth/register/",
                json=test_user["data"],
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                print(f"✅ {test_user['role'].title()} registration successful")
                registered_users.append(test_user)
            else:
                print(f"❌ {test_user['role'].title()} registration failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {test_user['role'].title()} registration error: {e}")
    
    # Test login for each registered user
    for test_user in registered_users:
        try:
            login_data = {
                "email": test_user["data"]["email"],
                "password": test_user["data"]["password"]
            }
            
            response = requests.post(
                f"{base_url}/auth/login/",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ {test_user['role'].title()} login successful")
                print(f"   User role: {user_data.get('user', {}).get('role', 'N/A')}")
            else:
                print(f"❌ {test_user['role'].title()} login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {test_user['role'].title()} login error: {e}")
    
    return True

def test_react_frontend():
    """Test if React frontend is accessible"""
    
    print("\n🖥️  Testing React Frontend...")
    
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ React frontend is running")
            
            # Test role selection page
            response = requests.get('http://localhost:5173/auth/role-selection', timeout=5)
            if response.status_code == 200:
                print("✅ Role selection page accessible")
            else:
                print(f"❌ Role selection page not accessible: {response.status_code}")
                
            return True
        else:
            print(f"❌ React frontend not accessible: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ React frontend not accessible: {e}")
        return False

def verify_database_state():
    """Verify database has correct role-based data"""
    
    print("\n📊 Verifying Database State...")
    
    # Check UserProfile counts by role
    for role, _ in UserProfile.USER_TYPES:
        count = UserProfile.objects.filter(user_type=role).count()
        print(f"   {role.title()} profiles: {count}")
    
    # Check specific profile models
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    staff_count = StaffProfile.objects.count()
    
    print(f"   Student records: {student_count}")
    print(f"   Teacher records: {teacher_count}")
    print(f"   Staff records: {staff_count}")
    
    # Check if profiles are properly linked
    total_users = CustomUser.objects.count()
    total_profiles = UserProfile.objects.count()
    
    print(f"   Total users: {total_users}")
    print(f"   Total profiles: {total_profiles}")
    
    if total_users == total_profiles:
        print("✅ All users have profiles")
    else:
        print("❌ Some users missing profiles")

def main():
    """Main test function"""
    
    print("🚀 Starting Role-Based Authentication System Test")
    print("=" * 60)
    
    # Test Django backend API
    api_success = test_api_endpoints()
    
    # Test React frontend
    frontend_success = test_react_frontend()
    
    # Verify database state
    verify_database_state()
    
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"   Django API: {'✅ Working' if api_success else '❌ Issues'}")
    print(f"   React Frontend: {'✅ Working' if frontend_success else '❌ Issues'}")
    
    if api_success and frontend_success:
        print("\n🎉 Role-based authentication system is working properly!")
        print("\n📝 Next Steps:")
        print("   1. Open http://localhost:5173/auth/role-selection")
        print("   2. Test the complete authentication flow")
        print("   3. Verify role-specific dashboards")
    else:
        print("\n⚠️  Some components need attention. Check the logs above.")

if __name__ == "__main__":
    main()
