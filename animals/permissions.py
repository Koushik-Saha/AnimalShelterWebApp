from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    """
    Allows access only to regular users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "user"

class IsStaff(BasePermission):
    """
    Allows access only to shelter staff.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "staff"

class IsAdmin(BasePermission):
    """
    Allows access only to admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admins to delete animals.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only staff users can modify (POST, PUT, DELETE)
        return request.user and request.user.is_staff

class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)