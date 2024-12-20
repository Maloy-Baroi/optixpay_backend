from django.urls import path
from app_bank.views.banktype import BankTypeListAPIView, BankTypeRetrieveAPIView
from app_bank.views.bank import BankModelAPIView, BankListCreateAPIView

urlpatterns = [
    path('bank-types/', BankTypeListAPIView.as_view(), name='bank_type_list_create'),
    path('bank-types/<int:pk>/', BankTypeRetrieveAPIView.as_view(), name='bank_type_detail'),

    path('bank/', BankListCreateAPIView.as_view(), name='bank-list-create'),
    path('bank/<int:pk>/', BankModelAPIView.as_view(), name='bank-detail-update-delete'),
]
