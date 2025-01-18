from rest_framework.permissions import BasePermission


class IsMerchantUser(BasePermission):
    """
    Custom permission to only allow admins to access.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to the 'admin' group
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name='merchant').exists()
        return False

    def has_object_permission(self, request, view, obj):
        # Merchants can only modify if status is 'Pending'
        if request.user.groups.filter(name='merchant').exists():
            return obj.status == 'Pending'
        # Other authenticated users can modify regardless of status
        return True
