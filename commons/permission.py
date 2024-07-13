from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return func(request, *args, **kwargs)
            else:
                return  HttpResponseForbidden("You are not allowed to perform this action.")
        return wrap
    return decorator