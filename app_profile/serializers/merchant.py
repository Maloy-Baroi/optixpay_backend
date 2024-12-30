from rest_framework import serializers

from app_profile.models.merchant import MerchantProfile


class MerchantProfileSerializer(serializers.ModelSerializer):
    authorization_details = serializers.SerializerMethodField()

    class Meta:
        model = MerchantProfile
        fields = ['id', 'user', 'authorization_details', 'name', 'phone_number', 'unique_id', 'logo', 'payment_methods', 'status',
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
