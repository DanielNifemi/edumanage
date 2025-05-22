from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('account_login')
            
            # Superusers can access everything
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Convert single role to list
            roles = allowed_roles if isinstance(allowed_roles, (list, tuple)) else [allowed_roles]
            
            try:
                user_profile = request.user.userprofile
                if user_profile.user_type in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 
                        f"Access denied. This page requires one of these roles: {', '.join(roles)}")
                    return redirect('dashboard')
            except:
                messages.error(request, "User profile not found.")
                return redirect('dashboard')
            
        return _wrapped_view
    return decorator

def superuser_or_self(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this page.")
            return redirect('account_login')
        
        # Allow superusers
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
            
        # Check if the user is accessing their own data
        profile_type = kwargs.get('profile_type')
        if profile_type:
            try:
                user_profile = request.user.userprofile
                if user_profile.user_type == profile_type:
                    return view_func(request, *args, **kwargs)
            except:
                pass
                
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
            
    return _wrapped_view
