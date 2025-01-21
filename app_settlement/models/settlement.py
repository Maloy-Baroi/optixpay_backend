from django.db import models

from core.models.BaseModel import BaseModel


class Settlement(BaseModel):
    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    settlement_id = models.CharField(max_length=20, unique=True)
    merchant_id = models.ForeignKey('app_profile.MerchantProfile', on_delete=models.CASCADE, null=True)
    currency = models.ForeignKey('app_bank.Currency', on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_percentage = models.FloatField()
    amount_after_fees = models.FloatField()
    txn_id = models.CharField(max_length=20, unique=True)
    usdt_address = models.CharField(max_length=34)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.settlement_id} - {self.merchant_id.name}"
