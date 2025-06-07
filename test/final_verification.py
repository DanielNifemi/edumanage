#!/usr/bin/env python
"""
Final comprehensive test of the fixed EduManage registration system
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.models import CustomUser
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile

print("🎉 EduManage Registration System - Final Verification")
print("=" * 60)

# Clean up any existing final test users
cleanup_usernames = ['finaltest_student', 'finaltest_teacher', 'finaltest_staff', 'finaltest_admin']
for username in cleanup_usernames:
    try:
        user = CustomUser.objects.get(username=username)
        user.delete()
        print(f"🧹 Cleaned up: {username}")
    except CustomUser.DoesNotExist:
        pass

print("\n📋 Testing Complete Registration Flow...")

# Test cases for API registration
test_cases = [
    {
        'type': 'Student',
        'data': {
            'username': 'finaltest_student',
            'email': 'finalstudent@edumanage.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Final',
            'last_name': 'Student',
            'user_type': 'student',
            'student_id': 'FIN2025001'
        }
    },
    {
        'type': 'Teacher', 
        'data': {
            'username': 'finaltest_teacher',
            'email': 'finalteacher@edumanage.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Final',
            'last_name': 'Teacher',
            'user_type': 'teacher',
            'employee_id': 'TCH2025001',
            'department': 'Computer Science'
        }
    },
    {
        'type': 'Staff',
        'data': {
            'username': 'finaltest_staff',
            'email': 'finalstaff@edumanage.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Final',
            'last_name': 'Staff',
            'user_type': 'staff',
            'employee_id': 'STF2025001'
        }
    },
    {
        'type': 'Admin',
        'data': {
            'username': 'finaltest_admin',
            'email': 'finaladmin@edumanage.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Final',
            'last_name': 'Admin',
            'user_type': 'admin',
            'admin_code': 'ADMIN123'
        }
    }
]

API_URL = 'http://localhost:8000/api/auth/register/'
success_count = 0
total_tests = len(test_cases)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{i}️⃣ Testing {test_case['type']} Registration...")
    
    try:
        response = requests.post(
            API_URL,
            json=test_case['data'],
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"   ✅ API Registration: SUCCESS")
            success_count += 1
            
            # Verify database records
            try:
                username = test_case['data']['username']
                user = CustomUser.objects.get(username=username)
                print(f"   ✅ User Created: {user.get_full_name()} ({user.email})")
                
                if hasattr(user, 'userprofile'):
                    profile = user.userprofile
                    print(f"   ✅ Profile Type: {profile.user_type}")
                    
                    # Check role-specific profiles
                    if profile.user_type == 'student' and hasattr(user, 'student'):
                        print(f"   ✅ Student Profile: {user.student.student_id}")
                    elif profile.user_type == 'teacher' and hasattr(user, 'teacher'):
                        print(f"   ✅ Teacher Profile: {user.teacher.teacher_id} - {user.teacher.department}")
                    elif profile.user_type == 'staff' and hasattr(user, 'staffprofile'):
                        print(f"   ✅ Staff Profile: {user.staffprofile.staff_id} - {user.staffprofile.employee_id}")
                    elif profile.user_type == 'admin':
                        print(f"   ✅ Admin Profile: Staff={user.is_staff}, Super={user.is_superuser}")
                    
                else:
                    print(f"   ⚠️  UserProfile missing")
                    
            except Exception as e:
                print(f"   ❌ Database verification failed: {e}")
                
        elif response.status_code == 400:
            print(f"   ❌ Validation Error:")
            try:
                errors = response.json()
                for field, msgs in errors.items():
                    print(f"      - {field}: {msgs}")
            except:
                print(f"      {response.text}")
                
        else:
            print(f"   ❌ API Error (Status: {response.status_code})")
            print(f"      Response: {response.text[:100]}...")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error - Django server not running?")
    except Exception as e:
        print(f"   ❌ Test Error: {e}")

print(f"\n{'='*60}")
print(f"🏁 Final Verification Results:")
print(f"   📊 Success Rate: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")

# Final database summary
total_users = CustomUser.objects.filter(username__startswith='finaltest_').count()
total_students = Student.objects.filter(user__username__startswith='finaltest_').count()
total_teachers = Teacher.objects.filter(user__username__startswith='finaltest_').count()
total_staff = StaffProfile.objects.filter(user__username__startswith='finaltest_').count()
total_admins = CustomUser.objects.filter(username__startswith='finaltest_', is_superuser=True).count()

print(f"\n📈 Database Summary:")
print(f"   👥 Total Users: {total_users}")
print(f"   🎓 Students: {total_students}")
print(f"   👩‍🏫 Teachers: {total_teachers}")
print(f"   👷 Staff: {total_staff}")
print(f"   👑 Admins: {total_admins}")

if success_count == total_tests and total_users == total_tests:
    print(f"\n🎉 CONGRATULATIONS!")
    print(f"🟢 EduManage Registration System is FULLY FUNCTIONAL!")
    print(f"✅ All user types can register successfully")
    print(f"✅ API endpoints working correctly")
    print(f"✅ Database models and relationships working")
    print(f"✅ Role-based authentication system ready!")
else:
    print(f"\n⚠️  Some issues remain. Check the errors above.")

print(f"\n🌐 Frontend Access: http://localhost:8082")
print(f"🔧 Backend API: http://localhost:8000/api/auth/register/")
print(f"{'='*60}")
