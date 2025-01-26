from locale import currency

from rest_framework import serializers
from app_profile.models.merchant import MerchantProfile  # Import the model if it's in a separate file
from app_deposit.models.deposit import Currency  # Make sure the import is correct
from app_profile.models.wallet import MerchantWallet
from app_settlement.models.settlement import Settlement
from utils.optixpay_id_generator import generate_settlement_id


class SettlementSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant_id.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)

    class Meta:
        model = Settlement
        fields = ['id', 'settlement_id', 'merchant_name', 'currency_code', 'amount', 'commission_percentage',
                  'amount_after_commission', 'txn_id', 'usdt_address', 'status']


class SettlementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = [
            'wallet',
            'amount',
            'usdt_address',
        ]

    def create(self, validated_data):
        amount = validated_data.get('amount', None)
        usdt_address = validated_data.get('usdt_address', None)
        wallet = validated_data.get('wallet', None)

        merchant_id = self.context.get('merchant_id', None)
        settlement_id = generate_settlement_id()

        wallet_obj = MerchantWallet.objects.get(id=wallet)

        if wallet is None or amount is None or usdt_address is None:
            raise serializers.ValidationError("Value Missing!")

        settlement = Settlement(
            settlement_id = settlement_id,
            merchant_id = merchant_id,
            wallet = wallet_obj,
            currency = wallet_obj.wallet_base_currency,
            amount = amount,
            commission_percentage = "0.0",
            amount_after_commission = amount,
            txn_id = "",
            usdt_address = usdt_address,
            status = "pending"
        )

        settlement.save()

        return settlement
