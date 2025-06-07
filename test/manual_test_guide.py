#!/usr/bin/env python3
"""
Manual Test Guide for Role-Based Authentication System
This script provides step-by-step instructions for testing the system
"""

def print_header(title):
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step_num, description):
    print(f"\n📋 Step {step_num}: {description}")

def print_checklist(items):
    print("\n✅ Verification Checklist:")
    for item in items:
        print(f"   □ {item}")

def manual_test_guide():
    print("🚀 EduManage Role-Based Authentication - Manual Test Guide")
    print("This guide will help you verify the complete authentication system")
    
    print_header("PREREQUISITES")
    print("Before starting, ensure you have:")
    print("   1. Django backend running on http://localhost:8000")
    print("   2. React frontend running on http://localhost:5173")
    print("   3. Both servers started without errors")
    
    print_header("TEST 1: ROLE SELECTION PAGE")
    print_step(1, "Open the role selection page")
    print("   URL: http://localhost:5173/auth/role-selection")
    
    print_checklist([
        "Page loads without errors",
        "4 role cards are displayed (Student, Teacher, Staff, Admin)",
        "Each card has appropriate icon and description",
        "Cards have hover effects with role-specific colors",
        "Student card hovers to blue",
        "Teacher card hovers to green", 
        "Staff card hovers to yellow",
        "Admin card hovers to red"
    ])
    
    print_header("TEST 2: STUDENT REGISTRATION")
    print_step(1, "Click on 'Student' role card")
    print_step(2, "Click 'Sign Up' button")
    print("   Expected URL: http://localhost:5173/auth/signup/student")
    
    print_step(3, "Fill out the student registration form:")
    print("   Email: student@test.com")
    print("   Password: TestPass123!")
    print("   First Name: Test")
    print("   Last Name: Student")
    print("   Student ID: STU001 (optional)")
    
    print_step(4, "Submit the form")
    
    print_checklist([
        "Form displays blue theme (student color)",
        "Student ID field is visible",
        "Form validates required fields",
        "Registration succeeds",
        "User is redirected to dashboard",
        "Dashboard shows 'Student' role"
    ])
    
    print_header("TEST 3: TEACHER REGISTRATION")
    print_step(1, "Go back to role selection page")
    print_step(2, "Click on 'Teacher' role card")
    print_step(3, "Click 'Sign Up' button")
    
    print_step(4, "Fill out the teacher registration form:")
    print("   Email: teacher@test.com")
    print("   Password: TestPass123!")
    print("   First Name: Test")
    print("   Last Name: Teacher")
    print("   Employee ID: TCH001")
    print("   Department: Mathematics")
    
    print_step(5, "Submit the form")
    
    print_checklist([
        "Form displays green theme (teacher color)",
        "Employee ID and Department fields are visible",
        "Registration succeeds",
        "User is redirected to dashboard",
        "Dashboard shows 'Teacher' role"
    ])
    
    print_header("TEST 4: STAFF REGISTRATION")
    print_step(1, "Test staff registration with staff-specific fields")
    print("   Email: staff@test.com")
    print("   Employee ID: STF001")
    print("   Department: Administration")
    
    print_checklist([
        "Form displays yellow theme (staff color)",
        "Staff-specific fields are shown",
        "Registration works correctly"
    ])
    
    print_header("TEST 5: ADMIN REGISTRATION")
    print_step(1, "Test admin registration with admin code")
    print("   Email: admin@test.com")
    print("   Admin Code: ADMIN123")
    
    print_checklist([
        "Form displays red theme (admin color)",
        "Admin code field is visible",
        "Registration requires admin code",
        "Admin gets elevated permissions"
    ])
    
    print_header("TEST 6: LOGIN FUNCTIONALITY")
    print_step(1, "Test login for each role")
    print("   Use the same credentials from registration")
    
    print_checklist([
        "Login forms have role-specific themes",
        "Login succeeds for each role",
        "Users are redirected to role-appropriate dashboards",
        "Role is correctly displayed in dashboard"
    ])
    
    print_header("TEST 7: API INTEGRATION")
    print_step(1, "Open browser developer tools (F12)")
    print_step(2, "Go to Network tab")
    print_step(3, "Perform a registration or login")
    print_step(4, "Check API calls")
    
    print_checklist([
        "API calls go to http://localhost:8000/api/auth/",
        "Requests include proper headers",
        "Responses include user data with role",
        "No CORS errors in console",
        "Authentication state updates correctly"
    ])
    
    print_header("TEST 8: ERROR HANDLING")
    print_step(1, "Test form validation")
    print("   Try submitting forms with:")
    print("   - Empty required fields")
    print("   - Invalid email format")
    print("   - Weak password")
    print("   - Duplicate email")
    
    print_checklist([
        "Form shows validation errors",
        "Error messages are clear",
        "User cannot submit invalid forms",
        "Server errors are handled gracefully"
    ])
    
    print_header("TEST 9: RESPONSIVE DESIGN")
    print_step(1, "Test on different screen sizes")
    print("   Use browser dev tools to simulate mobile")
    
    print_checklist([
        "Role cards stack properly on mobile",
        "Forms are usable on small screens",
        "Buttons are touch-friendly",
        "Text is readable on all sizes"
    ])
    
    print_header("TROUBLESHOOTING")
    print("If you encounter issues:")
    print("\n🔧 Backend Issues:")
    print("   - Check Django server is running: python manage.py runserver 8000")
    print("   - Check for migration issues: python manage.py migrate")
    print("   - Check Django admin: http://localhost:8000/admin/")
    print("   - Check API endpoints: http://localhost:8000/api/swagger/")
    
    print("\n🖥️  Frontend Issues:")
    print("   - Check React server is running: npm run dev")
    print("   - Check console for JavaScript errors")
    print("   - Clear browser cache and cookies")
    print("   - Check network requests in dev tools")
    
    print("\n🌐 Connection Issues:")
    print("   - Verify CORS settings in Django settings.py")
    print("   - Check firewall/antivirus blocking ports")
    print("   - Try different browsers")
    print("   - Check localhost vs 127.0.0.1")
    
    print_header("SUCCESS CRITERIA")
    print("The system is working correctly if:")
    print("   ✅ All 4 roles can register successfully")
    print("   ✅ All 4 roles can login successfully") 
    print("   ✅ Role-specific themes display correctly")
    print("   ✅ Role-specific fields work properly")
    print("   ✅ Dashboards show correct role information")
    print("   ✅ No console errors or API failures")
    print("   ✅ Responsive design works on mobile")
    
    print("\n🎉 If all tests pass, your role-based authentication system is ready!")

if __name__ == "__main__":
    manual_test_guide()
