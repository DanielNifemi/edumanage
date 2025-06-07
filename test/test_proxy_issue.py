#!/usr/bin/env python
"""
Test proxy issue with unique usernames
"""
import requests
import json
import random
import time

def generate_unique_test_data():
    timestamp = int(time.time())
    rand = random.randint(1000, 9999)
    return {
        'username': f'testuser_{timestamp}_{rand}',
        'email': f'test_{timestamp}_{rand}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User',
        'user_type': 'student'
    }

print("🧪 Testing Registration - Direct vs Proxy")
print("=" * 50)

# Test 1: Direct API
print("\n1. Testing DIRECT API (localhost:8000)...")
direct_data = generate_unique_test_data()
try:
    response = requests.post(
        'http://localhost:8000/api/auth/register/',
        json=direct_data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print("   ✅ SUCCESS!")
    else:
        print("   ❌ FAILED")
        print(f"   Response: {response.text[:200]}")
        
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Proxy
print("\n2. Testing PROXY (localhost:8080)...")
proxy_data = generate_unique_test_data()
try:
    response = requests.post(
        'http://localhost:8080/api/auth/register/',
        json=proxy_data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print("   ✅ SUCCESS!")
    else:
        print("   ❌ FAILED")
        print(f"   Response: {response.text[:500]}")
        
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Check CSRF issues
print("\n3. Testing CSRF token handling...")
try:
    # First get CSRF token
    csrf_response = requests.get('http://localhost:8080/api/auth/register/')
    print(f"   CSRF fetch status: {csrf_response.status_code}")
    
    if 'csrftoken' in csrf_response.cookies:
        print("   CSRF token found in cookies")
        csrf_token = csrf_response.cookies['csrftoken']
        
        # Try with CSRF token
        csrf_data = generate_unique_test_data()
        response = requests.post(
            'http://localhost:8080/api/auth/register/',
            json=csrf_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': csrf_token
            },
            cookies={'csrftoken': csrf_token}
        )
        print(f"   Status with CSRF: {response.status_code}")
        if response.status_code != 201:
            print(f"   Response: {response.text[:300]}")
    else:
        print("   No CSRF token found")
        
except Exception as e:
    print(f"   CSRF Error: {e}")

print("\n" + "=" * 50)
print("Test completed!")
