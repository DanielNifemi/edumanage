#!/usr/bin/env python
"""
Debug the 500 Internal Server Error for registration
"""
import requests
import json

print("🔍 Debugging Registration 500 Error")
print("=" * 50)

# Test data
test_data = {
    'username': 'debug500user',
    'email': 'debug500@example.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Debug',
    'last_name': 'User',
    'user_type': 'student'
}

# Test direct Django API
print("\n1️⃣ Testing Direct Django API (port 8000)...")
try:
    response = requests.post(
        'http://localhost:8000/api/auth/register/',
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    if response.status_code == 201:
        print("   ✅ Direct API works!")
    else:
        print(f"   ❌ Direct API failed")
        print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test through Vite proxy
print("\n2️⃣ Testing Through Vite Proxy (port 8080)...")
try:
    response = requests.post(
        'http://localhost:8080/api/auth/register/',
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    if response.status_code == 201:
        print("   ✅ Proxy works!")
    else:
        print(f"   ❌ Proxy failed")
        print(f"   Response: {response.text[:500]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test CORS preflight
print("\n3️⃣ Testing CORS Preflight...")
try:
    response = requests.options(
        'http://localhost:8080/api/auth/register/',
        headers={
            'Origin': 'http://localhost:8080',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'
        },
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   CORS Headers: {[h for h in response.headers.keys() if 'access-control' in h.lower()]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print(f"\n{'='*50}")
print("🔍 Debug Complete!")
