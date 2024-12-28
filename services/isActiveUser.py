from rest_framework.permissions import BasePermission

from app_auth.models import CustomUser


class IsUserActive(BasePermission):
    """
    Custom permission to allow access only to active users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and active
        return request.user and request.user.is_active


def is_user_active(email):
    user = CustomUser.objects.get(email=email)
    return user.is_active
