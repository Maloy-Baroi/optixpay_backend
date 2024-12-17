from rest_framework import serializers
from app_deposit.models.deposit import  Currency




class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        read_only_fields = ['created_by']

    def validate_name(self, value):
        """
        Ensure the name is not blank and follows specific rules.
        """
        if not value.strip():
            raise serializers.ValidationError("The name cannot be empty or whitespace.")
        # if not value.isalnum():
        #     raise serializers.ValidationError("The name must contain only alphanumeric characters.")
        return value
