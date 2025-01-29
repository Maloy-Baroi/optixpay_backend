from django.db.models import Q
from rest_framework import serializers
from app_deposit.models.deposit import Currency
from utils.validationerror_return import validation_error_return


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'currency_code', 'currency_symbol', 'is_active', 'created_by', 'updated_by',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'name', 'currency_code', 'currency_symbol', 'created_by', 'updated_by']


class CreateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'currency_code', 'currency_symbol']

    def create(self, validated_data):
        # Create the new currency record
        return Currency.objects.create(**validated_data)


class CurrencyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'currency_code', 'currency_symbol', 'is_active', 'created_by', 'updated_by',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'updated_by']
