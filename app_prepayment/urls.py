from django.urls import path

from app_prepayment.views.prepayment import PrepaymentListAPIView, PrepaymentUpdateAPIView, PrepaymentDeleteAPIView, \
    WebhookAPIView

urlpatterns = [
    path('webhooks/passimpay/', WebhookAPIView.as_view(), name='passimpay_webhook'),
    path('payments/', PrepaymentListAPIView.as_view(), name='prepayment-list'),
    path('payment/update/<int:pk>/', PrepaymentUpdateAPIView.as_view(), name='prepayment-list'),
    path('payment/delete/<int:pk>/', PrepaymentDeleteAPIView.as_view(), name='prepayment-list'),
]
