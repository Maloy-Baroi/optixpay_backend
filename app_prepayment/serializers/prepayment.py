from rest_framework import serializers

from app_prepayment.models.prepayment import Prepayment


class PrepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prepayment
        fields = [
            'id',
            'agent_id',
            'transaction_hash',
            'amount_usdt',
            'sender_address',
            'receiver_address',
            'exchange_rate',
            'converted_amount',
            'platform_id',
            'payment_id',
            'status',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active'
        ]

        extra_kwargs = {
            'agent_id': {'required': False},
            'status': {'required': False},
        }

class PrepaymentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prepayment
        fields = [
            'id',
            'order_id',
            'agent_id',
            'transaction_hash',
            'amount_usdt',
            'sender_address',
            'receiver_address',
            'exchange_rate',
            'converted_amount',
            'status',
            'is_active',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'created_at', 'updated_at'
        ]

        extra_kwargs = {
            'agent_id': {'required': False},
            'status': {'required': False},
            'created_by': {'required': False},
            'updated_by': {'required': False},
            'is_active': {'required': False},
        }
