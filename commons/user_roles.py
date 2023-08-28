from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden
# from dashboard.userinfo.models import RoleGroup





def customer_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            logout(request=request)

        return func(request, *args, **kwargs)

    return wrapper


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("you are not allowed")
    return wrapper_function

# def check_permission(module_name, permission):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             if not request.user.is_authenticated:
#                 return HttpResponseForbidden()
                
#             user_role = request.user.role.name
#             check_permission = False
            
#             if user_role == 'admin':
#                 check_permission = True
#             else:
#                 permission_field = f'{permission.lower()}'
#                 role_permission = RoleGroup.objects.filter(name=module_name).values(permission_field).first()
                
#                 if role_permission:
#                     check_permission = role_permission[permission_field]
            
#             if check_permission:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponseForbidden()
            
#         return _wrapped_view
#     return decorator




