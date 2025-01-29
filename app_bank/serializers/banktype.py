from django.db.models import Q
from rest_framework import serializers, status
from app_bank.models.bank import BankTypeModel
from utils.common_response import CommonResponse
from utils.validationerror_return import validation_error_return


class BankTypeModelSerializer(serializers.ModelSerializer):
    currency_name = serializers.SerializerMethodField()
    class Meta:
        model = BankTypeModel
        fields = [
            "name",
            "category",
            "currency",
            "currency_name",
            "is_active",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def get_currency_name(self, obj):
        return obj.currency.name

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Set updated_by to the current user (created_by should not change on update)
        user = self.context['request'].user
        validated_data['updated_by'] = user
        return super().update(instance, validated_data)


class BankTypeOnlyNameSerializer(serializers.Serializer):
    name = serializers.CharField()

