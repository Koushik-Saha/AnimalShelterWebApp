from rest_framework.permissions import BasePermission

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