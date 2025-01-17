from pkg_resources import require
from rest_framework import serializers
from app_withdraw.models.withdraw import Withdraw

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = [
            'id',
            'merchant_id',
            'customer_id',
            'bank',
            'agent_id',
            'order_id',
            'oxp_id',
            'txn_id',
            'requested_amount',
            'requested_currency',
            'sent_amount',
            'sent_currency',
            'sender_account',
            'receiver_account',
            'agent_commission',
            'merchant_commission',
            'status'
        ]

    merchant_id = serializers.PrimaryKeyRelatedField(read_only=True)
    bank = serializers.PrimaryKeyRelatedField(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    requested_currency = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    sent_currency = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    status = serializers.ChoiceField(choices=Withdraw.status_choices)

    def validate_customer_id(self, value):
        # Example validation: customer ID must be non-empty
        if not value:
            raise serializers.ValidationError("Customer ID must be provided.")
        return value

    def validate(self, data):
        # Add custom validation logic if necessary
        return data


class WithdrawCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = [
            'id',
            'merchant_id',
            'customer_id', # yes
            'bank',
            'agent_id',
            'order_id',
            'oxp_id',
            'txn_id',
            'requested_amount', # yes
            'requested_currency', # yes
            'sent_amount',
            'sent_currency',
            'sender_account', # yes
            'receiver_account',
            'agent_commission',
            'merchant_commission',
            'status' # yes
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'merchant_id': {'read_only': True, 'required': False},
            'bank': {'read_only': True, 'required': False},
            'agent_id': {'read_only': True, 'required': False},
            'order_id': {'read_only': True, 'required': False},
            'oxp_id': {'read_only': True, 'required': False},
            'txn_id': {'read_only': True, 'required': False},
            'sent_amount': {'read_only': True, 'required': False},
            'sent_currency': {'read_only': True, 'required': False},
            'receiver_account': {'read_only': True, 'required': False},
            'agent_commission': {'read_only': True, 'required': False},
            'merchant_commission': {'read_only': True, 'required': False},
        }
