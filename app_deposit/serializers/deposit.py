from rest_framework import serializers

from app_bank.serializers.bank import BankModelSerializer
from app_deposit.models.deposit import Deposit
from app_deposit.serializers.currency import CurrencySerializer
from app_profile.models.profile import Profile
from app_profile.serializers.profile import ProfileSerializer


class DepositListSerializer(serializers.ModelSerializer):
    merchant = ProfileSerializer(source='merchant_id', read_only=True)
    bank = BankModelSerializer(read_only=True)
    agent = ProfileSerializer(source='agent_id', read_only=True)
    requested_currency = CurrencySerializer(read_only=True)
    sent_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Deposit
        fields = [
            'merchant', 'customer_id', 'bank', 'agent', 'order_id',
            'oxp_id', 'txn_id', 'requested_amount', 'requested_currency',
            'sent_amount', 'sent_currency', 'created_on', 'last_updated',
            'sender_account', 'receiver_account', 'agent_commission',
            'merchant_commission', 'status'
        ]


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"

        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
