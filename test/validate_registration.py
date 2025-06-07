#!/usr/bin/env python
"""
Quick validation of registration serializer fixes
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.api.serializers import RegisterSerializer
from accounts.models import CustomUser
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile

print("🔧 Testing Registration Serializer Fixes")
print("=" * 50)

# Clean up any existing test users first
test_usernames = ['testvalidation1', 'testvalidation2', 'testvalidation3']
for username in test_usernames:
    try:
        user = CustomUser.objects.get(username=username)
        user.delete()
        print(f"🧹 Cleaned up existing user: {username}")
    except CustomUser.DoesNotExist:
        pass

# Test 1: Student registration
print("\n1️⃣ Testing Student Registration...")
student_data = {
    'username': 'testvalidation1',
    'email': 'testval1@example.com', 
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Test',
    'last_name': 'Student',
    'user_type': 'student'
}

try:
    serializer = RegisterSerializer(data=student_data)
    if serializer.is_valid():
        user = serializer.save()
        print(f"✅ Student user created: {user.username}")
        
        # Check if Student profile was created
        if hasattr(user, 'student'):
            student = user.student
            print(f"✅ Student profile created: {student.student_id}")
            print(f"   - Date of birth: {student.date_of_birth} (should be None/null)")
            print(f"   - Grade: {student.grade}")
        else:
            print("❌ Student profile NOT created")
    else:
        print(f"❌ Student validation failed: {serializer.errors}")
except Exception as e:
    print(f"❌ Student creation error: {str(e)}")

# Test 2: Teacher registration
print("\n2️⃣ Testing Teacher Registration...")
teacher_data = {
    'username': 'testvalidation2',
    'email': 'testval2@example.com',
    'password': 'TestPass123!', 
    'password_confirm': 'TestPass123!',
    'first_name': 'Test',
    'last_name': 'Teacher',
    'user_type': 'teacher',
    'employee_id': 'TCH001',
    'department': 'Mathematics'
}

try:
    serializer = RegisterSerializer(data=teacher_data)
    if serializer.is_valid():
        user = serializer.save()
        print(f"✅ Teacher user created: {user.username}")
        
        if hasattr(user, 'teacher'):
            teacher = user.teacher
            print(f"✅ Teacher profile created: {teacher.teacher_id}")
            print(f"   - Department: {teacher.department}")
            print(f"   - Qualification: {teacher.qualification}")
        else:
            print("❌ Teacher profile NOT created")
    else:
        print(f"❌ Teacher validation failed: {serializer.errors}")
except Exception as e:
    print(f"❌ Teacher creation error: {str(e)}")

# Test 3: Staff registration
print("\n3️⃣ Testing Staff Registration...")
staff_data = {
    'username': 'testvalidation3',
    'email': 'testval3@example.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!', 
    'first_name': 'Test',
    'last_name': 'Staff',
    'user_type': 'staff',
    'employee_id': 'STF001'
}

try:
    serializer = RegisterSerializer(data=staff_data)
    if serializer.is_valid():
        user = serializer.save()
        print(f"✅ Staff user created: {user.username}")
        
        if hasattr(user, 'staffprofile'):
            staff = user.staffprofile
            print(f"✅ Staff profile created: {staff.staff_id}")
            print(f"   - Employee ID: {staff.employee_id}")
            print(f"   - Position: {staff.position}")
        else:
            print("❌ Staff profile NOT created")
    else:
        print(f"❌ Staff validation failed: {serializer.errors}")
except Exception as e:
    print(f"❌ Staff creation error: {str(e)}")

print("\n" + "=" * 50)
print("🏁 Validation Complete!")

# Summary
total_users = CustomUser.objects.filter(username__startswith='testvalidation').count()
total_students = Student.objects.filter(user__username__startswith='testvalidation').count()
total_teachers = Teacher.objects.filter(user__username__startswith='testvalidation').count()
total_staff = StaffProfile.objects.filter(user__username__startswith='testvalidation').count()

print(f"\n📊 Summary:")
print(f"   - Users created: {total_users}")
print(f"   - Student profiles: {total_students}")
print(f"   - Teacher profiles: {total_teachers}")
print(f"   - Staff profiles: {total_staff}")

if total_users == 3 and total_students == 1 and total_teachers == 1 and total_staff == 1:
    print("\n🎉 ALL REGISTRATION TESTS PASSED!")
else:
    print("\n⚠️  Some registration tests failed. Check errors above.")
