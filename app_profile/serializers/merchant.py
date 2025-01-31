from rest_framework import serializers

from app_bank.serializers.banktype import BankTypeOnlyNameSerializer
from app_profile.models.merchant import MerchantProfile
from app_profile.models.wallet import MerchantWallet


class MerchantWalletForMerchantProfileSerializer(serializers.ModelSerializer):
    balance_amount = serializers.SerializerMethodField()

    class Meta:
        model = MerchantWallet
        fields = [
            'id',
            'balance_amount',
        ]

    def get_balance_amount(self, obj):
        return f"{obj.wallet_base_currency.currency_code} {obj.balance}"


class MerchantProfileSerializer(serializers.ModelSerializer):
    authorization_details = serializers.SerializerMethodField()
    merchant_wallet = MerchantWalletForMerchantProfileSerializer(many=True, read_only=True)
    payment_methods = BankTypeOnlyNameSerializer(many=True, read_only=True)

    class Meta:
        model = MerchantProfile
        fields = ['id', 'user', 'authorization_details', 'name', 'phone_number', 'unique_id', 'logo', 'payment_methods',
                  'status', 'is_active',
                  'merchant_wallet', 'app_key', 'secret_key']
        extra_kwargs = {
            'app_key': {'read_only': True},
            'secret_key': {'read_only': True},
            'user': {'read_only': True},
            'authorization_details': {'read_only': True},
            'unique_id': {'read_only': True},
        }

    def get_authorization_details(self, obj):
        # Only return non-sensitive information related to authorization
        return {
            "email": obj.user.email,
            "username": obj.user.username,
        }

    def get_merchant_wallet(self, obj):
        obj


class MerchantUpdateProfileSerializer(serializers.ModelSerializer):
    authorization_details = serializers.SerializerMethodField()

    class Meta:
        model = MerchantProfile
        fields = ['id', 'user', 'authorization_details', 'name', 'phone_number', 'unique_id', 'logo', 'payment_methods',
                  'status',
                  'merchant_wallet', 'app_key', 'secret_key']
        extra_kwargs = {
            'app_key': {'read_only': True},
            'secret_key': {'read_only': True},
            'user': {'read_only': True},
            'authorization_details': {'read_only': True},
            'unique_id': {'read_only': True},
            'name': {'required': False},  # Explicitly mark as required if not already handled in the model
            'logo': {'required': False},  # If the logo is optional, set required as False
        }

    def get_authorization_details(self, obj):
        # Only return non-sensitive information related to authorization
        return {
            "email": obj.user.email,
            "username": obj.user.username,
        }

    def validate_logo(self, value):
        """
        Add custom validation for the logo to ensure a file is provided if necessary.
        """
        if not value and self.instance and not self.instance.logo:
            raise serializers.ValidationError("No file was submitted for the logo.")
        return value
