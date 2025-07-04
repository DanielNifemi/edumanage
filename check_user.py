from accounts.models import CustomUser, UserProfile

def check_user():
    email = 'simple@test.com'
    try:
        user = CustomUser.objects.get(email=email)
        print(f'User exists: {user.email}, ID: {user.id}, Role: {user.role}')
        print(f'Password check: {user.check_password("test123")}')
        
        # Check UserProfile
        try:
            profile = UserProfile.objects.get(user=user)
            print(f'UserProfile exists: ID {profile.id}')
        except UserProfile.DoesNotExist:
            print('UserProfile missing, creating...')
            profile = UserProfile.objects.create(user=user, phone_number='+1234567890')
            print('UserProfile created')
            
    except CustomUser.DoesNotExist:
        print('User does not exist, creating...')
        user = CustomUser.objects.create_user(
            email=email,
            username='simple_user',
            password='test123',
            first_name='Simple',
            last_name='User',
            is_active=True,
            role='teacher'
        )
        profile = UserProfile.objects.create(user=user, phone_number='+1234567890')
        print(f'User created: {user.email}, ID: {user.id}')

check_user()
