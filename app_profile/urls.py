from django.urls import path

from app_profile.views.agent import AgentProfileCreateAPIView, AgentProfileUpdateAPIView, AgentProfileDeleteAPIView, \
    AgentDetailsAPIView
from app_profile.views.merchant import MerchantProfileCreateAPIView, MerchantProfileUpdateAPIView, \
    MerchantProfileDeleteAPIView, MerchantListAPIView
from app_profile.views.profile import ProfileListCreateAPIView, ProfileRetrieveUpdateAPIView
from app_profile.views.staff import StaffListAPIView, StaffCreateAPIView, StaffProfileUpdateAPIView, StaffProfileDeleteAPIView
from app_profile.views.wallet import MerchantWalletAPIView

urlpatterns = [
    # path('profiles/', ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    # path('profiles/<int:pk>/', ProfileRetrieveUpdateAPIView.as_view(), name='profile-retrieve-update'),

    # path('user/list/', UserListAPIView.as_view(), name='user-list'),

    path('merchants/', MerchantListAPIView.as_view(), name='create-merchant-profile'),
    path('merchant/create/', MerchantProfileCreateAPIView.as_view(), name='create-merchant-profile'),
    path('merchant/update/<int:pk>/', MerchantProfileUpdateAPIView.as_view(), name='update-merchant-profile'),
    path('merchant/delete/<int:pk>/', MerchantProfileDeleteAPIView.as_view(), name='delete-merchant-profile'),

    path('agents/', AgentDetailsAPIView.as_view(), name='agent-list'),
    path('agent/create/', AgentProfileCreateAPIView.as_view(), name='create-agent-profile'),
    path('agent/update/<int:pk>/', AgentProfileUpdateAPIView.as_view(), name='update-agent-profile'),
    path('agent/delete/<int:pk>/', AgentProfileDeleteAPIView.as_view(), name='delete-agent-profile'),

    path('staffs/', StaffListAPIView.as_view(), name='agent-list'),
    path('staff/create/', StaffCreateAPIView.as_view(), name='agent-list'),
    path('staff/update/<int:pk>/', StaffProfileUpdateAPIView.as_view(), name='update-agent-profile'),
    path('staff/delete/<int:pk>/', StaffProfileDeleteAPIView.as_view(), name='delete-agent-profile'),
    path('wallets/', MerchantWalletAPIView.as_view(), name='merchant_wallet_list'),

]
