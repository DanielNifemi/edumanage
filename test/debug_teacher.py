#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.api.serializers import RegisterSerializer

# Test teacher data
teacher_data = {
    'username': 'testteacher99',
    'email': 'testteacher99@example.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Test',
    'last_name': 'Teacher',
    'user_type': 'teacher',
    'employee_id': 'TCH099',
    'department': 'Mathematics'
}

print("Testing teacher serializer...")
serializer = RegisterSerializer(data=teacher_data)
print(f"Is valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")
else:
    try:
        user = serializer.save()
        print(f"User created: {user.username}")
        if hasattr(user, 'teacher'):
            print(f"Teacher profile created: {user.teacher.teacher_id}")
        else:
            print("No teacher profile found")
    except Exception as e:
        print(f"Error during save: {e}")
        import traceback
        traceback.print_exc()
