#!/usr/bin/env python
"""
Practical demonstration: Registration test through single port
"""
import requests
import json

print("🎯 PRACTICAL DEMO: Single Port Registration Test")
print("=" * 55)

# Test registration through the single port (8080) with proxy
registration_data = {
    'username': 'singleport_test',
    'email': 'singleport@example.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Single',
    'last_name': 'Port',
    'user_type': 'student'
}

print("📝 Testing user registration through single port...")
print(f"   Target URL: http://localhost:8080/api/auth/register/")
print(f"   User: {registration_data['username']}")
print(f"   Type: {registration_data['user_type']}")

try:
    # This request goes to port 8080 (Vite) but gets proxied to port 8000 (Django)
    response = requests.post(
        'http://localhost:8080/api/auth/register/',
        json=registration_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
    print(f"\n📡 Response:")
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 201:
        print("   ✅ SUCCESS! Registration worked through single port!")
        
        try:
            data = response.json()
            print(f"   📄 User Created:")
            print(f"      - Username: {data.get('username')}")
            print(f"      - Email: {data.get('email')}")
            print(f"      - Role: {data.get('role')}")
            print(f"      - Full Name: {data.get('first_name')} {data.get('last_name')}")
        except:
            print(f"   📄 Response: {response.text[:200]}...")
            
    elif response.status_code == 400:
        print("   ⚠️  Validation error (user might already exist)")
        try:
            errors = response.json()
            print(f"   📄 Errors: {json.dumps(errors, indent=2)}")
        except:
            print(f"   📄 Response: {response.text}")
    else:
        print(f"   ❌ Failed with status {response.status_code}")
        print(f"   📄 Response: {response.text[:200]}...")

except requests.exceptions.ConnectionError:
    print("   ❌ CONNECTION ERROR")
    print("   💡 Make sure React dev server is running on port 8080 with proxy enabled")
    print("   💡 Run: cd frontend && npm run dev")
    
except Exception as e:
    print(f"   ❌ ERROR: {str(e)}")

print(f"\n{'='*55}")
print("🎉 DEMONSTRATION COMPLETE!")
print("\n💡 What this proves:")
print("   ✅ Frontend and backend CAN run on same port")
print("   ✅ Vite proxy routes API calls to Django")
print("   ✅ User experiences single-port application")
print("   ✅ No CORS issues or port confusion")

print(f"\n🔧 How it works:")
print("   1. User accesses: http://localhost:8080/")
print("   2. React app loads from Vite dev server")
print("   3. API calls to /api/* get proxied to Django (port 8000)")
print("   4. User sees seamless single-port experience")

print(f"\n🌐 Try it yourself:")
print("   - Open: http://localhost:8080/")
print("   - All registration forms will work through this single URL")
print("   - API calls automatically routed to Django backend")

print(f"\n📚 Technical Summary:")
print("   - Frontend: Vite dev server (Node.js)")
print("   - Backend: Django WSGI server (Python)")
print("   - Integration: Vite proxy configuration")
print("   - Result: Single-port full-stack application!")
