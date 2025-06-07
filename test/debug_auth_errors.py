#!/usr/bin/env python
"""
Debug the auth context and registration errors
"""
import requests

print("🔍 Debugging Auth Context and Registration Errors")
print("=" * 60)

# Test 1: Current user endpoint (what AuthContext is calling)
print("\n1. Testing current user endpoint...")
try:
    response = requests.get('http://localhost:8000/api/auth/user/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Check what endpoints are available
print("\n2. Testing available auth endpoints...")
endpoints_to_test = [
    '/api/auth/csrf/',
    '/api/auth/register/',
    '/api/auth/login/',
    '/api/auth/logout/',
]

for endpoint in endpoints_to_test:
    try:
        response = requests.get(f'http://localhost:8000{endpoint}')
        print(f"   GET {endpoint}: {response.status_code}")
    except Exception as e:
        print(f"   GET {endpoint}: Error - {e}")

# Test 3: Try a registration to see the 400 error details
print("\n3. Testing registration to debug 400 error...")
import time
test_data = {
    'username': f'debuguser_{int(time.time())}',
    'email': f'debug_{int(time.time())}@test.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Debug',
    'last_name': 'User',
    'user_type': 'student'
}

try:
    response = requests.post(
        'http://localhost:8000/api/auth/register/',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Registration Status: {response.status_code}")
    print(f"   Registration Response: {response.text}")
except Exception as e:
    print(f"   Registration Error: {e}")

print("\n" + "=" * 60)
