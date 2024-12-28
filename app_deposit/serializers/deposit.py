from rest_framework import serializers
from app_deposit.models.deposit import Deposit
from app_profile.models.profile import Profile
from app_profile.serializers.profile import ProfileSerializer


class DepositListSerializer(serializers.ModelSerializer):
    merchant_details = serializers.SerializerMethodField()
    bank_details = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    requested_currency_details = serializers.SerializerMethodField()
    sent_currency_details = serializers.SerializerMethodField()


    class Meta:
        model = Deposit
        fields = [
            'merchant_id',
            'merchant_details',
            'customer_id',
            'bank',
            # 'bank_details',
            'agent_id',
            # 'agent_name',
            'order_id',
            'oxp_id',
            'txn_id',
            'requested_amount',
            'requested_currency',
            'requested_currency_details',
            'sent_amount',
            'sent_currency',
            'sent_currency_details',
            'created_on',
            'last_updated',
            'sender_account',
            'receiver_account',
            'agent_commission',
            'merchant_commission',
            'status'
        ]
        read_only_fields = ['merchant_details', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def get_merchant_details(self, obj):
        merchant = Profile.objects.get(id=obj.merchant_id)
        merchant_profile_serializer = ProfileSerializer(merchant)
        return merchant_profile_serializer.data


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"

        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
