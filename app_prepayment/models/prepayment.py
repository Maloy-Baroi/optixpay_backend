from django.db import models

from core.models.BaseModel import BaseModel


class Prepayment(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    order_id = models.CharField(max_length=100, unique=True)
    agent_id = models.CharField(max_length=100)
    transaction_hash = models.CharField(max_length=100)
    amount_usdt = models.FloatField(default=0.0)
    sender_address = models.CharField(max_length=100)
    receiver_address = models.CharField(max_length=100)
    exchange_rate = models.FloatField(default=0.0)
    amount_bdt = models.FloatField(default=0.0)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.order_id

