from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app_profile.models.profile import Profile
from app_profile.serializers.profile import ProfileSerializer

class ProfileListCreateAPIView(APIView):
    """
    Handles listing all profiles and creating a new profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        List all profiles that are active (not soft-deleted).
        """
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new profile.
        """
        serializer = ProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveUpdateAPIView(APIView):
    """
    Handles retrieving, updating, and soft-deleting a single profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific profile by ID.
        """
        try:
            profile = self.get_object(pk)
            if not profile:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProfileSerializer(profile)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update a specific profile by ID.
        """
        profile = self.get_object(pk)
        is_active = request.data.get("is_active")
        if not profile:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user, is_active=is_active)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Soft-delete a specific profile by ID.
        """
        profile = self.get_object(pk)
        if not profile:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        profile.soft_delete()
        return Response({"message": "Profile soft-deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
