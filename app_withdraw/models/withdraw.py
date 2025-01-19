from django.db import models

from app_profile.models.agent import AgentProfile
from app_profile.models.merchant import MerchantProfile
from app_profile.models.profile import Profile
from app_bank.models.bank import AgentBankModel, BankTypeModel
from app_deposit.models.deposit import Currency
from core.models.BaseModel import BaseModel



class Withdraw(BaseModel):
    # Foreign Key relationships
    merchant_id = models.ForeignKey(MerchantProfile, on_delete=models.CASCADE, related_name='merchant_withdraw', null=True, blank=True)
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    bank = models.ForeignKey(AgentBankModel, on_delete=models.CASCADE, related_name='bank_withdraw', null=True, blank=True)
    # bank_type = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE, related_name='bank_type_withdraw')
    agent_id = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='agent_withdraw', null=True, blank=True)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_withdraw',null=True, blank=True)

    # Fields
    order_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Order ID from merchant's side
    oxp_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Created on our side
    txn_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Transaction ID from the bank
    requested_amount = models.FloatField(default=0)  # Amount requested by merchant
    requested_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='requested_currency_withdraw',null=True, blank=True)  # Currency requested by merchant
    sent_amount = models.FloatField(default=0)  # Exact amount received
    sent_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='sent_currency_withdraw',null=True, blank=True)  # Bank currency
    sender_account = models.CharField(max_length=20, null=True, blank=True)  # Payer's/user's/player's bank number
    receiver_account = models.CharField(max_length=20, null=True, blank=True)  # Agent's bank number
    agent_commission = models.FloatField(default=0.0)  # Agent commission
    merchant_commission = models.FloatField(default=0.0)  # Merchant commission
    status_choices = [
        ('Assigned', 'Assigned'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')  # Status of the deposit
    success_callbackurl = models.CharField(max_length=255, null=True, blank=True)
    failed_callbackurl = models.CharField(max_length=255, null=True, blank=True)
    cancel_callbackurl = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Deposit {self.oxp_id} - {self.status}"

    class Meta:
        ordering = ['-created_at']  # Default sorting by created date descending