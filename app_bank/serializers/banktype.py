from rest_framework import serializers
from app_bank.models.bank import BankTypeModel

class BankTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTypeModel
        exclude = ['created_by', 'updated_by']  # Exclude these fields from the input

    def create(self, validated_data):
        # Set created_by and updated_by to the current user
        user = self.context['request'].user
        
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Set updated_by to the current user (created_by should not change on update)
        user = self.context['request'].user
        validated_data['updated_by'] = user
        return super().update(instance, validated_data)


class BankTypeOnlyNameSerializer(serializers.Serializer):
    name = serializers.CharField()

