from django.urls import path
from app_bank.views.banktype import BankTypeListAPIView, BankTypeUpdateAPIView, BankTypeDeleteAPIView
from app_bank.views.bank import BankUpdateAPIView, BankListCreateAPIView, BankDeleteAPIView

urlpatterns = [
    path('bank-types/', BankTypeListAPIView.as_view(), name='bank_type_list_create'),
    path('bank-types/update/<int:pk>/', BankTypeUpdateAPIView.as_view(), name='bank_type_detail'),
    path('bank-types/delete/<int:pk>/', BankTypeDeleteAPIView.as_view(), name='bank_type_detail'),

    path('bank/', BankListCreateAPIView.as_view(), name='bank-list-create'),
    path('bank/update/<int:pk>/', BankUpdateAPIView.as_view(), name='bank-detail-update'),
    path('bank/delete/<int:pk>/', BankDeleteAPIView.as_view(), name='bank-detail-delete'),
]
