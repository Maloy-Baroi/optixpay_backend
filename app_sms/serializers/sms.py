from rest_framework import serializers

from app_sms.models.sms import SMSManagement


class SMSManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSManagement
        fields = [
            'id',  # Assuming you have an 'id' field as primary key
            'amount',
            'sender',
            'fee',
            'balance',
            'txn_id',
            'send_date',
            'status',
            'is_active'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
            'send_date': {'required': False},
        }

    # If needed, you can add custom validation for fields
    def validate_sender(self, value):
        # Example validation: ensure sender starts with a certain number
        if not value.startswith('01'):
            raise serializers.ValidationError("Sender must start with '01'.")
        return value

    # Additional methods like create or update can be customized if needed

class SMSManagementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSManagement
        fields = [
            'id',  # Assuming you have an 'id' field as primary key
            'amount',
            'sender',
            'fee',
            'balance',
            'txn_id',
            'send_date',
            'status',
            'is_active'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
        }
