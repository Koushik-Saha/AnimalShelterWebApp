from rest_framework.permissions import BasePermission
from rest_framework import permissions

class CanManageBehaviorAssessment(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in ['staff', 'admin']
        )

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff