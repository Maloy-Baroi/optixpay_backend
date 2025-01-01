from django_browser_reload.views import message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app_profile.models.profile import Profile
from app_profile.serializers.profile import ProfileSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class ProfileListCreateAPIView(APIView):
    """
    Handles listing all profiles and creating a new profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        profile_type = request.query_params.get('profile_type')
        queryset = Profile.objects.all()
        if profile_type:
            queryset = queryset.filter(profile_type=profile_type)
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            # Bind request data to serializer
            serializer = ProfileSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                # Save the profile with the authenticated user as the owner
                serializer.save(user=request.user, created_by=request.user, updated_by=request.user)
                return CommonResponse("success", data=serializer.data, status=status.HTTP_201_CREATED, message="Successfully created!")
            # Return validation errors
            return CommonResponse("errors", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class ProfileRetrieveUpdateAPIView(APIView):
    """
    Handles retrieving, updating, and soft-deleting a single profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return None

    def get(self, request, pk):
        profile = self.get_object(pk)
        if profile is None:
            return CommonResponse('error', {}, status.HTTP_404_NOT_FOUND, 'Profile not found.')
        serializer = ProfileSerializer(profile)
        return CommonResponse("success", data=serializer.data, status=status.HTTP_200_OK, message="Successfully retrieved!")

    def put(self, request, pk):
        profile = self.get_object(pk)
        if profile is None:
            return CommonResponse('error', {}, status.HTTP_404_NOT_FOUND, 'Profile not found.')
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", data=serializer.data, status=status.HTTP_200_OK, message="Successfully updated!")
        return CommonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        if profile is None:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND,  'Profile not found.')
        profile.soft_delete()
        return CommonResponse("success",{}, status.HTTP_204_NO_CONTENT, "Successfully deleted!")
