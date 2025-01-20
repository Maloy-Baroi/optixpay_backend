from random import choice

from PIL.ImageChops import difference
from django.db.models import Q
from pkg_resources import require
from requests import request
from requests.sessions import preferred_clock
from rest_framework import serializers, status

from app_bank.models.bank import BankTypeModel, AgentBankModel
from app_deposit.models.deposit import Currency
from app_profile.models.agent import AgentProfile
from app_profile.models.merchant import MerchantProfile
from app_withdraw.models.withdraw import Withdraw
from utils.common_response import CommonResponse
from utils.generate_order_id import generate_order_id
from utils.optixpay_id_generator import generate_opx_id
from utils.withdraw_commission_calculation import calculate_balances_for_withdraw


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
            'receiver_account',  # yes
            'agent_commission',
            'merchant_commission',
            'agent_amount_after_commission',
            'merchant_amount_after_commission',
            'agent_balance_should_be',
            'merchant_balance_should_be',
            'success_callbackurl',
            'failed_callbackurl',
            'cancel_callbackurl',
            'status'
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'merchant_id': {'required': False},
            'customer_id': {'required': False},
            'bank': {'required': False},
            'agent_id': {'required': False},
            'order_id': {'required': False},
            'oxp_id': {'required': False},
            'txn_id': {'required': False},
            'requested_amount': {'required': False},
            'requested_currency': {'required': False},
            'sent_amount': {'required': False},
            'sent_currency': {'required': False},
            'sender_account': {'required': False},
            'receiver_account': {'required': False},
            'agent_commission': {'required': False},
            'merchant_commission': {'required': False},
            'agent_amount_after_commission': {'required': False},
            'merchant_amount_after_commission': {'required': False},
            'success_callbackurl': {'required': False},
            'failed_callbackurl': {'required': False},
            'cancel_callbackurl': {'required': False},
            'status': {'required': False},
        }

    def create(self, validated_data):
        try:
            # Extract necessary fields from validated_data
            this_request = self.context.get('request')
            app_key = self.context.get('app_key')
            secret_key = self.context.get('secret_key')
            if this_request:
                preferred_currency = this_request.data.pop('preferred_currency', None)

                if not preferred_currency:
                    raise ValueError("Preferred Currency is required!")
                else:
                    preferred_currency_id = Currency.objects.filter(
                        Q(name__iexact=preferred_currency) | Q(currency_code__iexact=preferred_currency)
                    )
                    if preferred_currency_id.exists():
                        preferred_currency_id = preferred_currency_id.first()
                        validated_data['requested_currency'] = preferred_currency_id
                    else:
                        raise ValueError("Preferred Currency is missing in serializer context")

                merchant_id = MerchantProfile.objects.filter(app_key=app_key, secret_key=secret_key).first()
                if not merchant_id:
                    raise ValueError("Merchant is not Valid!")
                else:
                    # Filter merchant_wallets linked to this profile with the specified base currency
                    wallet = merchant_id.merchant_wallet.filter(wallet_base_currency=preferred_currency_id).first()
                    print(wallet)

                    # Calculate the total balance for all wallets with the base currency
                    total_balance = wallet.balance
                    merchant_withdraw_commission = wallet.withdraw_commission
                    requested_amount = float(validated_data['requested_amount'])

                    if (total_balance < requested_amount or total_balance - requested_amount <= 0) and (
                            merchant_id.is_negative_transaction_allowed == False):
                        raise ValueError(f"Contact to {merchant_id.name}. Info: Balance is going negative!")

                    validated_data['merchant_id'] = merchant_id
                bank_name = this_request.data.pop('bank_name', None)
            else:
                raise ValueError("Request object is missing in serializer context")

            # Add custom logic here if needed
            validated_data['oxp_id'] = generate_opx_id()  # Assume generate_txn_id() is a helper function
            # validated_data['order_id'] = generate_order_id()  # Assume generate_order_id() is a helper function

            bank_type = BankTypeModel.objects.filter(name=bank_name, category='p2p').first()
            agent_bank = AgentBankModel.objects.filter(bank_type=bank_type)
            random_agent_bank = choice(agent_bank)
            agent_balance = random_agent_bank.balance
            agent_withdraw_commission = random_agent_bank.withdraw_commission
            agent = AgentProfile.objects.filter(id=random_agent_bank.agent.id).first()

            validated_data['bank'] = random_agent_bank
            validated_data['sender_account'] = random_agent_bank.account_number
            validated_data['agent_id'] = agent
            validated_data['status'] = 'Assigned'
            validated_data['created_by'] = merchant_id.user
            validated_data['updated_by'] = merchant_id.user

            # Create the Withdraw instance
            withdraw = Withdraw(
                merchant_id=validated_data['merchant_id'],
                customer_id=validated_data['customer_id'],
                bank=validated_data['bank'],
                agent_id=validated_data['agent_id'],
                order_id=validated_data['order_id'],
                oxp_id=validated_data['oxp_id'],
                # txn_id=validated_data[''],
                requested_amount=validated_data['requested_amount'],
                requested_currency=validated_data['requested_currency'],
                # sent_amount=validated_data[''],
                # sent_currency=validated_data[''],
                sender_account=validated_data['sender_account'],
                receiver_account=validated_data['receiver_account'],
                agent_commission=agent_withdraw_commission,  # Default
                merchant_commission=merchant_withdraw_commission,  # Default
                status=validated_data['status'],  # Default
                success_callbackurl=validated_data['success_callbackurl'],
                failed_callbackurl=validated_data['failed_callbackurl'],
                cancel_callbackurl=validated_data['cancel_callbackurl'],
                is_active=True,
                created_by=validated_data['created_by'],
                updated_by=validated_data['updated_by'],
            )

            merchant_new_balance, agent_new_balance, merchant_commission_amount_n_balance, agent_commission_amount_n_balance = calculate_balances_for_withdraw(requested_amount=requested_amount,
                                                                                      merchant_balance=wallet.balance,
                                                                                      agent_balance=agent_balance,
                                                                                      merchant_commission=merchant_withdraw_commission,
                                                                                      agent_commission=agent_withdraw_commission)

            wallet.balance = merchant_new_balance
            wallet.save()

            withdraw.agent_balance_should_be = agent_new_balance
            withdraw.merchant_balance_should_be = merchant_new_balance
            withdraw.agent_amount_after_commission = agent_commission_amount_n_balance
            withdraw.merchant_amount_after_commission = merchant_commission_amount_n_balance
            withdraw.save()

            # random_agent_bank.balance = agent_new_balance
            # random_agent_bank.save()
            return withdraw
        except Exception as e:
            raise ValueError(str(e))


