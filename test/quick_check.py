import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
django.setup()
from accounts.models import CustomUser
users = CustomUser.objects.filter(username__startswith='finaltest_')
print(f'Created test users: {users.count()}')
for user in users:
    profile_type = user.userprofile.user_type if hasattr(user, 'userprofile') else 'No profile'
    print(f'- {user.username}: {profile_type}')
