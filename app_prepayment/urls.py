from django.urls import path

from app_prepayment.views.prepayment import PrepaymentListAPIView, PrepaymentUpdateAPIView, PrepaymentDeleteAPIView

urlpatterns = [
    path('payments/', PrepaymentListAPIView.as_view(), name='prepayment-list'),
    path('payment/update/<int:pk>/', PrepaymentUpdateAPIView.as_view(), name='prepayment-list'),
    path('payments/delete/<int:pk>/', PrepaymentDeleteAPIView.as_view(), name='prepayment-list'),
]
