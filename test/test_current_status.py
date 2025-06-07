#!/usr/bin/env python
"""
Test current status of EduManage registration system
"""
import requests
import json
import time

def test_registration_status():
    print("🎯 Testing EduManage Registration System")
    print("=" * 50)
    
    # Test 1: Check if server is responding
    print("\n1. Testing server responsiveness...")
    try:
        response = requests.get('http://localhost:8000/api/auth/profile/', timeout=5)
        print(f"   ✅ Server responsive: {response.status_code}")
        print(f"   Profile response: {response.text}")
    except Exception as e:
        print(f"   ❌ Server error: {e}")
        return
    
    # Test 2: Test registration endpoint
    print("\n2. Testing registration endpoint...")
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
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json=test_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("   ✅ SUCCESS! Registration working!")
            try:
                result = response.json()
                user_data = result.get('user', {})
                print(f"      Created user: {user_data.get('username', 'Unknown')}")
                print(f"      User ID: {user_data.get('id', 'Unknown')}")
                print(f"      Email: {user_data.get('email', 'Unknown')}")
            except:
                print("      Success but couldn't parse JSON")
                
        elif response.status_code == 400:
            print("   ❌ Validation Error (400):")
            try:
                errors = response.json()
                for field, error_list in errors.items():
                    print(f"      {field}: {error_list}")
            except:
                print(f"      Raw error: {response.text}")
                
        elif response.status_code == 500:
            print("   ❌ Server Error (500):")
            print(f"      Raw response: {response.text}")
            
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            print(f"      Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection error")
    except Exception as e:
        print(f"   ❌ Request error: {e}")
    
    # Test 3: Check frontend accessibility
    print("\n3. Testing frontend server...")
    try:
        response = requests.get('http://localhost:8080', timeout=5)
        print(f"   ✅ Frontend responsive: {response.status_code}")
    except:
        print("   ⚠️  Frontend not running on port 8080")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_registration_status()
