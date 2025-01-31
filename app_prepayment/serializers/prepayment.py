from rest_framework import serializers

from app_prepayment.models.prepayment import Prepayment
from app_profile.models.agent import AgentProfile


class PrepaymentSerializer(serializers.ModelSerializer):
    agent_unique_id = serializers.CharField(source='agent_id.unique_id')
    class Meta:
        model = Prepayment
        fields = [
            'id',
            'agent_id',
            'agent_unique_id',
            'transaction_hash',
            'amount_usdt',
            'sender_address',
            'receiver_address',
            'exchange_rate',
            'converted_amount',
            'platform_id',
            'payment_id',
            'status',
            'note',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
            'is_active',
            'platform_id',
            'payment_id',
            'agent_id',
        ]

        extra_kwargs = {
            'agent_id': {'required': False},
            'status': {'required': False},
        }

    def create(self, validated_data):
        agent_id = self.context.get('agent_id')
        agent = AgentProfile.objects.get(id=agent_id)
        exchange_rate = 128.89
        amount_usdt = validated_data['amount_usdt']
        validated_data['exchange_rate'] = exchange_rate
        validated_data['converted_amount'] = float(amount_usdt) * exchange_rate
        validated_data['agent_id'] = agent

        return Prepayment.objects.create(**validated_data)

class PrepaymentUpdateSerializer(serializers.ModelSerializer):

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
            'status',
            'note',
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
