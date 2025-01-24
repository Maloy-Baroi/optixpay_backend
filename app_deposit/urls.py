from django.urls import path
from app_deposit.views.deposit import DepositAPIView, DepositListAPIView, DepositPtoPCreateAPIView
from app_deposit.views.currency import CurrencyUpdateAPIView, CurrencyListPostAPIView, CurrencyDeleteAPIView, \
    CreateCurrencyAPIView

urlpatterns = [
    path('currency/', CurrencyListPostAPIView.as_view(), name='currency-list'),   # List and Create
    path('currency/create/', CreateCurrencyAPIView.as_view(), name='currency-create'),   # List and Create
    path('currency/update/<int:pk>/', CurrencyUpdateAPIView.as_view(), name='currency-detail'),  # Retrieve, Update, Delete
    path('currency/delete/<int:pk>/', CurrencyDeleteAPIView.as_view(), name='currency-delete'),

    path('deposits/', DepositListAPIView.as_view(), name='deposit-list'),   # Deposit List
    path('deposit/create/', DepositPtoPCreateAPIView.as_view(), name='deposit-create'),
    path('deposits/<int:pk>/', DepositAPIView.as_view(), name='deposit-detail'),  # Retrieve, Update, Delete
]
