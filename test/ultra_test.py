#!/usr/bin/env python
"""
Ultra simple registration test
"""
import json
import urllib.request
import urllib.error

def test():
    data = {
        'username': 'ultratest123',
        'email': 'ultratest123@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Ultra',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    req = urllib.request.Request(
        'http://localhost:8000/api/auth/register/',
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"SUCCESS: {response.status}")
            print(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"ERROR: {e.code}")
        print(e.read().decode('utf-8'))

test()
