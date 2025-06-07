#!/usr/bin/env python
"""
Test registration through the frontend to verify the fix
"""
import requests
import time
import json

def test_registration_fix():
    """Test the complete registration flow"""
    print("🧪 Testing Registration Fix")
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
    
    print(f"Testing with user: {test_data['username']}")
    
    # Test 1: Direct API call
    print("\n1. Testing Direct API (port 8000)...")
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ SUCCESS - Direct API working!")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('username', 'Unknown')}")
        else:
            print("   ❌ FAILED - Direct API")
            print(f"   Error: {response.text[:300]}")
            
    except requests.exceptions.Timeout:
        print("   ❌ TIMEOUT - Django server not responding")
    except requests.exceptions.ConnectionError:
        print("   ❌ CONNECTION ERROR - Django server not running")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test 2: Proxy call (simulate frontend)
    print("\n2. Testing Proxy (port 8080 - Frontend)...")
    proxy_data = {
        'username': f'proxyuser_{timestamp}',
        'email': f'proxy_{timestamp}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Proxy',
        'last_name': 'User',
        'user_type': 'student'
    }
    
    try:
        response = requests.post(
            'http://localhost:8080/api/auth/register/',
            json=proxy_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ SUCCESS - Proxy working!")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('username', 'Unknown')}")
        else:
            print("   ❌ FAILED - Proxy")
            print(f"   Error: {response.text[:300]}")
            
    except requests.exceptions.Timeout:
        print("   ❌ TIMEOUT - Vite server not responding")
    except requests.exceptions.ConnectionError:
        print("   ❌ CONNECTION ERROR - Vite server not running")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 40)
    print("Test completed!")

if __name__ == "__main__":
    test_registration_fix()
