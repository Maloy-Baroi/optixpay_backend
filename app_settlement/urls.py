from django.urls import path

from app_settlement.views.settlement import SettlementCreateAPIView, SettlementListAPIView, SettlementUpdateAPIView

urlpatterns = [
    path('settlements/', SettlementListAPIView.as_view(), name='settlements'),
    path('settlement/create/', SettlementCreateAPIView.as_view(), name='settlement'),
    path('settlement/update/<int:pk>/', SettlementUpdateAPIView.as_view(), name='settlement'),
]
