#!/usr/bin/env python
"""
Test script to identify the registration issue
"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from django.test import Client
from accounts.api.serializers import RegisterSerializer

def test_register_serializer():
    """Test the RegisterSerializer directly"""
    print("🧪 Testing RegisterSerializer...")
    
    # Sample registration data
    data = {
        'username': 'testuser3',
        'email': 'test3@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'user_type': 'student',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    try:
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            print("✅ Serializer validation passed")
            user = serializer.save()
            print(f"✅ User created successfully: {user.username}")
            return True
        else:
            print(f"❌ Serializer validation failed: {serializer.errors}")
            return False
    except Exception as e:
        print(f"❌ Serializer error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_register_api():
    """Test the registration API endpoint directly"""
    print("\n🌐 Testing Registration API...")
    
    client = Client()
    data = {
        'username': 'testuser4',
        'email': 'test4@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'user_type': 'student',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    try:
        response = client.post(
            '/api/auth/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        print(f"API Response Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ API registration successful")
            print(f"Response: {response.content.decode()}")
            return True
        else:
            print(f"❌ API registration failed")
            print(f"Response: {response.content.decode()}")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Registration Debugging Tool")
    print("=" * 50)
    
    # Test serializer
    serializer_ok = test_register_serializer()
    
    # Test API
    api_ok = test_register_api()
    
    print("\n" + "=" * 50)
    print(f"Serializer Test: {'✅ PASS' if serializer_ok else '❌ FAIL'}")
    print(f"API Test: {'✅ PASS' if api_ok else '❌ FAIL'}")
