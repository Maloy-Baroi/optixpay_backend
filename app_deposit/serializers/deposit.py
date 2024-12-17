from rest_framework import serializers
from app_deposit.models.deposit import Deposit

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'  # Use all fields, or specify specific fields if needed
        # read_only_fields = ['merchant']