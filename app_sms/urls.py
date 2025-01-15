from django.urls import path

from app_sms.views.sms import SMSListAPIView, SMSCreateAPIView, SMSUpdateAPIView, SMSDeleteAPIView, GenerateAccessToken

urlpatterns = [
    path('sms/', SMSListAPIView.as_view(), name='sms_list'),
    path('sms/create/', SMSCreateAPIView.as_view(), name='sms_create'),
    path('sms/update/<int:pk>/', SMSUpdateAPIView.as_view(), name='sms_update'),
    path('sms/<int:pk>/', SMSDeleteAPIView.as_view(), name='sms_delete'),
    path('regenerate-token/', GenerateAccessToken.as_view(), name='regenerate_token'),
]
