from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admins to access.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to the 'admin' group
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name='admin').exists()
        return False

    def has_object_permission(self, request, view, obj):
        # Optional: Check permissions for read/write operations
        # For simplicity, just reuse the `has_permission`
        return self.has_permission(request, view)
