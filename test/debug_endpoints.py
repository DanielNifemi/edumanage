#!/usr/bin/env python
"""
Debug Django responses for proxied requests
"""
import requests
import json

def test_endpoints():
    print("🔍 Debugging Django Endpoints")
    print("=" * 50)
    
    # Test 1: Health check - direct
    print("\n1. Health check - Direct API")
    try:
        response = requests.get('http://localhost:8000/api/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Health check - proxy
    print("\n2. Health check - Proxy")
    try:
        response = requests.get('http://localhost:8080/api/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get CSRF token - direct
    print("\n3. CSRF token - Direct API")
    try:
        response = requests.get('http://localhost:8000/api/auth/csrf-token/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get CSRF token - proxy
    print("\n4. CSRF token - Proxy")
    try:
        response = requests.get('http://localhost:8080/api/auth/csrf-token/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Register endpoint - GET direct
    print("\n5. Register endpoint GET - Direct")
    try:
        response = requests.get('http://localhost:8000/api/auth/register/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Register endpoint - GET proxy
    print("\n6. Register endpoint GET - Proxy")
    try:
        response = requests.get('http://localhost:8080/api/auth/register/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_endpoints()
