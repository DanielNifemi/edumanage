#!/usr/bin/env python3
"""
Backend Verification Script
Tests all critical backend functionality before frontend development
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        status_ok = response.status_code == expected_status if expected_status else response.status_code < 400
        
        return {
            "success": status_ok,
            "status_code": response.status_code,
            "data": response.json() if response.content else None,
            "url": url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

def main():
    print("🔍 BACKEND VERIFICATION STARTING...")
    print("=" * 50)
    
    results = []
    
    # Test 1: User Registration
    print("\n1️⃣  Testing User Registration...")
    reg_data = {
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "user_type": "student"
    }
    
    reg_result = test_endpoint("POST", "/auth/register/", reg_data, expected_status=201)
    results.append(("Registration", reg_result))
    
    if reg_result["success"]:
        print("✅ Registration successful")
        user_email = reg_data["email"]
    else:
        print(f"❌ Registration failed: {reg_result}")
        user_email = "newuser@example.com"  # Fallback to existing user
    
    # Test 2: User Login
    print("\n2️⃣  Testing User Login...")
    login_data = {
        "email": user_email,
        "password": "testpass123"
    }
    
    login_result = test_endpoint("POST", "/auth/login/", login_data, expected_status=200)
    results.append(("Login", login_result))
    
    if login_result["success"]:
        print("✅ Login successful")
        token = login_result["data"].get("token") if login_result["data"] else None
        auth_headers = {"Authorization": f"Bearer {token}"} if token else {}
    else:
        print(f"❌ Login failed: {login_result}")
        auth_headers = {}
    
    # Test 3: Protected Endpoints (should require auth)
    print("\n3️⃣  Testing Protected Endpoints...")
    
    protected_endpoints = [
        "/courses/",
        "/students/", 
        "/teachers/",
        "/staff/",
        "/schedules/",
        "/attendance/",
        "/examinations/",
        "/communication/messages/",
        "/discipline/"
    ]
    
    for endpoint in protected_endpoints:
        # Test without auth (should fail)
        unauth_result = test_endpoint("GET", endpoint, expected_status=401)
        
        # Test with auth (if we have token)
        if auth_headers:
            auth_result = test_endpoint("GET", endpoint, headers=auth_headers)
            endpoint_status = "✅ Protected" if unauth_result["success"] and auth_result["status_code"] in [200, 403] else "❌ Security Issue"
        else:
            endpoint_status = "✅ Protected" if unauth_result["success"] else "❌ Security Issue"
        
        print(f"  {endpoint}: {endpoint_status}")
        results.append((f"Security: {endpoint}", {"success": "✅" in endpoint_status}))
    
    # Test 4: API Structure
    print("\n4️⃣  Testing API Structure...")
    
    # Test main API endpoint
    api_result = test_endpoint("GET", "/", expected_status=200)
    results.append(("API Root", api_result))
    
    if api_result["success"]:
        print("✅ API root accessible")
    else:
        print("❌ API root not accessible")
    
    # Test 5: Database Connectivity
    print("\n5️⃣  Testing Database Connectivity...")
    
    # Test by trying to access auth endpoints (requires DB)
    db_test = test_endpoint("POST", "/auth/login/", {"email": "test", "password": "test"})
    db_status = "✅ Database Connected" if db_test["status_code"] in [400, 401] else "❌ Database Issue"
    print(f"  {db_status}")
    results.append(("Database", {"success": "✅" in db_status}))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result.get("success", False))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED - BACKEND READY FOR FRONTEND!")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️  MOSTLY WORKING - Minor issues detected")
    else:
        print("\n❌ CRITICAL ISSUES - Backend needs attention")
    
    print("\n📋 Detailed Results:")
    for test_name, result in results:
        status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not result.get("success", False) and "error" in result:
            print(f"    Error: {result['error']}")
    
    print(f"\n🕐 Verification completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Verification failed with error: {e}")
        sys.exit(1)
