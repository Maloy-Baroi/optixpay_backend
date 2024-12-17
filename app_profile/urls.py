from django.urls import path
from app_profile.views.profile import ProfileListCreateAPIView, ProfileRetrieveUpdateAPIView

urlpatterns = [
    path('profiles/', ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', ProfileRetrieveUpdateAPIView.as_view(), name='profile-retrieve-update'),
]
