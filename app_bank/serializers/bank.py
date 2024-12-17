
# from rest_framework import serializers
# from app_bank.models.bank import BankModel
# from app_profile.models.profile import Profile

# class BankSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = BankModel
#         fields = [
#             'id', 'bank_unique_id', 'bank_name', 'bank_type', 'agent', 'account_number',
#             'minimum_amount', 'maximum_amount', 'daily_limit', 'monthly_limit'
#         ]
#         read_only_fields = ['bank_unique_id', 'agent', 'daily_usage', 'monthly_usage', 'app_key', 'secret_key']

#     def validate_account_number(self, value):
#         """
#         Validate that the account number starts with +880 and contains 9-10 digits.
#         """
#         if not value.startswith('+880') or not value[4:].isdigit() or not (9 <= len(value[4:]) <= 10):
#             raise serializers.ValidationError("Account number must start with +880 and contain 9-10 digits.")
#         return value

#     # def validate(self, data):
#     #     """
#     #     Custom validation to check the limits.
#     #     """
#     #     # Ensure that the minimum_amount is less than or equal to the maximum_amount
#     #     if data.get('minimum_amount') > data.get('maximum_amount', 0):
#     #         raise serializers.ValidationError({"minimum_amount": "Minimum amount cannot be greater than the maximum amount."})

#     #     # Ensure the daily and monthly limits are non-negative
#     #     if data.get('daily_limit', 0) < 0 or data.get('monthly_limit', 0) < 0:
#     #         raise serializers.ValidationError({"daily_limit": "Limit must be greater than or equal to 0."})

#     #     return data

#     def validate(self, data):
#         """
#         Custom validation to check the limits.
#         """
#         minimum_amount = data.get('minimum_amount', 0)  # Default to 0 if not provided
#         maximum_amount = data.get('maximum_amount', 0)  # Default to 0 if not provided
#         daily_limit = data.get('daily_limit', 0)        # Default to 0 if not provided
#         monthly_limit = data.get('monthly_limit', 0)    # Default to 0 if not provided

#         # Ensure that the minimum_amount is less than or equal to the maximum_amount
#         if minimum_amount > maximum_amount:
#             raise serializers.ValidationError({"minimum_amount": "Minimum amount cannot be greater than the maximum amount."})

#         # Ensure the daily and monthly limits are non-negative
#         if daily_limit < 0 or monthly_limit < 0:
#             raise serializers.ValidationError({"daily_limit": "Limit must be greater than or equal to 0."})

#         return data






from rest_framework import serializers
from app_bank.models.bank import BankModel
import uuid

class BankModelSerializer(serializers.ModelSerializer):
    # Set agent to the current user automatically
    class Meta:
        model = BankModel
        fields = [
            'id', 'bank_unique_id', 'bank_name', 'bank_type', 'agent',
            'account_number', 'minimum_amount', 'maximum_amount', 'daily_limit',
            'daily_usage', 'monthly_limit', 'monthly_usage', 'app_key', 'secret_key', 'is_active'
        ]
        read_only_fields = ['bank_unique_id', 'agent','app_key', 'secret_key']  # These fields will be set automatically

    def create(self, validated_data):
        # Automatically set the agent (current user)
        # user = self.context['request'].user
        # validated_data['agent'] = user
        user = self.context['request'].user

        validated_data['created_by'] = user
        validated_data['updated_by'] = user

        # Auto-generate bank_unique_id
        validated_data['bank_unique_id'] = str(uuid.uuid4())

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Automatically set the agent (current user) during update as well if needed
        user = self.context['request'].user

        validated_data['created_by'] = user
        validated_data['updated_by'] = user


        return super().update(instance, validated_data)
