from django.db import models
from app_profile.models.profile import Profile
from app_bank.models.bank import AgentBankModel, BankTypeModel
from app_deposit.models.deposit import Currency
from core.models.BaseModel import BaseModel



class Withdraw(BaseModel):
    # Foreign Key relationships
    merchant_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='merchant_withdraw')
    customer_id = models.CharField(max_length=255)
    bank = models.ForeignKey(AgentBankModel, on_delete=models.CASCADE, related_name='bank_withdraw')
    # bank_type = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE, related_name='bank_type_withdraw')
    agent_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='agent_withdraw', null=True, blank=True)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_withdraw',null=True, blank=True)

    # Fields
    order_id = models.CharField(max_length=255, unique=True)  # Order ID from merchant's side
    oxp_id = models.CharField(max_length=255, unique=True)  # Created on our side
    txn_id = models.CharField(max_length=255, unique=True)  # Transaction ID from the bank
    requested_amount = models.FloatField(default=0)  # Amount requested by merchant
    requested_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='requested_currency_withdraw',null=True, blank=True)  # Currency requested by merchant
    sent_amount = models.FloatField(default=0)  # Exact amount received
    sent_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='sent_currency_withdraw',null=True, blank=True)  # Bank currency
    created_on = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp of the last status update
    # bank_id = models.CharField(max_length=255)  # Bank's unique ID
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