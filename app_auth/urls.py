from django.urls import path

from app_auth.views.permissions import PermissionListAPIView
from app_auth.views.reset_password import SendOTPView, ResetPasswordAPIView, VerifyOTPAPIVIew
from app_auth.views.users import CustomTokenObtainPairView, CustomTokenRefreshView, VerifyOTPView, UserRegistrationView, \
    ResendVerifyOTPView

app_name = 'app_auth'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-verify-otp/', ResendVerifyOTPView.as_view(), name='verify-otp'),

    path('reset-password-otp/', SendOTPView.as_view(), name='send-otp'),
    path('reset-password-verify-otp/', VerifyOTPAPIVIew.as_view(), name='send-otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('login/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('login/token/refresh/', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    path('permissions/', PermissionListAPIView.as_view(), name='permissions'),
]
