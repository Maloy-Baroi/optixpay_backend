from requests import request
from rest_framework import serializers

from app_profile.models.merchant import MerchantProfile
from app_profile.models.wallet import MerchantWallet


class MerchantWalletSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    wallet_base_currency_name = serializers.CharField(source='wallet_base_currency.name', read_only=True)

    class Meta:
        model = MerchantWallet
        fields = [
            'id',
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

    def create(self, validated_data):
        # Get the merchant_id from the context
        merchant_id = self.context.get('merchant_id', None)

        # Fetch the merchant profile
        merchant = MerchantProfile.objects.filter(id=merchant_id).first()
        if merchant is None:
            raise ValueError('Merchant not found!')

        # Create the MerchantWallet instance
        merchant_wallet = MerchantWallet.objects.create(**validated_data)

        # Associate the created wallet with the merchant profile
        merchant.merchant_wallet.add(merchant_wallet)

        return merchant_wallet


class MerchantWalletUpdateSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            'bank': {'required': False},
            'balance': {'required': False},
            'wallet_base_currency': {'required': False},
            'withdraw_commission': {'required': False},
            'deposit_commission': {'required': False},
            'settlement_commission': {'required': False},
        }

    def update(self, instance, validated_data):
        # Update the instance with validated data
        instance.bank = validated_data.get('bank', instance.bank)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.wallet_base_currency = validated_data.get('wallet_base_currency', instance.wallet_base_currency)
        instance.withdraw_commission = validated_data.get('withdraw_commission', instance.withdraw_commission)
        instance.deposit_commission = validated_data.get('deposit_commission', instance.deposit_commission)
        instance.settlement_commission = validated_data.get('settlement_commission', instance.settlement_commission)

        # Save the updated instance
        instance.save()
        return instance

