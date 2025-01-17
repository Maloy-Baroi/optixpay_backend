from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView

from app_auth.models import CustomUser, CustomGroup
from app_auth.serializers.users import CustomUserSerializer
from utils.common_response import CommonResponse

class AutoCreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        group_name = request.data.get('group')

        if not all([email, username, password, group_name]):
            return CommonResponse("error", {"message": "All fields are required."},
                                  status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the group exists or create a new one
            group, created = CustomGroup.objects.get_or_create(name=group_name)

            # Create the user and save them to the database
            user = CustomUser(email=email, username=username, is_active=True)
            user.set_password(password)
            user.save()  # Explicitly save the user to ensure the id is set before adding to many-to-many fields

            # Add user to the group
            user.groups.add(group)

            # Serialize the user object
            data = CustomUserSerializer(user).data
            return CommonResponse("success", data=data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return CommonResponse("error", {"message": "A user with that email or username already exists."},
                                  status=status.HTTP_409_CONFLICT)
        except Exception as e:
            # Handle unexpected exceptions
            return CommonResponse("error", {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
