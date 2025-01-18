from rest_framework.permissions import BasePermission


class IsAgentUser(BasePermission):
    """
    Custom permission to only allow admins to access.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to the 'admin' group
        if request.user and request.user.is_authenticated and request.user.is_active:
            return request.user.groups.filter(name='agent').exists()
        return False

