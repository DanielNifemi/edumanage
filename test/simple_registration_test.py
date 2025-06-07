import requests
import json
import time

def test_registration_endpoint():
    print("🔍 Testing Registration Endpoint")
    print("=" * 40)
    
    # Create unique test data
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
    
    try:
        print(f"Testing with data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Registration working!")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Django server not responding")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration_endpoint()
