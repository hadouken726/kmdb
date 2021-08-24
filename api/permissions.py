from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        give_admin_permission = request.user.is_superuser and request.user.is_staff
        if view.__class__.__name__ == 'MovieView':
            if request.method == 'POST':    
                return give_admin_permission
        if view.__class__.__name__ == 'MovieDetailView':
            if request.method == 'DELETE':
                return give_admin_permission
        if view.__class__.__name__ == 'ReviewView':
            if request.method == 'GET':
                return give_admin_permission

class Any(BasePermission):
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'MovieView':
            if request.method == 'GET':    
                return True
        if view.__class__.__name__ == 'MovieDetailView':
            if request.method == 'GET':    
                return True

class IsCritic(BasePermission):
    def has_permission(self, request, view):
        give_admin_permission = not request.user.is_superuser and request.user.is_staff
        if view.__class__.__name__ == 'ReviewView':
            if request.method in ['GET', 'PUT', 'POST']:
                return give_admin_permission