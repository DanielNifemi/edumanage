#!/usr/bin/env python3
"""
Simple API Test for Role-Based Authentication
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000/api"
    
    print("🔧 Testing EduManage API...")
    
    # Test 1: Get CSRF Token
    try:
        response = requests.get(f"{base_url}/auth/csrf/")
        if response.status_code == 200:
            print("✅ CSRF Token endpoint working")
            csrf_data = response.json()
            print(f"   CSRF Token received: {csrf_data.get('csrfToken', 'N/A')[:10]}...")
        else:
            print(f"❌ CSRF Token endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ CSRF Token test error: {e}")
    
    # Test 2: Test Student Registration
    student_data = {
        "username": "test_student_new@example.com",
        "email": "test_student_new@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "first_name": "New",
        "last_name": "Student",
        "user_type": "student",
        "student_id": "STU002"
    }
    
    print("\n📝 Testing Student Registration...")
    try:
        response = requests.post(
            f"{base_url}/auth/register/",
            json=student_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print("✅ Student registration successful")
            data = response.json()
            print(f"   User created: {data.get('user', {}).get('email', 'N/A')}")
            print(f"   Role: {data.get('user', {}).get('role', 'N/A')}")
        else:
            print(f"❌ Student registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Student registration error: {e}")
    
    # Test 3: Test Student Login
    login_data = {
        "email": "test_student_new@example.com",
        "password": "TestPass123!"
    }
    
    print("\n🔐 Testing Student Login...")
    try:
        response = requests.post(
            f"{base_url}/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Student login successful")
            data = response.json()
            print(f"   Welcome: {data.get('user', {}).get('first_name', 'N/A')}")
            print(f"   Role: {data.get('user', {}).get('role', 'N/A')}")
        else:
            print(f"❌ Student login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Student login error: {e}")

if __name__ == "__main__":
    test_api()
