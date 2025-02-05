from random import choice

from rest_framework import serializers

from app_bank.models.bank import AgentBankModel, BankTypeModel
from app_bank.serializers.bank import BankModelSerializer
from app_deposit.models.deposit import Deposit, Currency
from app_deposit.serializers.currency import CurrencySerializer
from app_profile.models.merchant import MerchantProfile
from utils.decrypt_payment_data import decrypt_payment_data
from utils.encrypt_deposit_p2p_data import encrypt_deposit_p2p_data
from utils.optixpay_id_generator import generate_opx_id


class DepositListSerializer(serializers.ModelSerializer):
    # merchant = ProfileSerializer(source='merchant_id', read_only=True)
    # bank = BankModelSerializer(read_only=True)
    # agent = ProfileSerializer(source='agent_id', read_only=True)
    # sending_currency = CurrencySerializer(read_only=True)
    # sent_currency = CurrencySerializer(read_only=True)
    merchant_unique_id = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()
    agent_unique_id = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    sending_currency_name = serializers.SerializerMethodField()
    received_currency_name = serializers.SerializerMethodField()

    class Meta:
        model = Deposit
        fields = [
            'id',
            'merchant_unique_id',
            'merchant_name',
            'customer_id',
            'bank',
            'bank_name',
            'agent_unique_id',
            'agent_name',
            'order_id',
            'oxp_id',
            'txn_id',
            'sending_amount',
            'sending_currency',
            'sending_currency_name',
            'actual_received_amount',
            'received_currency',
            'received_currency_name',
            'created_on',
            'last_updated',
            'sender_account',
            'receiver_account',
            'agent_commission',
            'merchant_commission',
            'status'
        ]

    def get_merchant_unique_id(self, obj):
        return obj.merchant_id.unique_id if obj.merchant_id else ""

    def get_merchant_name(self, obj):
        return obj.merchant_id.name if obj.merchant_id.name else ""

    def get_bank_name(self, obj):
        return obj.bank.bank_name if obj.bank.bank_name else ""

    def get_agent_unique_id(self, obj):
        return obj.agent_id.unique_id if obj.agent_id else ""

    def get_agent_name(self, obj):
        return obj.agent_id.name if obj.agent_id.name else ""

    def get_sending_currency_name(self, obj):
        return obj.sending_currency.currency_code if obj.sending_currency.currency_code else ""

    def get_received_currency_name(self, obj):
        return obj.received_currency.currency_code if obj.received_currency.currency_code else ""


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"

        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


class DepositCreateSerializer(serializers.ModelSerializer):
    optixpay_component = serializers.CharField(max_length=1000, write_only=True)
    unique_id = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Deposit
        fields = [
            'merchant_id',  # done
            'customer_id',  # done
            'bank',  # done
            'agent_id',  # done
            'order_id',  # done
            'oxp_id',  # done
            'txn_id',
            'sending_amount',  # done
            'sending_currency',  # done
            'actual_received_amount',
            'received_currency',
            'created_on',  # auto
            'last_updated',  # auto
            'sender_account',
            'receiver_account',  # done
            'agent_commission',  # done
            'merchant_commission',
            'status',  # done
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            "optixpay_component",
            "unique_id",
            'call_back_url'
        ]

        extra_kwargs = {
            'merchant_id': {'required': False},
            'customer_id': {'required': False},  # merchant dibe encrypt kore
            # 'bank_name': {'required': True}, # merchant dibe encrypt kore
            'bank': {'required': False},
            'agent_id': {'required': False},
            'order_id': {'required': False},  # merchant dibe encrypt kore
            'oxp_id': {'required': False},
            'txn_id': {'required': False},
            'sending_amount': {'required': False},  # merchant dibe encrypt kore
            'sending_currency': {'required': False},  # merchant dibe encrypt kore
            'actual_received_amount': {'required': False},
            'received_currency': {'required': False},
            'created_on': {'required': False},
            'last_updated': {'required': False},
            'sender_account': {'required': False},
            'receiver_account': {'required': False},
            'agent_commission': {'required': False},
            'merchant_commission': {'required': False},
            'call_back_url': {'required': False},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'optixpay_component': {'write_only': True},
            'unique_id': {'write_only': True},
        }


