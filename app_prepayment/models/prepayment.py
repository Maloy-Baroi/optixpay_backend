from django.db import models

from app_profile.models.agent import AgentProfile
from core.models.BaseModel import BaseModel


class Prepayment(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    agent_id = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='prepayment_agent')
    transaction_hash = models.CharField(max_length=100)
    amount_usdt = models.FloatField(default=0.0)
    sender_address = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=100)
    exchange_rate = models.FloatField(default=0.0)
    converted_amount = models.FloatField(default=0.0)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return self.order_id

