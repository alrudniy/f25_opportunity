from rest_framework import permissions

from accounts.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'organization'):
            return obj.organization.user == request.user
        return False


class IsOrganizationUser(permissions.BasePermission):
    """
    Allows access only to organization users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == User.UserType.ORGANIZATION


class IsStudentUser(permissions.BasePermission):
    """
    Allows access only to student users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == User.UserType.STUDENT
