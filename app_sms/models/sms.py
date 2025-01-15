from core.models.BaseModel import BaseModel
from django.db import models


class SMSManagement(BaseModel):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Refused', 'Refused'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender = models.CharField(max_length=20)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    trx_id = models.CharField(max_length=20, unique=True)
    send_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'sms_table'

    def __str__(self):
        return f"Transaction {self.trx_id} by {self.sender}"

