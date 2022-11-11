from django.core.exceptions import PermissionDenied
from functools import wraps

def is_superuser(view):
    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.is_superuser:    
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return _view



from rest_framework.permissions import IsAdminUser

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)