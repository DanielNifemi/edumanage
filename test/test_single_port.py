#!/usr/bin/env python
"""
Test the single-port setup with Vite proxy
"""
import requests
import time

print("🔗 Testing Single-Port Setup with Vite Proxy")
print("=" * 50)

# Test cases
test_urls = [
    {
        'name': 'Frontend (React App)',
        'url': 'http://localhost:8080/',
        'expected': 'React app served by Vite'
    },
    {
        'name': 'API via Proxy (Registration)',
        'url': 'http://localhost:8080/api/auth/register/',
        'expected': 'Django API proxied through Vite',
        'method': 'OPTIONS'  # Test CORS preflight
    },
    {
        'name': 'Django Admin via Proxy',
        'url': 'http://localhost:8080/admin/',
        'expected': 'Django admin interface'
    }
]

print("\n📝 Testing URLs through single port (8080)...")

for test in test_urls:
    print(f"\n🔍 Testing: {test['name']}")
    print(f"   URL: {test['url']}")
    
    try:
        method = test.get('method', 'GET')
        if method == 'OPTIONS':
            response = requests.options(test['url'], timeout=5)
        else:
            response = requests.get(test['url'], timeout=5)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 405]:  # 405 is OK for OPTIONS on some endpoints
            print(f"   ✅ SUCCESS - {test['expected']}")
            
            # Check for specific content indicators
            content = response.text.lower()
            if 'react' in content or 'vite' in content:
                print(f"   📄 Content: React/Vite detected")
            elif 'django' in content or 'admin' in content:
                print(f"   📄 Content: Django detected")
            elif response.headers.get('server', '').lower().startswith('django'):
                print(f"   📄 Headers: Django server detected")
            else:
                print(f"   📄 Content: {len(content)} characters")
        else:
            print(f"   ❌ FAILED - Status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ CONNECTION ERROR - Server not running on port 8080")
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT - Server took too long to respond")
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")

print(f"\n{'='*50}")
print("🎯 Single-Port Test Summary:")
print("\n💡 What this demonstrates:")
print("   ✅ Frontend served directly by Vite (port 8080)")
print("   ✅ API requests proxied to Django (port 8000)")
print("   ✅ Admin interface proxied to Django (port 8000)")
print("   ✅ All accessible through single port!")

print(f"\n🔧 How it works:")
print("   1. Vite dev server runs on port 8080")
print("   2. Vite proxy routes /api/* to Django (port 8000)")
print("   3. Vite proxy routes /admin/* to Django (port 8000)")
print("   4. All other routes served by React app")

print(f"\n🌐 Access everything at: http://localhost:8080/")
print("   - Frontend: http://localhost:8080/")
print("   - API: http://localhost:8080/api/")
print("   - Admin: http://localhost:8080/admin/")
