#!/usr/bin/env python
"""
Simple registration test using built-in libraries
"""
import urllib.request
import urllib.parse
import json
import time

def test_registration():
    print("Testing Registration Endpoint")
    print("=" * 30)
    
    # Create test data
    timestamp = int(time.time())
    test_data = {
        'username': f'simpletest_{timestamp}',
        'email': f'simpletest_{timestamp}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Simple',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    print(f"Creating user: {test_data['username']}")
    
    try:
        # Create request
        req = urllib.request.Request(
            'http://localhost:8000/api/auth/register/',
            data=json.dumps(test_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json'
            }
        )
        
        # Send request
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"✅ SUCCESS! Status: {response.status}")
            print(f"Response: {result}")
            
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {error_data}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()
