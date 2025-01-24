from rest_framework import serializers
from app_profile.models.merchant import MerchantProfile  # Import the model if it's in a separate file
from app_deposit.models.deposit import Currency  # Make sure the import is correct
from app_settlement.models.settlement import Settlement


class SettlementSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant_id.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)

    class Meta:
        model = Settlement
        fields = ['id', 'settlement_id', 'merchant_name', 'currency_code', 'amount', 'commission_percentage',
                  'amount_after_fees', 'txn_id', 'usdt_address', 'status']
