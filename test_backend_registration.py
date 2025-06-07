#!/usr/bin/env python
"""
Test if backend registration is working
"""
import requests
import time
import json

def test_backend_registration():
    print("🧪 Testing Backend Registration")
    print("=" * 40)
    
    timestamp = int(time.time())
    test_data = {
        'username': f'testuser_{timestamp}',
        'email': f'testuser_{timestamp}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User',
        'user_type': 'student'
    }
    
    try:
        print(f"Registering user: {test_data['username']}")
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Registration successful!")
            try:
                result = response.json()
                print(f"User created: {result.get('user', {}).get('username')}")
            except:
                print("Response not JSON, but registration successful")
        else:
            print(f"❌ Registration failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_backend_registration()
