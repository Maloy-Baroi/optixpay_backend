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
        try:
            email = request.data.get('email')
            username = request.data.get('username')
            password = request.data.get('password')
            group_name = request.data.get('group')

            if not all([email, username, password, group_name]):
                CommonResponse("error", {"message": "All fields are required."},
                                      status_code=status.HTTP_400_BAD_REQUEST)

            group, create = Group.objects.get_or_create(name=group_name)

            try:
                # Create the user and set their password
                user = CustomUser.objects.create_user(email=email, username=username, password=password)
                user.groups.add(group)
                user.save()
                # Serialize the user object
                data = CustomUserSerializer(user).data

                CommonResponse("success", data=data, status_code=status.HTTP_201_CREATED)
            except IntegrityError:
                CommonResponse("error", {"message": "A user with that email or username already exists."},
                                      status_code=status.HTTP_409_CONFLICT)

        except Exception as e:
            print(str(e))
            CommonResponse("error", {"message": str(e)}, status.HTTP_400_BAD_REQUEST)


