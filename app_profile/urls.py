from django.urls import path

from app_profile.views.agent import AgentProfileCreateAPIView, AgentProfileUpdateAPIView, AgentProfileDeleteAPIView, \
    AgentDetailsAPIView
from app_profile.views.merchant import MerchantProfileCreateAPIView, MerchantProfileUpdateAPIView, \
    MerchantProfileDeleteAPIView
from app_profile.views.profile import ProfileListCreateAPIView, ProfileRetrieveUpdateAPIView

urlpatterns = [
    # path('profiles/', ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    # path('profiles/<int:pk>/', ProfileRetrieveUpdateAPIView.as_view(), name='profile-retrieve-update'),

    # path('user/list/', UserListAPIView.as_view(), name='user-list'),

    path('merchant/create/', MerchantProfileCreateAPIView.as_view(), name='create-merchant-profile'),
    path('merchant/update/<int:pk>/', MerchantProfileUpdateAPIView.as_view(), name='update-merchant-profile'),
    path('merchant/delete/<int:pk>/', MerchantProfileDeleteAPIView.as_view(), name='delete-merchant-profile'),

    path('agents/', AgentDetailsAPIView.as_view(), name='agent-list'),
    path('agent/create/', AgentProfileCreateAPIView.as_view(), name='create-merchant-profile'),
    path('agent/update/<int:pk>/', AgentProfileUpdateAPIView.as_view(), name='update-merchant-profile'),
    path('agent/delete/<int:pk>/', AgentProfileDeleteAPIView.as_view(), name='delete-merchant-profile'),
]
