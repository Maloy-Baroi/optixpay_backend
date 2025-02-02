from locale import currency
from random import choice

from PIL.ImageChops import difference
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers, status
from app_bank.models.bank import BankTypeModel, AgentBankModel
from app_deposit.models.deposit import Currency
from app_profile.models.agent import AgentProfile
from app_profile.models.merchant import MerchantProfile
from app_profile.models.wallet import CurrencyConversion
from app_sms.models.sms import SMSManagement
from app_withdraw.models.withdraw import Withdraw
from core.models.InValidTransactionId import InvalidTransactionId
from utils.optixpay_id_generator import generate_opx_id
from utils.withdraw_commission_calculation import calculate_balances_for_withdraw
from utils.withdraw_verify_by_sms import verify_by_sms


class WithdrawListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = [
            "merchant_unique_id",
            "merchant_name",
            "customer_id",
            "bank",
            "bank_name",
            "agent_id",
            "agent_name",
            "order_id",
            "oxp_id",
            "txn_id",
            "requested_amount",
            "requested_currency",
            "requested_currency_name",
            "sent_amount",
            "sent_currency",
            "sent_currency_name",
            "sent_currency_name",
            "sender_account",
            "receiver_account",
            "agent_commission",
            "merchant_commission",
            "agent_amount_after_commission",
            "merchant_amount_after_commission",
            "agent_balance_should_be",
            "merchant_balance_should_be",
            "status",
        ]

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
    status = serializers.ChoiceField(choices=Withdraw.STATUS_CHOICES)

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
            # bank_name = self.context.get('bank_name')
            if this_request:
                preferred_currency = this_request.data.pop('preferred_currency', None)
                bank_name = this_request.data.pop('bank_name', None)

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
                    filtered_wallet = merchant_id.merchant_wallet.filter(wallet_base_currency=preferred_currency_id)
                    wallets = []
                    for wal in filtered_wallet:
                        if wal.bank.name.lower() == bank_name.lower():
                            wallets.append(wal)

                    wallet = choice(wallets)

                    # Calculate the total balance for all wallets with the base currency
                    total_balance = 0
                    converted_requested_amount = 0.00
                    requested_amount = float(validated_data['requested_amount'])
                    try:
                        wallet_currency_code = wallet.wallet_base_currency.currency_code
                        wallet_currency_name = wallet.wallet_base_currency.name

                        if not (wallet_currency_code == preferred_currency_id.currency_code or wallet_currency_name == preferred_currency_id.name):
                            currency_rate = CurrencyConversion.objects.filter(
                                (
                                        Q(base_currency__currency_code=preferred_currency_id.currency_code,
                                          to_currency__currency_code=wallet_currency_code)
                                ) & Q(merchant_wallet=wallet)
                            )
                            if not currency_rate.exists():
                                raise ValueError("Currency rate is not valid!")

                            currency_rate = currency_rate.first()

                            converted_amount = float(requested_amount) * float(currency_rate.conversion_rate)
                        else:
                            converted_amount = requested_amount
                        total_balance = wallet.balance
                    except Exception as e:
                        raise ValueError(f"Error Merchant: {str(e)}")
                    merchant_withdraw_commission = wallet.withdraw_commission

                    if (total_balance < converted_amount or total_balance - converted_amount <= 0) and (
                            merchant_id.is_negative_transaction_allowed == False):
                        raise ValueError(f"Contact to {merchant_id.name}. Info: Balance is going negative!")

                    validated_data['merchant_id'] = merchant_id
            else:
                raise ValueError("Request object is missing in serializer context")

            # Add custom logic here if needed
            validated_data['oxp_id'] = generate_opx_id()  # Assume generate_txn_id() is a helper function
            # validated_data['order_id'] = generate_order_id()  # Assume generate_order_id() is a helper function

            bank_type = BankTypeModel.objects.filter(name__iexact=bank_name, category='p2p').first()
            agent_bank = AgentBankModel.objects.filter(bank_type=bank_type, usage_for='withdraw')
            random_agent_bank = choice(agent_bank)
            try:
                agent_balance = random_agent_bank.balance
            except Exception as e:
                raise ValueError(f"Agent Bank: {str(e)}")
            agent_withdraw_commission = random_agent_bank.withdraw_commission
            agent = AgentProfile.objects.filter(id=random_agent_bank.agent.id).first()

            validated_data['bank'] = random_agent_bank
            validated_data['sender_account'] = random_agent_bank.account_number
            validated_data['agent_id'] = agent
            validated_data['status'] = 'Assigned'
            validated_data['created_by'] = merchant_id.user
            validated_data['updated_by'] = merchant_id.user

            print("Before withdraw")

            # Create the Withdraw instance
            withdraw = Withdraw.objects.create(
                merchant_id=validated_data['merchant_id'],
                customer_id=validated_data['customer_id'],
                bank=validated_data['bank'],
                agent_id=validated_data['agent_id'],
                order_id=validated_data['order_id'],
                oxp_id=validated_data['oxp_id'],
                # txn_id=validated_data[''],
                requested_amount=validated_data['requested_amount'],
                converted_amount=converted_amount,
                requested_currency=validated_data['requested_currency'],
                # sent_amount=validated_data[''],
                # sent_currency=validated_data[''],
                sender_account=validated_data['sender_account'],
                receiver_account=validated_data['receiver_account'],
                agent_commission=agent_withdraw_commission,  # Default
                merchant_commission=merchant_withdraw_commission,  # Default
                status=validated_data['status'],  # Default
                success_callbackurl="",
                failed_callbackurl="",
                cancel_callbackurl="",
                is_active=True,
                created_by=validated_data['created_by'],
                updated_by=validated_data['updated_by'],
            )

            print('Withdraw created')

            merchant_new_balance, agent_new_balance, merchant_commission_amount_n_balance, agent_commission_amount_n_balance = calculate_balances_for_withdraw(
                requested_amount=converted_amount,
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
            print("Withdraw: ", withdraw)

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
            'converted_amount',
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
    status = serializers.ChoiceField(choices=Withdraw.STATUS_CHOICES)
    txn_id = serializers.CharField(required=True)

    # def validate_customer_id(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Customer ID must be provided.")
    #     return value

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if not request:
            raise serializers.ValidationError({"status": "error", "data": {},
                                               "message": "Request context is required."})

        user = request.user

        # Check if user is an agent
        if user.groups.filter(name='agent').exists():
            # Agents can only update txn_id and status
            allowed_fields = ['txn_id', 'status', 'updated_by']
            for field in validated_data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError(f"Agents are not allowed to update {field}.")
            instance.status = validated_data.get('status', instance.status)

            if validated_data.get('status') and validated_data.get('status') == 'successful':
                instance.txn_id = validated_data.get('txn_id', instance.txn_id)
                withdraw_sender_account = instance.sender_account
                withdraw_requested_amount = instance.requested_amount
                withdraw_verify, sms = verify_by_sms(amount=withdraw_requested_amount, txn_id=instance.txn_id,
                                                account=withdraw_sender_account)

                # without amount check from sms
                # withdraw_verify = verify_by_sms(amount=withdraw_requested_amount, txn_id=instance.txn_id)

                if not withdraw_verify:
                    raise serializers.ValidationError({"status": "error", "data": {},
                                                       "message": "Transaction verification failed. Please contact to the administrator."})

                # without amount check from sms
                # if amount != instance.converted_amount:
                #     new_converted_amount = instance

                agent_balance = instance.agent_balance_should_be
                withdraw_agent_bank = instance.bank
                agent_bank = AgentBankModel.objects.get(id=withdraw_agent_bank.id)
                agent_bank.balance = agent_balance

                instance.sent_currency = agent_bank.bank_type.currency
                instance.sent_amount = instance.requested_amount

                sms = SMSManagement.objects.get(txn_id=instance.txn_id)
                sms.status = 'claimed'

                invalid_txn_id = InvalidTransactionId(txn_id=instance.txn_id)

                try:
                    with transaction.atomic():
                        instance.save()
                        agent_bank.save()
                        sms.save()
                        invalid_txn_id.save()
                except Exception as e:
                    # Optionally, re-raise the exception if you want to propagate it
                    raise serializers.ValidationError({"status": "error", "data": {},
                                                       "message": "An error occurred: {str(e)}"})

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
            raise serializers.ValidationError({"status": "error", "data": {},
                                               "message": "You do not have permission to update this record."})

        return instance