class DepositExternalCreateSerializer(serializers.ModelSerializer):
    optixpay_component = serializers.CharField(max_length=1000, write_only=True)
    unique_id = serializers.CharField(max_length=255, write_only=True)
    encrypted_data = serializers.CharField(max_length=1000, read_only=True)
    agent_number = serializers.CharField(max_length=25, read_only=True)

    class Meta:
        model = Deposit
        fields = [
            "optixpay_component",
            "unique_id",
            "encrypted_data",
            "agent_number",
        ]

    def create(self, validated_data):
        try:
            print("deposit starts")
            deposit_dictionary = {}
            optixpay_component = validated_data.get('optixpay_component')
            unique_id = validated_data.get('unique_id')

            if not unique_id:
                raise ValueError("Merchant is not Valid!")

            merchant = MerchantProfile.objects.filter(unique_id=unique_id).first()
            if not merchant:
                raise ValueError("Merchant is not Valid!")
            merchant_app_key = merchant.app_key
            merchant_secret_key = merchant.secret_key
            payment_data = decrypt_payment_data(optixpay_component, merchant_app_key, merchant_secret_key)
            # """
            #     Decrypted Data in dictionary:
            #     {'customer_id': '14ejsn', 'order_id': '213enjdsfn', 'bank_name': 'bkash', 'sending_amount': 1000, 'sending_currency': 'BDT', "call_back_url": "hhtps://"}
            # """

            order_id = payment_data.get('order_id', None)
            customer_id = payment_data.get('customer_id', None)
            bank_name = payment_data.get('bank_name', None)
            sending_amount = payment_data.get('sending_amount', None)
            sending_currency = payment_data.get('sending_currency', None)
            call_back_url = payment_data.get('call_back_url', None)

            if not (order_id and customer_id and bank_name and sending_amount and sending_currency and call_back_url):
                raise ValueError("Encryption Error!")

            sending_currency_obj = Currency.objects.filter(currency_code__iexact=sending_currency)
            if not sending_currency_obj.exists():
                raise ValueError("Sending currency is not Valid!")
            # bank_type = BankTypeModel.objects.filter(name__iexact=bank_name, category='p2p').first()

            agent_bank = AgentBankModel.objects.filter(bank_type__name__iexact=bank_name, bank_type__category__iexact='p2p')

            take_bank = []
            for bank in agent_bank:
                negative_balance_possible = bank.agent.is_negative_transaction_allowed
                bank_balance = bank.balance
                bank_deposit_commission = bank.deposit_commission
                with_commission_balance = float(float(sending_amount) * float(bank_deposit_commission)) / 100.0 + float(
                    sending_amount)
                if with_commission_balance > bank_balance and negative_balance_possible:
                    continue
                take_bank.append(bank)

            if len(take_bank) == 0:
                raise ValueError("No Bank Found for this amount of money!")

            random_agent_bank = choice(take_bank)

            deposit_dictionary['order_id'] = order_id
            deposit_dictionary['customer_id'] = customer_id
            deposit_dictionary['bank'] = random_agent_bank
            deposit_dictionary['sending_amount'] = sending_amount
            deposit_dictionary['sending_currency'] = sending_currency_obj.first()
            deposit_dictionary['oxp_id'] = generate_opx_id()
            deposit_dictionary['agent_id'] = random_agent_bank.agent
            deposit_dictionary['receiver_account'] = random_agent_bank.account_number
            deposit_dictionary['received_currency'] = random_agent_bank.bank_type.currency
            deposit_dictionary['merchant_id'] = merchant
            deposit_dictionary['txn_id'] = None

            bank_balance = random_agent_bank.balance
            bank_deposit_commission = random_agent_bank.deposit_commission
            agent_commission_amount = float(float(sending_amount) * float(bank_deposit_commission)) / 100.0
            deposit_dictionary['agent_commission'] = agent_commission_amount
            deposit_dictionary['call_back_url'] = call_back_url
            deposit_dictionary['status'] = "processing"

            deposit = Deposit(
                **deposit_dictionary,
                created_by=merchant.user,
                updated_by=merchant.user,
                is_active=True
            )
            deposit.save()

            deposit_serializers = DepositSerializer(deposit)

            encrypted_data = encrypt_deposit_p2p_data(deposit_serializers.data)
            response_data = {
                'encrypted_data': encrypted_data,
                'agent_number': random_agent_bank.account_number
            }
            return response_data
        except Exception as e:
            print("Exception Error", str(e))
            return None


class DepositPutRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = [
            'txn_id',
            'call_back_url'
        ]


class DepositInternalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = [
            'merchant_id', 'customer_id', 'bank', 'agent_id',
            'order_id', 'oxp_id', 'txn_id', 'sending_amount',
            'sending_currency', 'actual_received_amount', 'received_currency',
            'created_on', 'last_updated', 'sender_account', 'receiver_account',
            'agent_commission', 'merchant_commission', 'status', 'call_back_url'
        ]
        read_only_fields = ['merchant_id', 'agent_id', 'bank', 'oxp_id', 'txn_id', 'actual_received_amount',
                            'agent_commission', 'received_currency', 'created_on', 'last_updated']

    def create(self, validated_data):
        # Automatically generate UUID for oxp_id and txn_id if not provided
        validated_data['oxp_id'] = generate_opx_id()
        merchant_id = self.context.get('merchant_id')
        agent_phone_number = validated_data.get('receiver_account')
        agent_bank = AgentBankModel.objects.get(account_number=agent_phone_number)
        agent_id = agent_bank.agent
        deposit_commission = agent_bank.deposit_commission
        validated_data['merchant_id'] = merchant_id
        validated_data['bank'] = agent_bank
        validated_data['agent_id'] = agent_id
        validated_data['actual_received_amount'] = validated_data['sending_amount']
        validated_data['received_currency'] = validated_data['sending_currency']
        validated_data['agent_commission'] = deposit_commission
        return super().create(validated_data)

class DepositWebhookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = [
            'customer_id',
            'order_id',
            'oxp_id',
            'txn_id',
            'sending_amount',
            'sending_currency',
        ]


