# from django.urls import path
# from .views.banktype import BankTypeSuperUserAPIView,BankTypeAPIView
# from .views.bank import BankListRetrieveAPIView, BankPostPutDeleteAPIView

# urlpatterns = [
#     path('banktypes-super/', BankTypeSuperUserAPIView.as_view(), name='banktype'),
#     path('banktypes-super/<int:pk>/', BankTypeSuperUserAPIView.as_view(), name='banktype-detail'),

#     path('banktypes/', BankTypeAPIView.as_view(), name='banktype-list'),
#     path('banktypes/<int:pk>/', BankTypeAPIView.as_view(), name='banktype-user'),




#     path('banks/', BankListRetrieveAPIView.as_view(), name='bank-list'),
#     path('banks/<int:pk>/', BankListRetrieveAPIView.as_view(), name='bank-detail'),

#     # Create, update, and delete endpoints
#     path('banks/manage/', BankPostPutDeleteAPIView.as_view(), name='bank-create'),
#     path('banks/manage/<int:pk>/', BankPostPutDeleteAPIView.as_view(), name='bank-update-delete'),
# ]







from django.urls import path
from app_bank.views.banktype import BankTypeModelAPIView
from app_bank.views.bank import BankModelAPIView

urlpatterns = [
    path('bank-types/', BankTypeModelAPIView.as_view(), name='bank_type_list_create'),
    path('bank-types/<int:pk>/', BankTypeModelAPIView.as_view(), name='bank_type_detail'),

    path('bank/', BankModelAPIView.as_view(), name='bank-list-create'),
    path('bank/<int:pk>/', BankModelAPIView.as_view(), name='bank-detail-update-delete'),
]
