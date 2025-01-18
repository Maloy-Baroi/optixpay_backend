from random import choice

from pkg_resources import require
from requests import request
from rest_framework import serializers, status

from app_bank.models.bank import BankTypeModel, AgentBankModel
from app_profile.models.agent import AgentProfile
from app_profile.models.merchant import MerchantProfile
from app_withdraw.models.withdraw import Withdraw
from utils.common_response import CommonResponse
from utils.generate_order_id import generate_order_id
from utils.optixpay_id_generator import generate_opx_id


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = [
            'id',
            'merchant_id',
            'customer_id',
            'bank',
            'agent_id',
            'order_id',
            'oxp_id',
            'txn_id',
            'requested_amount',
            'requested_currency',
            'sent_amount',
            'sent_currency',
            'sender_account',
            'receiver_account',
            'agent_commission',
            'merchant_commission',
            'status'
        ]

    merchant_id = serializers.PrimaryKeyRelatedField(read_only=True)
    bank = serializers.PrimaryKeyRelatedField(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    requested_currency = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    sent_currency = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    status = serializers.ChoiceField(choices=Withdraw.status_choices)

    def validate_customer_id(self, value):
        # Example validation: customer ID must be non-empty
        if not value:
            raise serializers.ValidationError("Customer ID must be provided.")
        return value

    def validate(self, data):
        # Add custom validation logic if necessary
        return data


class WithdrawCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = [
            'id',
            'merchant_id',
            'customer_id',  # yes
            'bank',
            'agent_id',
            'order_id',
            'oxp_id',
            'txn_id',
            'requested_amount',  # yes
            'requested_currency',  # yes
            'sent_amount',
            'sent_currency',
            'sender_account',
            'receiver_account', # yes
            'agent_commission',
            'merchant_commission',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'merchant_id': {'read_only': True, 'required': False},
            'bank': {'read_only': True, 'required': False},
            'agent_id': {'read_only': True, 'required': False},
            'order_id': {'read_only': True, 'required': False},
            'oxp_id': {'read_only': True, 'required': False},
            'txn_id': {'read_only': True, 'required': False},
            'sent_amount': {'read_only': True, 'required': False},
            'sent_currency': {'read_only': True, 'required': False},
            'sender_account': {'read_only': True, 'required': False},
            'agent_commission': {'read_only': True, 'required': False},
            'merchant_commission': {'read_only': True, 'required': False},
            'status': {'read_only': True, 'required': False},
        }

    def create(self, validated_data):
        try:
            # Extract necessary fields from validated_data
            this_request = self.context.get('request')
            if this_request:
                user = this_request.user
                merchant_id = MerchantProfile.objects.filter(user=user).first()
                bank_name = this_request.data.pop('bank_name', None)
                validated_data['merchant_id'] = merchant_id
            else:
                raise ValueError("Request object is missing in serializer context")

            customer_id = validated_data.get('customer_id')
            requested_amount = validated_data.get('requested_amount')
            requested_currency = validated_data.get('requested_currency')
            sender_account = validated_data.get('sender_account')

            # Add custom logic here if needed
            # Example: Set default values or perform calculations
            validated_data['oxp_id'] = generate_opx_id()  # Assume generate_txn_id() is a helper function
            validated_data['order_id'] = generate_order_id()  # Assume generate_order_id() is a helper function

            bank_type = BankTypeModel.objects.filter(name=bank_name, category='p2p').first()
            agent_bank = AgentBankModel.objects.filter(bank_type=bank_type)
            random_agent_bank = choice(agent_bank)
            agent = AgentProfile.objects.filter(id=random_agent_bank.agent.id).first()

            validated_data['bank'] = random_agent_bank
            validated_data['agent_id'] = agent
            validated_data['status'] = 'Assigned'

            # Create the Withdraw instance
            withdraw = Withdraw.objects.create(**validated_data)

            # Return the created Withdraw instance
            return withdraw
        except Exception as e:
            return None
