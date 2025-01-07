from rest_framework import serializers

from app_bank.models.bank import AgentBankModel
from app_bank.serializers.bank import BankModelSerializer
from app_profile.models.agent import AgentProfile


class AgentProfileSerializer(serializers.ModelSerializer):
    authorization_details = serializers.SerializerMethodField()
    bank_details = serializers.SerializerMethodField()

    class Meta:
        model = AgentProfile
        fields = [
            'id',
            'user',
            'authorization_details',
            'unique_id',
            'name',
            'phone_number',
            'bank_details',
            'status',
            'is_active'
        ]

        extra_kwargs = {
            'user': {'read_only': True},
            'authorization_details': {'read_only': True},
            'unique_id': {'read_only': True},
            'bank_details': {'read_only': True},
        }

    def get_authorization_details(self, obj):
        # Only return non-sensitive information related to authorization
        return {
            "email": obj.user.email,
            "username": obj.user.username,
        }

    def get_bank_details(self, obj):
        try:
            bank = AgentBankModel.objects.filter(agent=obj)
            bank_serializers = BankModelSerializer(bank, many=True)
            return bank_serializers.data
        except AgentBankModel.DoesNotExist:
            return {}