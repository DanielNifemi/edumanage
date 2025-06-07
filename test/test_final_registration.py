#!/usr/bin/env python
"""
Final test of registration API after fixes
"""
import requests
import time
import json

def test_registration_api():
    print("🎯 Final Registration API Test")
    print("=" * 40)
    
    # Create test data with unique timestamp
    timestamp = int(time.time())
    test_data = {
        'username': f'apitest_{timestamp}',
        'email': f'apitest_{timestamp}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'API',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    print(f"Testing registration for: {test_data['username']}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Registration working!")
            try:
                result = response.json()
                user_data = result.get('user', {})
                print(f"   Created user: {user_data.get('username', 'Unknown')}")
                print(f"   User ID: {user_data.get('id', 'Unknown')}")
                print(f"   Email: {user_data.get('email', 'Unknown')}")
                print("   ✅ Frontend registration should now work!")
            except json.JSONDecodeError:
                print("   Success but couldn't parse JSON response")
                
        elif response.status_code == 400:
            print("❌ Validation Error (400):")
            try:
                errors = response.json()
                for field, error_list in errors.items():
                    print(f"   {field}: {error_list}")
            except:
                print(f"   Raw error: {response.text}")
                
        elif response.status_code == 500:
            print("❌ Server Error (500):")
            print(f"   Raw response: {response.text}")
            
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Django server not running")
    except Exception as e:
        print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    test_registration_api()
