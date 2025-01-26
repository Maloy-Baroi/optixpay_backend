from django.urls import path

from app_settlement.views.settlement import SettlementCreateAPIView

urlpatterns = [
    path('settlement/create/', SettlementCreateAPIView.as_view(), name='settlement'),
]
