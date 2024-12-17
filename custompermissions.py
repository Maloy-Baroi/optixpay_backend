from rest_framework.permissions import BasePermission
from app_profile.models.profile import Profile

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsAgent(BasePermission):
    """
    Custom permission to allow only users whose profile type is 'AG' (Agent).
    """

    def has_permission(self, request, view):
        # Get the user's profile based on the authenticated user
        profile = Profile.objects.filter(user=request.user).first()

        if profile and profile.profile_type == 'AG':
            return True
        return False


class IsMerchant(BasePermission):
    """
    Custom permission to allow only users whose profile type is 'AG' (Agent).
    """

    def has_permission(self, request, view):
        # Get the user's profile based on the authenticated user
        profile = Profile.objects.filter(user=request.user).first()

        if profile and profile.profile_type == 'MC':
            return True
        return False
