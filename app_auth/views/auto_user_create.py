from django.contrib.auth.models import Group
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_auth.models import CustomUser
from app_auth.serializers.users import CustomUserSerializer
from utils.common_response import CommonResponse



class AutoCreateUserView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        group_name = request.data.get('group')

        if not all([email, username, password, group_name]):
            return CommonResponse("error", {"message": "All fields are required."}, status_code=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the group exists
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return CommonResponse("error", {"message": "Group not found."}, status_code=status.HTTP_404_NOT_FOUND)

        try:
            # Create the user and set their password
            user = CustomUser.objects.create_user(email=email, username=username, password=password)
            user.groups.add(group)
            user.save()
        except IntegrityError:
            return CommonResponse("error", {"message": "A user with that email or username already exists."},
                            status_code=status.HTTP_409_CONFLICT)

        # Serialize the user object
        data = CustomUserSerializer(user).data

        return CommonResponse("success", data=data, status_code=status.HTTP_201_CREATED)


