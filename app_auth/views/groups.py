from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_auth.models import CustomGroup
from app_auth.serializers.users import GroupSerializer
from services.is_admin import IsAdminUser
from utils.common_response import CommonResponse


class CustomGroupListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            group_id = request.query_params.get('group_id', None)
            groups = CustomGroup.objects.all()
            if group_id:
                group = groups.filter(id=group_id)
                group_serializers = GroupSerializer(group)
                return CommonResponse("success", group_serializers.data, status.HTTP_200_OK, "Data Found!")
            group_serializers = GroupSerializer(groups, many=True)
            return CommonResponse("success", group_serializers.data, status.HTTP_200_OK, "Data Found!")
        except Exception as e:
            return CommonResponse("error", str(e), status.HTTP_400_BAD_REQUEST, "Data Not Found")

    def post(self, request):
        try:
            name = request.data.get("name")
            group = CustomGroup.objects.filter(name=name)

            if group.exists():
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, f"Group {name} already exists")

            group = CustomGroup.objects.create(name=name)
            group_serializers = GroupSerializer(group)
            return CommonResponse("success", group_serializers.data, status.HTTP_201_CREATED, "Successfully Created")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Unsuccessful Creation!")


class CustomGroupUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, pk):
        try:
            group_id = pk
            group = CustomGroup.objects.filter(id=group_id)
            group_name = request.data.get("name")
            permissions = request.data.get("permissions", [])

            if not group.exists():
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Group not found!")

            group = CustomGroup.objects.get(id=group_id)
            if group_name:
                group.name = group_name
            if permissions:
                group.permissions = permissions
            group.save()
            return CommonResponse("success", {}, status.HTTP_200_OK, "Data Updated Successfully!")
        except Exception as e:
            return CommonResponse("error", str(e), status.HTTP_204_NO_CONTENT, "Data Not Found")



class CustomGroupDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, pk):
        try:
            group = CustomGroup.objects.get(id=pk)
            if group:
                group.delete()
                return CommonResponse("success", {}, status.HTTP_200_OK, "Data Deleted Successfully!")
            else:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Group not found!")
        except Exception as e:
            return CommonResponse("error", str(e), status.HTTP_204_NO_CONTENT, "Data Not Found")
