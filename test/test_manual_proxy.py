#!/usr/bin/env python
"""
Simple proxy test to isolate the issue
"""
import requests
import subprocess
import time
import json

def test_manual_proxy():
    """Test with manual proxy setup"""
    print("🔧 Manual Proxy Test")
    print("=" * 30)
    
    # Test direct connection first
    print("1. Testing direct Django connection...")
    try:
        response = requests.get('http://localhost:8000/api/auth/csrf/')
        print(f"   Direct Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Direct Response: {data.get('csrfToken', 'No token')[:20]}...")
        else:
            print(f"   Direct Error: {response.text[:100]}")
    except Exception as e:
        print(f"   Direct Error: {e}")
    
    # Test registration with proper headers
    print("\n2. Testing direct registration...")
    test_data = {
        'username': f'testuser_{int(time.time())}',
        'email': f'test_{int(time.time())}@example.com',
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
                'Accept': 'application/json',
                'User-Agent': 'TestClient/1.0'
            }
        )
        print(f"   Direct Registration Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Direct registration works!")
        else:
            print(f"   Direct Registration Error: {response.text[:200]}")
    except Exception as e:
        print(f"   Direct Registration Error: {e}")
    
    # Test through different approaches
    print("\n3. Testing with different headers...")
    try:
        # Test with headers that mimic Vite proxy
        response = requests.post(
            'http://localhost:8000/api/auth/register/',
            json={
                'username': f'proxytest_{int(time.time())}',
                'email': f'proxy_{int(time.time())}@example.com',
                'password': 'TestPass123!',
                'password_confirm': 'TestPass123!',
                'first_name': 'Proxy',
                'last_name': 'Test',
                'user_type': 'student'
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'http://localhost:8080',
                'Referer': 'http://localhost:8080/',
                'User-Agent': 'Mozilla/5.0 (Vite Proxy)'
            }
        )
        print(f"   Proxy-like headers Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Proxy-like headers work!")
        else:
            print(f"   Proxy-like headers Error: {response.text[:200]}")
    except Exception as e:
        print(f"   Proxy-like headers Error: {e}")

if __name__ == "__main__":
    test_manual_proxy()
