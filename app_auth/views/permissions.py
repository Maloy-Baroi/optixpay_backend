import json

from django.contrib.auth.models import Permission, Group
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_auth.models import CustomUser
from app_auth.serializers.serializers import PermissionSerializer


class PermissionListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_groups = user.groups.all()  # Fetch user groups
            permissions = set()  # Use a set to avoid duplicates

            # Collect all permissions from the user's groups
            for group in user_groups:
                for perm in group.permissions.all():
                    permissions.add(perm)  # Add individual permissions to the set

            # Serialize the flat list of permissions
            permission_serializer = PermissionSerializer(list(permissions), many=True)

            return Response({"data": permission_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePermissionsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            # Retrieve and validate the user's ID from the request
            user_id = request.data.get("user", None)
            if not user_id:
                return Response(
                    {"error": "User's ID is required to change the permission"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Retrieve and validate the group name from the request
            group_name = request.data.get("group_name", None)
            if not group_name:
                return Response(
                    {"error": "Group name is required to change the permission"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Retrieve permissions from the request (optional)
            permission_codenames = request.data.get("permissions", [])
            if not isinstance(permission_codenames, list):
                return Response(
                    {"error": "Permissions must be provided as a list of codenames"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": f"User with ID {user_id} does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Fetch the group
            group = Group.objects.filter(name=group_name).first()
            if not group:
                return Response(
                    {"error": f"Group '{group_name}' not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Check if the user is associated with the group
            if not user.groups.filter(id=group.id).exists():
                return Response(
                    {"error": f"User '{user.username}' is not associated with group '{group_name}'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch the permissions
            permissions_to_add = Permission.objects.filter(codename__in=permission_codenames)
            if permissions_to_add.count() != len(permission_codenames):
                return Response(
                    {"error": "Some or all of the permissions were not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Update group permissions
            group.permissions.set(permissions_to_add)
            group.save()

            return Response(
                {
                    "message": f"Permissions updated successfully for group '{group_name}'.",
                    "updated_permissions": [perm.codename for perm in permissions_to_add],
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


