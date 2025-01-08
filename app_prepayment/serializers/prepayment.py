from rest_framework import serializers

from app_prepayment.models.prepayment import Prepayment


class PrepaymentSerializer(serializers.ModelSerializer):
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
            'amount_bdt',
            'status',
            'is_active',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'created_by', 'updated_by', 'created_at', 'updated_at', 'is_active'
        ]
