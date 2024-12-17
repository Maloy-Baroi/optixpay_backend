from django.urls import path
from app_deposit.views.deposit import DepositAPIView
from app_withdraw.views.withdraw import WithdrawAPIView, WithdrawListAPIView

urlpatterns = [
    path('withdraw/', WithdrawListAPIView.as_view(), name='deposit-list'),   # List and Create
    path('withdraw/<int:pk>/', WithdrawAPIView.as_view(), name='deposit-detail'),  # Retrieve, Update, Delete
]