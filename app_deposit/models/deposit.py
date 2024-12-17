from django.db import models
from app_profile.models.profile import Profile
from app_bank.models.bank import BankModel

import uuid

class Currency(models.Model):

    name = models.CharField(max_length=255, unique=True)
    currency_code =models.CharField(max_length=255,unique=True)
    currency_symbol = models.CharField(max_length=255)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='currency')

    def __str__(self):
        return f"{self.name} - {self.currency_symbol}"



class Deposit(models.Model):
    # Foreign Key relationships
    merchant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='merchant_deposits')
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='customer_deposits')
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE, related_name='bank_deposits')
    agent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='agent_deposits')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_deposits')

    # Fields
    order_id = models.CharField(max_length=255, unique=True)  # Order ID from merchant's side
    oxp_id = models.CharField(max_length=255, unique=True)  # Created on our side
    txn_id = models.CharField(max_length=255, unique=True)  # Transaction ID from the bank
    requested_amount = models.DecimalField(max_digits=15, decimal_places=2)  # Amount requested by merchant
    # requested_currency = models.CharField(max_length=10)  # Currency requested by merchant
    received_amount = models.DecimalField(max_digits=15, decimal_places=2)  # Exact amount received
    # received_currency = models.CharField(max_length=10)  # Bank currency
    created_on = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp of the last status update
    # bank_id = models.CharField(max_length=255)  # Bank's unique ID
    sender_no = models.CharField(max_length=20)  # Payer's/user's/player's bank number
    receiver_no = models.CharField(max_length=20)  # Agent's bank number
    agent_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)  # Agent commission
    merchant_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)  # Merchant commission
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
