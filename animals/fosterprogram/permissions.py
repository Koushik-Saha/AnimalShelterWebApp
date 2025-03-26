from rest_framework.permissions import BasePermission


class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated