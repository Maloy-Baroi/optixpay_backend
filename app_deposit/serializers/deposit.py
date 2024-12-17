# from rest_framework import serializers
# from app_deposit.models.deposit import Deposit

# class DepositSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Deposit
#         fields = '__all__'  # Include all fields of the Deposit model










# from rest_framework import serializers
# from app_deposit.models.deposit import Deposit
# from app_profile.models.profile import Profile
# from django.db.models import F, Q
# from decimal import Decimal

# class DepositSerializer(serializers.ModelSerializer):
#     # merchant = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Auto-assign current user
#     received_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)  # Calculated field

#     class Meta:
#         model = Deposit
#         fields = [
#             'id', 'merchant', 'customer', 'bank', 'agent', 'currency', 'order_id',
#             'oxp_id', 'txn_id', 'requested_amount', 'received_amount', 'sender_no',
#             'receiver_no', 'agent_commission', 'merchant_commission', 'status',
#             'created_on', 'last_updated',
#         ]
#         read_only_fields = ['merchant','oxp_id','txn_id', 'received_amount', 'status', 'created_on', 'last_updated']

#     def validate(self, data):
#         """
#         Custom validation to calculate `received_amount` and auto-assign `agent`.
#         """
#         # Calculate received_amount
#         # requested_amount = data.get('requested_amount')
#         # agent_commission = data.get('agent_commission')
#         # merchant_commission = data.get('merchant_commission')
#         # total_commission = (agent_commission + merchant_commission)/100
#         # data['received_amount'] = requested_amount - (requested_amount * total_commission)


#         requested_amount = data.get('requested_amount')
#         agent_commission = data.get('agent_commission', 0)  # Default to 0 if not provided
#         merchant_commission = data.get('merchant_commission', 0)  # Default to 0 if not provided

#         # Validate `requested_amount`
#         if requested_amount is None:
#             raise serializers.ValidationError({"requested_amount": "This field is required and cannot be None."})

#         # Ensure commissions are numbers and convert to Decimal
#         try:
#             agent_commission = Decimal(agent_commission)
#             merchant_commission = Decimal(merchant_commission)
#         except Exception as e:
#             raise serializers.ValidationError({"commission": "Commission values must be valid numbers."})

#         # Calculate total commission as a percentage (in Decimal)
#         total_commission = (agent_commission + merchant_commission) / Decimal(100)

#         # Calculate `received_amount` (ensure `requested_amount` is Decimal)
#         if not isinstance(requested_amount, Decimal):
#             requested_amount = Decimal(requested_amount)

#         data['received_amount'] = requested_amount - (requested_amount * total_commission)

#         # Assign an agent randomly from the same bank
#         bank = data.get('bank')

#         if not bank:
#             raise serializers.ValidationError({'bank': 'Bank is required to assign an agent.'})
#         # agents = Profile.objects.filter(Q(profile_type='AG') & Q(country='BD'))  # Customize the filter as needed
#         # if not agents.exists():
#         #     raise serializers.ValidationError({'agent': 'No agent available for this bank.'})
#         # data['agent'] = agents.order_by('?').first()

#         return data



from rest_framework import serializers
from app_deposit.models.deposit import Deposit

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'  # Use all fields, or specify specific fields if needed
        read_only_fields = ['merchant']