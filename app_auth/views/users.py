import random
from multiprocessing import Process

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app_auth.models import CustomUser, UserVerificationToken
from app_auth.serializers.users import OTPVerificationSerializer, UserRegistrationSerializer
from services.isActiveUser import IsUserActive, is_user_active
from services.send_main import send_verification_email
from utils.common_response import CommonResponse

# Create User
import threading
from django.core.mail import send_mail
from django.conf import settings


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = serializer.save()
                otp = serializer.context['otp']

                cache = UserVerificationToken(user=user, token=otp)
                cache.save()

                # Start a new process for sending email
                email_process = Process(target=send_verification_email, args=(user.email, otp))
                email_process.start()

                return CommonResponse("success", {}, status.HTTP_201_CREATED,
                                      'User registered. Please check your email for verification code.')
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class ResendVerifyOTPView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            user = CustomUser.objects.get(email=email)

            if not user:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "No User found with this email")

            otp_cached = UserVerificationToken.objects.get(user=user)

            if otp_cached is None:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "No User found with this email")

            otp = random.randint(1000, 9999)

            otp_cached.token = otp
            otp_cached.save()

            # Start a new process for sending email
            email_process = Process(target=send_verification_email, args=(user.email, otp))
            email_process.start()

            return CommonResponse("success", {},
                                  status.HTTP_201_CREATED, 'Please check your email for resend verification code.')
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


# views.py
class VerifyOTPView(APIView):
    def post(self, request):
        try:
            email = str(request.data.get('email'))
            otp_provided = int(request.data.get('otp'))
            user = CustomUser.objects.get(email=email)

            otp_cached = UserVerificationToken.objects.get(user=user)

            if otp_cached is None:
                return CommonResponse("error", {},
                                      status.HTTP_400_BAD_REQUEST, 'OTP has expired or does not exist.')

            if otp_provided == otp_cached.token:
                user.is_active = True
                agent_group, created = Group.objects.get_or_create(name='agent')  # Ensure the agent group exists
                user.groups.add(agent_group)  # Add the user to the agent group
                user.save()
                return CommonResponse("success", {},
                                      status.HTTP_200_OK, 'Email verified successfully!')
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, 'Invalid OTP')

        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


# Login
class CustomTokenObtainPairView(TokenObtainPairView):

    @swagger_auto_schema(operation_summary="Login")
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            if not is_user_active(email):
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "User is not active.")

            # Retrieve user by email
            user = CustomUser.objects.get(email=email)

            # Check if the provided password matches the stored password
            if user.check_password(password):
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Get user groups
                groups = [i.name for i in user.groups.all()]
                permissions = user.user_permissions.all()

                # permission_serializers = PermissionSerializer(permissions, many=True)
                return CommonResponse("success", {
                    'refresh': str(refresh),
                    'access': access_token,
                    'groups': groups,
                    'username': user.username,
                    'email': user.email
                    # 'permissions': permission_serializers
                }, status.HTTP_200_OK, "Login Successful!")
                # If password is correct, proceed to issue the token
                # return super().post(request, *args, **kwargs)
            else:
                # If password is incorrect, return an error response
                return CommonResponse("error", {}, status.HTTP_401_UNAUTHORIZED, 'Invalid password')

        except CustomUser.DoesNotExist:
            # If the user does not exist, return an error response
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, 'User not found')


class CustomTokenRefreshView(TokenRefreshView):

    @swagger_auto_schema(operation_summary="Refresh Token Generator")
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        try:
            if refresh_token is None:
                return CommonResponse("error", {},
                                      status.HTTP_400_BAD_REQUEST, 'Refresh token is required')

            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return CommonResponse("success", {
                'access': access_token,
            }, status.HTTP_200_OK, "Refresh Token Generated Successfully")

        except TokenError as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Token Error!")
