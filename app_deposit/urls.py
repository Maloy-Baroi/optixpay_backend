from django.urls import path
from app_deposit.views.deposit import DepositAPIView, DepositListAPIView, DepositCreateAPIView
from app_deposit.views.currency import CurrencyUpdateAPIView, CurrencyListPostAPIView, CurrencyDeleteAPIView, \
    CreateCurrencyAPIView
from app_deposit.views.deposit_p2c import VerifyMerchantView, DepositBKashPayView, BkashPaymentExecuteAPIView, \
    BkashPaymentInitiateAPIView
# from app_deposit.views.deposit_p2c import DepositBKashPayView, BkashPaymentInitiateAPIView, BkashPaymentExecuteAPIView
from app_deposit.views.deposit_p2p import DepositPtoPCreateAPIView, DepositTransactionIdSubmitAPIView

urlpatterns = [
    # path('bkash/grants/', DepositBKashPayView.as_view(), name='bkash-payment'),
    # path('bkash/create/', BkashPaymentInitiateAPIView.as_view(), name='bkash-initiate'),
    # path('bkash/execute/', BkashPaymentExecuteAPIView.as_view(), name='bkash-execute'),

    path('currency/', CurrencyListPostAPIView.as_view(), name='currency-list'),  # List and Create
    path('currency/create/', CreateCurrencyAPIView.as_view(), name='currency-create'),  # List and Create
    path('currency/update/<int:pk>/', CurrencyUpdateAPIView.as_view(), name='currency-detail'),
    # Retrieve, Update, Delete
    path('currency/delete/<int:pk>/', CurrencyDeleteAPIView.as_view(), name='currency-delete'),

    path('deposits/', DepositListAPIView.as_view(), name='deposit-list'),  # Deposit List
    path('deposit/create/', DepositCreateAPIView.as_view(), name='deposit-create-internal'),  # Deposit List
    path('merchants/verification/', VerifyMerchantView.as_view(), name='merchant-verification'),
    path('bkash/grants/', DepositBKashPayView.as_view(), name='merchant-verification'),
    path('bkash/execute/', BkashPaymentExecuteAPIView.as_view(), name='merchant-verification'),
    path('bkash/create/', BkashPaymentInitiateAPIView.as_view(), name='bkash-initiate'),
    path('deposit/external/', DepositPtoPCreateAPIView.as_view(), name='deposit-create'),
    path('deposit/external/update/', DepositTransactionIdSubmitAPIView.as_view(), name='deposit-update'),
    path('deposits/<int:pk>/', DepositAPIView.as_view(), name='deposit-detail'),  # Retrieve, Update, Delete
]
