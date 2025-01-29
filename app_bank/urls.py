from django.urls import path
from app_bank.views.banktype import BankTypeListAPIView, BankTypeUpdateAPIView, BankTypeDeleteAPIView
from app_bank.views.banktype import BankTypeCreateAPIView
from app_bank.views.bank import BankUpdateAPIView, BankListAPIView, BankDeleteAPIView, BankCreateAPIView

urlpatterns = [
    path('bank-types/', BankTypeListAPIView.as_view(), name='bank_type_list'),
    path('bank-type/create/', BankTypeCreateAPIView.as_view(), name='bank_type_create'),
    path('bank-types/update/<int:pk>/', BankTypeUpdateAPIView.as_view(), name='bank_type_detail'),
    path('bank-types/delete/<int:pk>/', BankTypeDeleteAPIView.as_view(), name='bank_type_detail'),

    path('banks/', BankListAPIView.as_view(), name='bank-list'),
    path('bank/create/', BankCreateAPIView.as_view(), name='bank-create'),
    path('bank/update/<int:pk>/', BankUpdateAPIView.as_view(), name='bank-detail-update'),
    path('bank/delete/<int:pk>/', BankDeleteAPIView.as_view(), name='bank-detail-delete'),
]
