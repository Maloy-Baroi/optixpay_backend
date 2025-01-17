from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_auth.models import CustomPermission
from app_auth.serializers.users import PermissionSerializer
from services.is_admin import IsAdminUser
from utils.common_response import CommonResponse


class PermissionListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            permissions = CustomPermission.objects.all()
            permission_serializers = PermissionSerializer(permissions, many=True)
            return CommonResponse("success", permission_serializers.data, status.HTTP_200_OK, "Data Found!")
        except Exception as e:
            return CommonResponse("Error", {}, status.HTTP_204_NO_CONTENT, "Data Not Found!")

    def post(self, request, *args, **kwargs):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Permission Data Created!")
        return CommonResponse("error", serializer.data, status.HTTP_400_BAD_REQUEST, "Unsuccessful Creation!")

