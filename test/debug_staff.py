#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()

from accounts.api.serializers import RegisterSerializer

# Test staff data
staff_data = {
    'username': 'teststaff99',
    'email': 'teststaff99@example.com',
    'password': 'TestPass123!',
    'password_confirm': 'TestPass123!',
    'first_name': 'Test',
    'last_name': 'Staff',
    'user_type': 'staff',
    'employee_id': 'STF099'
}

print("Testing staff serializer...")
serializer = RegisterSerializer(data=staff_data)
print(f"Is valid: {serializer.is_valid()}")
if not serializer.is_valid():
    print(f"Errors: {serializer.errors}")
else:
    try:
        user = serializer.save()
        print(f"User created: {user.username}")
        if hasattr(user, 'staffprofile'):
            print(f"Staff profile created: {user.staffprofile.staff_id}")
            print(f"Employee ID: {user.staffprofile.employee_id}")
        else:
            print("No staff profile found")
    except Exception as e:
        print(f"Error during save: {e}")
        import traceback
        traceback.print_exc()
