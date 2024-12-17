from rest_framework import serializers
from app_withdraw.models.withdraw import Withdraw

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'  # Use all fields, or specify specific fields if needed
        read_only_fields = ['merchant']