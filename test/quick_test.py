#!/usr/bin/env python
"""
Quick test to check if Django server is responding
"""
import urllib.request
import json
import time

def quick_test():
    print("Quick Django Server Test")
    
    # Test profile endpoint
    try:
        with urllib.request.urlopen('http://localhost:8000/api/auth/profile/') as response:
            data = response.read().decode('utf-8')
            print(f"Profile endpoint: {response.status} - {data}")
    except Exception as e:
        print(f"Profile endpoint error: {e}")
    
    # Test registration endpoint  
    timestamp = int(time.time())
    test_data = {
        'username': f'quicktest_{timestamp}',
        'email': f'quicktest_{timestamp}@example.com', 
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Quick',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    try:
        req = urllib.request.Request(
            'http://localhost:8000/api/auth/register/',
            data=json.dumps(test_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            print(f"Registration: {response.status} - {data[:200]}...")
            
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        print(f"Registration error: {e.code} - {error_data[:200]}...")
    except Exception as e:
        print(f"Registration error: {e}")

if __name__ == "__main__":
    quick_test()
