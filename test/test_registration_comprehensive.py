#!/usr/bin/env python3
"""
Comprehensive Registration Test for EduManage
Tests the complete registration flow after all fixes
"""

import os
import sys
import django
import requests
import json
from time import sleep
import threading

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile

def print_status(message, status="INFO"):
    icons = {"SUCCESS": "✅", "ERROR": "❌", "INFO": "ℹ️", "WARNING": "⚠️"}
    print(f"{icons.get(status, 'ℹ️')} {message}")

def check_django_server():
    """Check if Django server is running"""
    try:
        response = requests.get('http://localhost:8000/api/auth/profile/', timeout=5)
        return response.status_code in [200, 401, 403]
    except:
        return False

def start_django_server():
    """Start Django server in background"""
    import subprocess
    import time
    
    print_status("Starting Django server...")
    
    # Kill any existing Django processes
    try:
        os.system('taskkill /f /im python.exe 2>nul')
        time.sleep(2)
    except:
        pass
    
    # Start new server
    try:
        process = subprocess.Popen([
            'python', 'manage.py', 'runserver', '8000'
        ], cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        for i in range(30):
            if check_django_server():
                print_status("Django server is running", "SUCCESS")
                return True
            time.sleep(1)
            
        print_status("Django server failed to start properly", "ERROR")
        return False
    except Exception as e:
        print_status(f"Error starting Django server: {e}", "ERROR")
        return False

def test_registration_api():
    """Test registration API endpoint"""
    print_status("Testing registration API...")
    
    test_data = {
        "username": "test_comprehensive_user",
        "email": "test_comprehensive@example.com",
        "password": "securepass123",
        "first_name": "Test",
        "last_name": "User",
        "user_type": "student",
        "phone_number": "1234567890",
        "address": "123 Test Street"
    }
    
    try:
        # Clean up any existing test user
        try:
            User.objects.filter(username=test_data["username"]).delete()
            print_status("Cleaned up existing test user")
        except:
            pass
            
        # Test registration
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print_status(f"Registration response status: {response.status_code}")
        print_status(f"Registration response: {response.text[:500]}")
        
        if response.status_code == 201:
            print_status("Registration successful!", "SUCCESS")
            
            # Verify user was created
            user = User.objects.get(username=test_data["username"])
            profile = UserProfile.objects.get(user=user)
            print_status(f"User created: {user.username}, Type: {profile.user_type}", "SUCCESS")
            
            # Clean up
            user.delete()
            print_status("Test user cleaned up")
            return True
        else:
            print_status(f"Registration failed with status {response.status_code}", "ERROR")
            return False
            
    except requests.exceptions.Timeout:
        print_status("Registration request timed out", "ERROR")
        return False
    except Exception as e:
        print_status(f"Registration test error: {e}", "ERROR")
        return False

def test_auth_context_data():
    """Test auth profile endpoint"""
    print_status("Testing auth profile endpoint...")
    
    try:
        response = requests.get('http://localhost:8000/api/auth/profile/', timeout=10)
        print_status(f"Profile endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_status(f"Profile response: {json.dumps(data, indent=2)}")
            
            # Check if it handles unauthenticated users properly
            if data.get('authenticated') is False and data.get('user') is None:
                print_status("Auth context handles unauthenticated users correctly", "SUCCESS")
                return True
            else:
                print_status("Unexpected auth response format", "WARNING")
                return False
        else:
            print_status(f"Profile endpoint returned {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Auth context test error: {e}", "ERROR")
        return False

def test_all_user_types():
    """Test registration for all user types"""
    print_status("Testing registration for all user types...")
    
    user_types = ['student', 'teacher', 'staff', 'admin']
    results = {}
    
    for user_type in user_types:
        test_data = {
            "username": f"test_{user_type}_comp",
            "email": f"test_{user_type}_comp@example.com",
            "password": "securepass123",
            "first_name": "Test",
            "last_name": user_type.title(),
            "user_type": user_type,
            "phone_number": "1234567890",
            "address": "123 Test Street"
        }
        
        try:
            # Clean up existing
            User.objects.filter(username=test_data["username"]).delete()
            
            response = requests.post(
                'http://localhost:8000/api/auth/register/',
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            if response.status_code == 201:
                print_status(f"{user_type.title()} registration successful", "SUCCESS")
                results[user_type] = True
                
                # Clean up
                User.objects.filter(username=test_data["username"]).delete()
            else:
                print_status(f"{user_type.title()} registration failed: {response.status_code}", "ERROR")
                print_status(f"Response: {response.text[:200]}")
                results[user_type] = False
                
        except Exception as e:
            print_status(f"{user_type.title()} registration error: {e}", "ERROR")
            results[user_type] = False
    
    return results

def main():
    print_status("=" * 60)
    print_status("EduManage Comprehensive Registration Test")
    print_status("=" * 60)
    
    # Check if server is running
    if not check_django_server():
        print_status("Django server not running, attempting to start...")
        if not start_django_server():
            print_status("Failed to start Django server, exiting", "ERROR")
            return False
    else:
        print_status("Django server is already running", "SUCCESS")
    
    # Test 1: Auth context endpoint
    auth_test = test_auth_context_data()
    
    # Test 2: Basic registration
    basic_test = test_registration_api()
    
    # Test 3: All user types
    user_type_tests = test_all_user_types()
    
    # Summary
    print_status("=" * 60)
    print_status("TEST RESULTS SUMMARY")
    print_status("=" * 60)
    
    print_status(f"Auth Context Test: {'PASS' if auth_test else 'FAIL'}", 
                "SUCCESS" if auth_test else "ERROR")
    print_status(f"Basic Registration Test: {'PASS' if basic_test else 'FAIL'}", 
                "SUCCESS" if basic_test else "ERROR")
    
    for user_type, result in user_type_tests.items():
        print_status(f"{user_type.title()} Registration: {'PASS' if result else 'FAIL'}", 
                    "SUCCESS" if result else "ERROR")
    
    all_passed = auth_test and basic_test and all(user_type_tests.values())
    
    if all_passed:
        print_status("🎉 ALL TESTS PASSED! Registration system is working correctly.", "SUCCESS")
    else:
        print_status("❌ Some tests failed. Check the output above for details.", "ERROR")
    
    return all_passed

if __name__ == "__main__":
    main()
