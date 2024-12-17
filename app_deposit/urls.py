# from django.urls import path
# from app_deposit.views.deposit import (
#     CreateDepositAPIView,
#     RetrieveDepositAPIView,
#     UpdateDepositAPIView,
#     DeleteDepositAPIView
# )

# urlpatterns = [
#     path('deposits/create/', CreateDepositAPIView.as_view(), name='create-deposit'),
#     path('deposits/<int:pk>/', RetrieveDepositAPIView.as_view(), name='retrieve-deposit'),
#     path('deposits/<int:pk>/update/', UpdateDepositAPIView.as_view(), name='update-deposit'),
#     path('deposits/<int:pk>/delete/', DeleteDepositAPIView.as_view(), name='delete-deposit'),
# ]


# from django.urls import path
# from app_deposit.views.deposit import DepositListCreateView, DepositDetailView
# from app_deposit.views.currency import CurrencyAPIView,CurrencySuperUserAPIView

# urlpatterns = [
#     path('currency-super/', CurrencySuperUserAPIView.as_view(), name='currency'),
#     path('currency-super/<int:pk>/', CurrencySuperUserAPIView.as_view(), name='currency-detail'),

#     path('currency/', CurrencyAPIView.as_view(), name='currency-list'),
#     path('currency/<int:pk>/', CurrencyAPIView.as_view(), name='currency-user'),

#     path('deposits/', DepositListCreateView.as_view(), name='deposit-list-create'),
#     path('deposits/<int:pk>/', DepositDetailView.as_view(), name='deposit-detail'),
# ]


from django.urls import path
from app_deposit.views.deposit import DepositAPIView
from app_deposit.views.currency import CurrencyAPIView

urlpatterns = [
    path('currency/', CurrencyAPIView.as_view(), name='currency-list'),   # List and Create
    path('currency/<int:pk>/', CurrencyAPIView.as_view(), name='currency-detail'),  # Retrieve, Update, Delete


    path('deposits/', DepositAPIView.as_view(), name='deposit-list'),   # List and Create
    path('deposits/<int:pk>/', DepositAPIView.as_view(), name='deposit-detail'),  # Retrieve, Update, Delete
]
