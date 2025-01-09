from django.urls import path
from app_deposit.views.deposit import DepositAPIView, DepositListAPIView
from app_deposit.views.currency import CurrencyUpdateAPIView, CurrencyListPostAPIView, CurrencyDeleteAPIView

urlpatterns = [
    path('currency/', CurrencyListPostAPIView.as_view(), name='currency-list'),   # List and Create
    path('currency/update/<int:pk>/', CurrencyUpdateAPIView.as_view(), name='currency-detail'),  # Retrieve, Update, Delete
    path('currency/delete/<int:pk>/', CurrencyDeleteAPIView.as_view(), name='currency-delete'),


    path('deposits/', DepositListAPIView.as_view(), name='deposit-list'),   # List and Create
    path('deposits/<int:pk>/', DepositAPIView.as_view(), name='deposit-detail'),  # Retrieve, Update, Delete
]
