from datetime import timezone

from django.utils.datetime_safe import datetime

from core.models.BaseModel import BaseModel
from django.db import models


class SMSManagement(BaseModel):
    STATUS_CHOICES = [
        ('confirmed', 'confirmed'),
        ('claimed', 'claimed'),
        ('unclaimed', 'unclaimed'),
    ]

    amount = models.CharField(max_length=10)
    sender = models.CharField(max_length=20)
    fee = models.CharField(max_length=10)
    balance = models.CharField(max_length=10)
    txn_id = models.CharField(max_length=20, unique=True)
    send_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Unclaimed')

    class Meta:
        db_table = 'sms_table'

    def __str__(self):
        return f"Transaction {self.txn_id} by {self.sender}"

