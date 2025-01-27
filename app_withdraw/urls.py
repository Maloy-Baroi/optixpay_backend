from django.urls import path

from app_withdraw.views.withdraw import WithdrawListAPIView, WithdrawCreateAPIView, \
    WithdrawDeleteAPIView, WithdrawUpdateAPIView, BankTypeForWithdrawCreateAPIView, WithdrawCreateP2PExternalAPIView, MerchantWalletListAPIView

urlpatterns = [
    path('withdraws/', WithdrawListAPIView.as_view(), name='deposit-list'),   # List
    path('withdraw/create/internal/', WithdrawCreateAPIView.as_view(), name='deposit-create'),   # List
    path('withdraw/create/', WithdrawCreateP2PExternalAPIView.as_view(), name='deposit-create'),   # List
    path('withdraw/update/<int:pk>/', WithdrawUpdateAPIView.as_view(), name='deposit-update'),  # Retrieve, Update, Delete
    path('withdraw/delete/<int:pk>/', WithdrawDeleteAPIView.as_view(), name='deposit-delete'),  # Retrieve, Update, Delete
    path('bank-list/', BankTypeForWithdrawCreateAPIView.as_view(), name='bank-list'),
    path('wallets/', MerchantWalletListAPIView.as_view(), name='merchant_wallet_list'),
]
