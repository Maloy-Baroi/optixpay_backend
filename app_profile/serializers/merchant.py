from rest_framework import serializers

from app_profile.models.merchant import MerchantProfile


class MerchantProfileSerializer(serializers.ModelSerializer):
    authorization_details = serializers.SerializerMethodField()

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
