#!/usr/bin/env python
"""
Test registration API endpoint with our fixes
"""
import requests
import json

API_URL = 'http://localhost:8000/api/auth/register/'

test_cases = [
    {
        'name': 'Student Registration',
        'data': {
            'username': 'apistudent1',
            'email': 'apistudent1@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'API',
            'last_name': 'Student',
            'user_type': 'student'
        }
    },
    {
        'name': 'Teacher Registration',
        'data': {
            'username': 'apiteacher1',
            'email': 'apiteacher1@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'API',
            'last_name': 'Teacher',
            'user_type': 'teacher',
            'employee_id': 'APITCH001',
            'department': 'Computer Science'
        }
    },
    {
        'name': 'Staff Registration',
        'data': {
            'username': 'apistaff1',
            'email': 'apistaff1@example.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'first_name': 'API',
            'last_name': 'Staff',
            'user_type': 'staff',
            'employee_id': 'APISTF001'
        }
    }
]

print("🚀 Testing Registration API Endpoint")
print("=" * 50)

for test_case in test_cases:
    print(f"\n📝 Testing: {test_case['name']}")
    
    try:
        response = requests.post(
            API_URL,
            json=test_case['data'],
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("   ✅ Registration SUCCESSFUL!")
            try:
                data = response.json()
                print(f"   📄 Response: {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"   📄 Response: {response.text[:100]}...")
        
        elif response.status_code == 400:
            print("   ⚠️  Validation Error")
            try:
                errors = response.json()
                print(f"   📄 Errors: {json.dumps(errors, indent=2)}")
            except:
                print(f"   📄 Response: {response.text}")
        
        else:
            print("   ❌ Registration FAILED")
            print(f"   📄 Response: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error - Django server not running?")
    except requests.exceptions.Timeout:
        print("   ❌ Request Timeout")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print(f"\n{'='*50}")
print("🏁 API Testing Complete!")
