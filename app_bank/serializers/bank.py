from rest_framework import serializers
from app_bank.models.bank import AgentBankModel
import uuid

class BankModelSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    # Set agent to the current user automatically
    class Meta:
        model = AgentBankModel
        fields = [
            'id', 'master_username', 'master_password', 'bank_unique_id', 'bank_name', 'bank_type', 'usage_for', 'agent',
            'account_number', 'minimum_amount', 'maximum_amount', 'daily_limit',
            'daily_usage', 'monthly_limit', 'monthly_usage', 'app_key', 'secret_key', 'is_active', 'status', 'category'
        ]
        read_only_fields = ['agent', 'bank_type', 'category', 'usage_for', 'bank_unique_id', 'created_by', 'updated_by',
                            'created_at', 'updated_at', 'status', 'category']  # These fields will be set automatically
        extra_kwargs = {
            "agent": {"required": False},
            "bank_type": {"required": False},
            "bank_unique_id": {"required": False},
            "usage_for": {"required": False},
        }

    def get_category(self, obj):
        return f"{obj.usage_for} {obj.bank_type.category}" if obj.bank_type.category else None

    def create(self, validated_data):
        # Auto-generate bank_unique_id
        validated_data['bank_unique_id'] = str(uuid.uuid4())

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Automatically set the agent (current user) during update as well if needed
        user = self.context['request'].user
        return super().update(instance, validated_data)
