from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_auth.models import CustomUser
from app_auth.serializers.users import CustomUserSerializer
from utils.common_response import CommonResponse


class AutoCreateUserView(APIView):

    def post(self, request):
        email = request.data.get('email')

        user = CustomUser.objects.get(email=email, is_active=True)
        user.set_password("123456")
        user.save()
        data = CustomUserSerializer(user).data
        return CommonResponse("success", data, status.HTTP_201_CREATED)

