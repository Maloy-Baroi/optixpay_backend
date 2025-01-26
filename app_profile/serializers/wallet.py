from rest_framework import serializers

from app_profile.models.wallet import MerchantWallet


class MerchantWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantWallet
        fields = '__all__'
