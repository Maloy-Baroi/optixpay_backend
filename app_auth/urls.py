from django.urls import path

from app_auth.views.users import CustomTokenObtainPairView, CustomTokenRefreshView, VerifyOTPView, UserRegistrationView, \
    ResendVerifyOTPView

app_name = 'app_auth'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-verify-otp/', ResendVerifyOTPView.as_view(), name='verify-otp'),
    path('login/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('login/token/refresh/', CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
]
