#!/usr/bin/env python
"""
Simple script to test Django URL resolution and API availability
"""
import os
import sys
import django
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.test import Client
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

def test_url_resolution():
    """Test if our API URLs are properly resolved"""
    print("🔍 Testing Django URL Resolution...")
    
    try:
        # Test basic admin URL
        admin_url = reverse('admin:index')
        print(f"✅ Admin URL resolved: {admin_url}")
    except NoReverseMatch as e:
        print(f"❌ Admin URL failed: {e}")
    
    try:
        # Test API URLs
        from django.urls import get_resolver
        resolver = get_resolver()
        print(f"✅ URL Resolver loaded successfully")
        
        # Check available URL patterns
        print("\n📋 Available URL patterns:")
        for pattern in resolver.url_patterns:
            print(f"  - {pattern}")
            
    except Exception as e:
        print(f"❌ URL resolution error: {e}")

def test_api_endpoints():
    """Test API endpoints using Django test client"""
    print("\n🧪 Testing API Endpoints with Django Client...")
    
    client = Client()
    
    # Test base API
    try:
        response = client.get('/api/')
        print(f"✅ /api/ - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ /api/ error: {e}")
    
    # Test auth API
    try:
        response = client.get('/api/auth/')
        print(f"✅ /api/auth/ - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ /api/auth/ error: {e}")
    
    # Test register endpoint
    try:
        response = client.get('/api/auth/register/')
        print(f"✅ /api/auth/register/ - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ /api/auth/register/ error: {e}")

def test_live_api():
    """Test live API endpoints"""
    print("\n🌐 Testing Live API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/admin/",
        "/api/",
        "/api/auth/",
        "/api/auth/register/",
        "/api/swagger/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} error: {e}")

if __name__ == "__main__":
    print("🚀 Django API Diagnostic Tool")
    print("=" * 50)
    
    test_url_resolution()
    test_api_endpoints()
    test_live_api()
    
    print("\n" + "=" * 50)
    print("✅ Diagnostic complete!")
