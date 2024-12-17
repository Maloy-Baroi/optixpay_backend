import random

from django.conf import settings
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


# Create User
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            # Send OTP email
            otp = serializer.context['otp']

            cache = UserVerificationToken(user=user, token=otp)

            cache.save()  # OTP expires in 300 seconds (5 minutes)

            send_mail(
                'Verify Your Email',
                f'Your verification code is: {otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'User registered. Please check your email for verification code.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)

        if not user:
            return Response({"message": "No user found with this email!"}, status=status.HTTP_400_BAD_REQUEST)

        otp_cached = UserVerificationToken.objects.get(user=user)

        if otp_cached is None:
            return Response({"message": "No User found with this email"}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(1000, 9999)
        print("=============================================")
        print(otp)

        otp_cached.token = otp
        otp_cached.save()

        send_mail(
            'Verify Your Email',
            f'Your verification code is: {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Please check your email for resend verification code.'},
                        status=status.HTTP_201_CREATED)


# views.py
class VerifyOTPView(APIView):
    def post(self, request):
        email = str(request.data.get('email'))
        otp_provided = int(request.data.get('otp'))
        user = CustomUser.objects.get(email=email)

        otp_cached = UserVerificationToken.objects.get(user=user)

        if otp_cached is None:
            return Response({'error': 'OTP has expired or does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_provided == otp_cached.token:
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


# Login
class CustomTokenObtainPairView(TokenObtainPairView):

    @swagger_auto_schema(operation_summary="Login")
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
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
                return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                    'groups': groups,
                    'username': user.name
                    # 'permissions': permission_serializers
                }, status=status.HTTP_200_OK)
                # If password is correct, proceed to issue the token
                # return super().post(request, *args, **kwargs)
            else:
                # If password is incorrect, return an error response
                return Response({'detail': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        except CustomUser.DoesNotExist:
            # If the user does not exist, return an error response
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenRefreshView(TokenRefreshView):

    @swagger_auto_schema(operation_summary="Refresh Token Generator")
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if refresh_token is None:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({
                'access': access_token,
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
