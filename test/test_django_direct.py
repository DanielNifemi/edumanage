#!/usr/bin/env python
"""
Test Django models directly to isolate registration issues
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.models import CustomUser, UserProfile
from students.models import Student
from teachers.models import Teacher
from staff.models import StaffProfile

def test_user_creation():
    print("🧪 Testing User Creation Directly")
    print("=" * 50)
    
    import time
    timestamp = int(time.time())
    
    try:
        # Test 1: Create a basic user
        print("1. Creating basic user...")
        user = CustomUser.objects.create_user(
            username=f'testuser_{timestamp}',
            email=f'test_{timestamp}@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        print(f"   ✅ User created: {user.username}")
        
        # Test 2: Create UserProfile
        print("2. Creating user profile...")
        profile = UserProfile.objects.create(user=user, user_type='student')
        print(f"   ✅ Profile created: {profile.user_type}")
        
        # Test 3: Create Student profile
        print("3. Creating student profile...")
        student = Student.objects.create(
            user=user,
            student_id=f"STU{user.id:06d}",
            grade='Not set',
            address='Not set',
            parent_name='Not set',
            parent_contact='Not set'
        )
        print(f"   ✅ Student created: {student.student_id}")
        
        print("\n✅ Manual user creation successful!")
        
    except Exception as e:
        print(f"❌ Error in manual creation: {e}")
        import traceback
        traceback.print_exc()

def test_serializer():
    print("\n🧪 Testing RegisterSerializer")
    print("=" * 50)
    
    from accounts.api.serializers import RegisterSerializer
    import time
    timestamp = int(time.time())
    
    data = {
        'username': f'serializertest_{timestamp}',
        'email': f'serializer_{timestamp}@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Serializer',
        'last_name': 'Test',
        'user_type': 'student'
    }
    
    try:
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"✅ Serializer test successful: {user.username}")
        else:
            print(f"❌ Serializer validation failed: {serializer.errors}")
    except Exception as e:
        print(f"❌ Serializer error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()
    test_serializer()
