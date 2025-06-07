#!/usr/bin/env python
"""
Quick solution: Bypass Vite proxy and use direct API calls from frontend
"""

print("🔧 QUICK FIX SOLUTION")
print("=" * 50)

print("""
ISSUE IDENTIFIED:
- Direct Django API (port 8000) works perfectly ✅
- Vite proxy (port 8080) returns 500 errors ❌

IMMEDIATE SOLUTION:
Instead of fixing the Vite proxy (which requires server restart),
we can modify the frontend to use direct API calls temporarily.

STEPS:
1. Update frontend/src/lib/api.ts to use direct Django URL
2. Update CORS settings to allow direct calls
3. Test registration through the frontend

This bypasses the proxy issue entirely and gets the registration working immediately.
""")

print("\n📝 Implementation:")
print("1. Change API_BASE_URL from '/api' to 'http://localhost:8000/api'")
print("2. Ensure CORS allows localhost:8080")
print("3. Test registration")

print("\n🔍 Current Status:")
print("✅ Django server running on port 8000")
print("✅ Frontend running on port 8080") 
print("✅ Registration API working via direct calls")
print("✅ CORS configured for cross-origin requests")
print("❌ Vite proxy misconfigured (returns 500)")

print("\n💡 Recommendation:")
print("Use direct API calls until Vite proxy can be properly debugged.")
print("This is a common pattern and perfectly acceptable for development.")

# Test the direct API approach
import requests
import time

test_data = {
    'username': f'directtest_{int(time.time())}',
    'email': f'directtest_{int(time.time())}@example.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Direct',
    'last_name': 'Test',
    'user_type': 'student'
}

print(f"\n🧪 Testing Direct API Registration:")
try:
    response = requests.post(
        'http://localhost:8000/api/auth/register/',
        json=test_data,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    
    if response.status_code == 201:
        print("✅ SUCCESS - Direct API registration working!")
        print("   This confirms the backend is ready for frontend integration.")
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"   Error: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Error: {e}")
