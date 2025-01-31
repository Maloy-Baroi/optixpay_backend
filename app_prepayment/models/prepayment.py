from django.db import models

from app_profile.models.agent import AgentProfile
from core.models.BaseModel import BaseModel


class Prepayment(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('failed', 'failed'),
    ]

    agent_id = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='prepayment_agent')
    transaction_hash = models.CharField(max_length=100)
    amount_usdt = models.FloatField(default=0.0)
    sender_address = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=100)
    exchange_rate = models.FloatField(default=0.0)
    converted_amount = models.FloatField(default=0.0)
    platform_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    # note = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'prepayment'


    def save(self, *args, **kwargs):
        self.exchange_rate = 128.89
        self.converted_amount = float(self.amount_usdt) * 129.1
        super(Prepayment, self).save(*args, **kwargs)

