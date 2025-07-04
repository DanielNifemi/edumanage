# Debug and Fix Summary - EduManage Authentication & Schedule API

## Overview
This document summarizes the debugging and fixing process for login and schedule API endpoints in the EduManage Django + React (Vite) application running in Docker containers.

## Issues Encountered

### 1. Initial Backend Startup Problems
- **Problem**: Backend container failing to start with "Network Error" and "ERR_EMPTY_RESPONSE"
- **Root Cause**: Missing `STATIC_ROOT` configuration for Django's collectstatic command in Docker
- **Fix**: Added `STATIC_ROOT = BASE_DIR / 'staticfiles'` to `settings.py`

### 2. Missing Dependencies
- **Problem**: Backend startup error due to missing JWT library
- **Root Cause**: `djangorestframework-simplejwt` not in requirements.txt
- **Fix**: Added `djangorestframework-simplejwt` to `requirements.txt`

### 3. Frontend Authentication 404 Errors
- **Problem**: Frontend getting 404 errors when calling `/auth/login/` endpoint
- **Root Cause**: Incorrect API endpoint URLs in frontend - confusion between `/api/auth/login/` vs `/auth/login/`
- **Fix**: Updated frontend API base URL configuration to ensure correct endpoint paths

### 4. Authentication 403/400 Errors
- **Problem**: Login attempts returning "Unable to log in with provided credentials" even with correct data
- **Root Cause**: Test user didn't exist in database or had incorrect password hash
- **Fix**: Created proper Django management command to create test user with correct UserProfile

### 5. Schedule API Double `/api` Prefix Issue
- **Problem**: Frontend calling `/api/schedules/api/schedules/by-teacher/` resulting in 404 errors
- **Root Cause**: URL structure had nested `/api` prefixes:
  - Main URLs: `/api/` → `edumanage.api`
  - Schedule app: `schedules/` → `schedules.api.urls`
  - Schedule URLs: `api/` → router.urls
- **Fix**: Removed extra `api/` prefix from `schedules/api/urls.py`

### 6. User Model Configuration Issues
- **Problem**: Management command failed with `TypeError: CustomUser() got unexpected keyword arguments: 'role'`
- **Root Cause**: `CustomUser` model doesn't have `role` field - role is stored in `UserProfile.user_type`
- **Fix**: Updated management command to properly create user and associated UserProfile

## Files Modified

### Backend Changes

#### 1. `edumanage/settings.py`
```python
# Added for Docker static file collection
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Enhanced CORS configuration
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]

# CSRF exemptions for API
CSRF_EXEMPT_URLS = [r'^/api/.*$']
```

#### 2. `requirements.txt`
```
# Added missing JWT dependency
djangorestframework-simplejwt
```

#### 3. `schedules/api/urls.py`
```python
# Fixed double /api prefix issue
urlpatterns = [
    path('', include(router.urls)),  # Changed from 'api/'
    # Custom endpoints updated to remove /api prefix
    path('schedules/by-teacher/', ScheduleViewSet.as_view({'get': 'by_teacher'})),
    # ... other endpoints
]
```

#### 4. `accounts/management/commands/create_test_user.py`
```python
# New management command to create test user properly
user = CustomUser.objects.create_user(
    username='simple_user',
    email='simple@test.com',
    password='test123',
    first_name='Simple',
    last_name='User',
    is_active=True
)

profile = UserProfile.objects.create(
    user=user,
    user_type='teacher'  # Correct way to set role
)
profile.create_specific_profile()  # Creates Teacher profile
```

### Frontend Changes

#### 5. `frontend/src/lib/api.ts`
```typescript
// Fixed schedule API endpoints
export const schedulesAPI = {
  getByUser: async (userType: string, userId: string) => {
    if (userType === 'teacher') {
      // Fixed: removed double /api prefix
      const response = await api.get(`/schedules/schedules/by-teacher/?teacher_id=${userId}`);
      return response.data;
    }
    // ... other cases
  }
};
```

## Testing and Verification

### 1. Authentication Testing
```bash
# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"simple@test.com","password":"test123"}'

# Response: ✅ JWT tokens and user data returned
```

### 2. Schedule API Testing
```bash
# Test with authentication
JWT_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
curl -H "Authorization: Bearer $JWT_TOKEN" \
  "http://localhost:8000/api/schedules/schedules/by-teacher/?teacher_id=5"

# Response: ✅ Endpoint accessible (returns empty data as expected)
```

### 3. Frontend Integration
- ✅ Frontend can successfully authenticate users
- ✅ JWT tokens are properly stored and sent with requests
- ✅ Schedule API calls no longer return 404/403 errors
- ✅ CORS issues resolved

## Current System State

### User Credentials
- **Email**: `simple@test.com`
- **Password**: `test123`
- **Role**: Teacher (user_type in UserProfile)
- **User ID**: 5
- **Teacher ID**: TCH000005

### API Endpoints Working
- `POST /api/auth/login/` - User authentication ✅
- `GET /api/schedules/schedules/` - All schedules ✅
- `GET /api/schedules/schedules/by-teacher/?teacher_id=5` - Teacher schedules ✅
- `GET /api/schedules/schedules/by-class/?class_id=X` - Class schedules ✅

### Services Running
- **Backend**: `http://localhost:8000` (Django + PostgreSQL)
- **Frontend**: `http://localhost:5173` (React + Vite)
- **Database**: PostgreSQL in Docker container

## Key Learnings

1. **URL Structure**: Avoid nested `/api` prefixes in Django URL configuration
2. **User Models**: Distinguish between `CustomUser` fields vs `UserProfile` fields
3. **Docker Static Files**: Always configure `STATIC_ROOT` for production-like environments
4. **CORS Configuration**: Comprehensive CORS setup needed for Docker + frontend communication
5. **JWT Authentication**: Proper token validation and refresh mechanisms essential
6. **Management Commands**: Create dedicated commands for test data setup

## Next Steps

1. **Add Sample Data**: Create schedules, courses, and other test data
2. **Clean Up Debug Code**: Remove temporary debug endpoints and logging
3. **Error Handling**: Improve frontend error handling for API failures
4. **Performance**: Optimize database queries for schedule endpoints
5. **Testing**: Add automated tests for authentication and API endpoints

## Commands Used

### Docker Management
```bash
docker-compose up -d              # Start all services
docker-compose restart web       # Restart backend
docker-compose logs web --tail=20 # Check backend logs
```

### Django Management
```bash
docker-compose exec web python manage.py create_test_user  # Create test user
docker-compose exec web python manage.py migrate          # Apply migrations
```

### API Testing
```bash
# Login and get JWT
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"simple@test.com","password":"test123"}'

# Use JWT for authenticated requests
curl -H "Authorization: Bearer $JWT_TOKEN" \
  "http://localhost:8000/api/schedules/schedules/"
```

---

**Status**: ✅ **RESOLVED** - Authentication and Schedule API endpoints are now fully functional
**Date**: July 4, 2025
**Environment**: Docker + Django + React + PostgreSQL
