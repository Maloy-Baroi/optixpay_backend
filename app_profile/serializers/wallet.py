from rest_framework import serializers

from app_profile.models.wallet import MerchantWallet


class MerchantWalletSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    wallet_base_currency_name = serializers.CharField(source='wallet_base_currency.name', read_only=True)

    class Meta:
        model = MerchantWallet
        fields = [
            'bank',
            'bank_name',
            'balance',
            'wallet_base_currency_name',
            'wallet_base_currency',
            'withdraw_commission',
            'deposit_commission',
            'settlement_commission',
        ]


class MerchantWalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantWallet
        fields = [
            'bank',
            'balance',
            'wallet_base_currency',
            'withdraw_commission',
            'deposit_commission',
            'settlement_commission',
        ]
