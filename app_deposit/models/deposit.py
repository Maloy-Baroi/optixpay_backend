from django.db import models

from app_bank.models.bank import AgentBankModel
from app_profile.models.profile import Profile
import uuid

from core.models.BaseModel import BaseModel


class Currency(BaseModel):

    name = models.CharField(max_length=255, unique=True)
    currency_code =models.CharField(max_length=255,unique=True)
    currency_symbol = models.CharField(max_length=255)

    class Meta:
        db_table = 'currency'
        verbose_name = 'Currencies'

    def __str__(self):
        return f"{self.name} - {self.currency_symbol}"



class Deposit(BaseModel):
    # Foreign Key relationships
    merchant_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='merchant_deposits')
    customer_id = models.CharField(max_length=255)
    bank = models.ForeignKey(AgentBankModel, on_delete=models.CASCADE, related_name='bank_deposits')
    agent_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='agent_deposits')

    # Fields
    order_id = models.CharField(max_length=255, unique=True)  # Order ID from merchant's side
    oxp_id = models.CharField(max_length=255, unique=True)  # Created on our side
    txn_id = models.CharField(max_length=255, unique=True)  # Transaction ID from the bank
    requested_amount = models.FloatField(default=0)  # Amount requested by merchant
    requested_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="currency_request", null=True)  # Currency requested by merchant
    sent_amount = models.FloatField(default=0)  # Exact amount received
    sent_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="currency_receive", null=True)  # Bank currency
    created_on = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp of the last status update
    sender_account = models.CharField(max_length=20)  # Payer's/user's/player's bank number
    receiver_account = models.CharField(max_length=20)  # Agent's bank number
    agent_commission = models.FloatField(default=0.0)  # Agent commission
    merchant_commission = models.FloatField(default=0.0)  # Merchant commission
    status_choices = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
        ('Expired', 'Expired'),
        ('Under Review', 'Under Review'),
        ('On Hold', 'On Hold'),
        ('Declined', 'Declined'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')  # Status of the deposit

    def __str__(self):
        return f"Deposit {self.oxp_id} - {self.status}"

    class Meta:
        ordering = ['-created_on']  # Default sorting by created date descending

    # def save(self, *args, **kwargs):
    #     """Override save to automatically generate bank_unique_id before saving the instance."""
    #     if not self.oxp_id:
    #         self.oxp_id = str(uuid.uuid4())  # Generate a unique UUID as the bank_unique_id
    #     if not self.txn_id:
    #         self.txn_id = str(uuid.uuid4())  # Generate a unique UUID as the bank_unique_id
    #     super().save(*args, **kwargs)