class WithdrawUpdateSerializer(serializers.ModelSerializer):
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
            'agent_balance_should_be',
            'merchant_balance_should_be',
            'agent_amount_after_commission',
            'merchant_amount_after_commission',
            'success_callbackurl',
            'failed_callbackurl',
            'cancel_callbackurl',
            'status'
        ]

    merchant_id = serializers.PrimaryKeyRelatedField(read_only=True)
    bank = serializers.PrimaryKeyRelatedField(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    requested_currency = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    sent_currency = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    status = serializers.ChoiceField(choices=Withdraw.status_choices)
    txn_id = serializers.CharField(required=True)

    def validate_customer_id(self, value):
        if not value:
            raise serializers.ValidationError("Customer ID must be provided.")
        return value

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if not request:
            raise serializers.ValidationError("Request context is required.")

        user = request.user

        # Check if user is an agent
        if user.groups.filter(name='agent').exists():
            # Agents can only update txn_id and status
            allowed_fields = ['txn_id', 'status', 'updated_by']
            for field in validated_data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError(f"Agents are not allowed to update {field}.")
            instance.status = validated_data.get('status', instance.status)


            if validated_data.get('status') and validated_data.get('status') == 'Successful':
                instance.txn_id = validated_data.get('transaction_id', instance.txn_id)

                agent_balance = instance.agent_balance_should_be
                withdraw_agent_bank = instance.bank
                agent_bank = AgentBankModel.objects.get(id=withdraw_agent_bank.id)
                agent_bank.balance = agent_balance
                agent_bank.save()

                instance.save()
            else:
                merchant_id = MerchantProfile.objects.get(id=instance.merchant_id.id)
                preferred_currency_id = instance.requested_currency
                wallet = merchant_id.merchant_wallet.filter(wallet_base_currency=preferred_currency_id).first()
                wallet.balance += instance.merchant_amount_after_commission
                wallet.save()

                instance.save()

        # If user is admin, allow updating all fields
        elif user.groups.filter(name='admin').exists():
            for field, value in validated_data.items():
                setattr(instance, field, value)
            instance.save()
        else:
            raise serializers.ValidationError("You do not have permission to update this record.")

        return instance

