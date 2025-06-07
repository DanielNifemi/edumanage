#!/usr/bin/env python
"""
Test registration to debug 400 error
"""
import requests
import time
import json

def test_registration():
    print("🧪 Testing Registration - Debug 400 Error")
    print("=" * 50)
    
    # Create test data
    timestamp = int(time.time())
    test_data = {
        'username': f'testuser_{timestamp}',
        'email': f'test_{timestamp}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User',
        'user_type': 'student'
    }
    
    print(f"Testing with data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
        elif response.status_code == 400:
            print("❌ Validation error (400):")
            try:
                error_data = response.json()
                for field, errors in error_data.items():
                    print(f"  {field}: {errors}")
            except:
                print(f"  Raw error: {response.text}")
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_registration()
