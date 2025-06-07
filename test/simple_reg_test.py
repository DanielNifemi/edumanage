#!/usr/bin/env python
"""
Simple direct test of the registration API to isolate the issue
"""
import requests
import json

print("🧪 Simple Registration API Test")
print("=" * 40)

# Test with minimal data
simple_data = {
    'username': 'simpletest123',
    'email': 'simpletest123@test.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Simple',
    'last_name': 'Test',
    'user_type': 'student'
}

print("Testing direct Django API...")
try:
    response = requests.post(
        'http://localhost:8000/api/auth/register/',
        json=simple_data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ SUCCESS!")
        data = response.json()
        print(f"User created: {data.get('username')}")
    else:
        print("❌ FAILED")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
    
print("\nTesting proxy (if available)...")
try:
    response = requests.post(
        'http://localhost:8080/api/auth/register/',
        json={
            'username': 'proxytest123',
            'email': 'proxytest123@test.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'Proxy',
            'last_name': 'Test',
            'user_type': 'student'
        },
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    
    print(f"Proxy Status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ PROXY SUCCESS!")
    else:
        print("❌ PROXY FAILED")
        print(f"Response: {response.text[:200]}")
        
except requests.exceptions.ConnectionError:
    print("❌ Proxy not available (Vite server not running?)")
except Exception as e:
    print(f"Proxy Error: {e}")
