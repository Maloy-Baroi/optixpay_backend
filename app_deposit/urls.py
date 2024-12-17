from django.urls import path
from app_deposit.views.deposit import DepositAPIView
from app_deposit.views.currency import CurrencyAPIView

urlpatterns = [
    path('currency/', CurrencyAPIView.as_view(), name='currency-list'),   # List and Create
    path('currency/<int:pk>/', CurrencyAPIView.as_view(), name='currency-detail'),  # Retrieve, Update, Delete


    path('deposits/', DepositAPIView.as_view(), name='deposit-list'),   # List and Create
    path('deposits/<int:pk>/', DepositAPIView.as_view(), name='deposit-detail'),  # Retrieve, Update, Delete
]
