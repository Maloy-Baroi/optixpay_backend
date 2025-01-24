from random import choice

from rest_framework import serializers

from app_bank.models.bank import AgentBankModel, BankTypeModel
from app_bank.serializers.bank import BankModelSerializer
from app_deposit.models.deposit import Deposit, Currency
from app_deposit.serializers.currency import CurrencySerializer
from app_profile.models.merchant import MerchantProfile
from app_profile.models.profile import Profile
from app_profile.serializers.profile import ProfileSerializer
from utils.decrypt_deposit_p2p_data import decrypt_deposit_p2p_data
from utils.decrypt_payment_data import decrypt_payment_data
from utils.optixpay_id_generator import generate_opx_id


class DepositListSerializer(serializers.ModelSerializer):
    merchant = ProfileSerializer(source='merchant_id', read_only=True)
    bank = BankModelSerializer(read_only=True)
    agent = ProfileSerializer(source='agent_id', read_only=True)
    sending_currency = CurrencySerializer(read_only=True)
    sent_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Deposit
        fields = [
            'merchant', 'customer_id', 'bank', 'agent', 'order_id',
            'oxp_id', 'txn_id', 'sending_amount', 'sending_currency',
            'actual_received_amount', 'received_currency', 'created_on', 'last_updated',
            'sender_account', 'receiver_account', 'agent_commission',
            'merchant_commission', 'status'
        ]


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
            'merchant_id', # done
            'customer_id', # done
            'bank', # done
            'agent_id', # done
            'order_id', # done
            'oxp_id', # done
            'txn_id',
            'sending_amount', # done
            'sending_currency', # done
            'actual_received_amount',
            'received_currency',
            'created_on', # auto
            'last_updated', # auto
            'sender_account',
            'receiver_account', # done
            'agent_commission', # done
            'merchant_commission',
            'status', # done
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
            'customer_id': {'required': False}, # merchant dibe encrypt kore
            # 'bank_name': {'required': True}, # merchant dibe encrypt kore
            'bank': {'required': False},
            'agent_id': {'required': False},
            'order_id': {'required': False}, # merchant dibe encrypt kore
            'oxp_id': {'required': False},
            'txn_id': {'required': False},
            'sending_amount': {'required': False}, # merchant dibe encrypt kore
            'sending_currency': {'required': False}, # merchant dibe encrypt kore
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
    class Meta:
        model = Deposit
        fields = [
            "optixpay_component",
            "unique_id"
        ]

    def create(self, validated_data):
        try:
            deposit_dictionary = {}
            encrypted_data = validated_data.get('optixpay_component')
            unique_id = validated_data.get('unique_id')

            print("Encrypted data: ", encrypted_data, "\nUnique ID: ", unique_id)

            if not unique_id:
                raise ValueError("Merchant is not Valid!")

            merchant = MerchantProfile.objects.filter(unique_id=unique_id)
            if not merchant.exists():
                raise ValueError("Merchant is not Valid!")
            merchant_app_key = merchant.first().app_key
            merchant_secret_key = merchant.first().secret_key
            payment_data = decrypt_payment_data(encrypted_data, merchant_app_key, merchant_secret_key)
            # """
            #     Decrypted Data in dictionary:
            #     {'customer_id': '14ejsn', 'order_id': '213enjdsfn', 'bank_name': 'bkash', 'sending_amount': 1000, 'sending_currency': 'BDT', "call_back_url": "hhtps://"}
            # """

            order_id = payment_data.get('order_id')
            customer_id = payment_data.get('customer_id')
            bank_name = payment_data.get('bank_name')
            sending_amount = payment_data.get('sending_amount')
            sending_currency = payment_data.get('sending_currency')
            call_back_url = payment_data.get('call_back_url')

            if not (order_id and customer_id and bank_name and sending_amount and sending_currency and call_back_url):
                raise ValueError("Encryption Error!")

            sending_currency_obj = Currency.objects.filter(currency_code__iexact=sending_currency)
            if not sending_currency_obj.exists():
                raise ValueError("Sending currency is not Valid!")
            bank_type = BankTypeModel.objects.filter(name__iexact=bank_name, category='p2p').first()
            agent_bank = AgentBankModel.objects.filter(bank_type=bank_type, usage_for='deposit')

            take_bank = []
            for bank in agent_bank:
                negative_balance_possible = bank.agent.is_negative_transaction_allowed
                bank_balance = bank.balance
                bank_deposit_commission = bank.deposit_commission
                with_commission_balance = float(float(sending_amount) * float(bank_deposit_commission)) / 100.0 + float(
                    sending_amount)
                print("Amount with commission: ", with_commission_balance)
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
            deposit_dictionary['merchant_id'] = merchant.first()

            bank_balance = random_agent_bank.balance
            bank_deposit_commission = random_agent_bank.deposit_commission
            agent_commission_amount = float(float(sending_amount) * float(bank_deposit_commission)) / 100.0
            deposit_dictionary['agent_commission'] = agent_commission_amount
            deposit_dictionary['call_back_url'] = call_back_url
            deposit_dictionary['status'] = "processing"

            deposit = Deposit(
                **deposit_dictionary,
                created_by=merchant.first().user,
                updated_by=merchant.first().user
            )
            deposit.save()

            return deposit
        except Exception as e:
            print("Error: ", e)
            return None



class DepositPutRequestSerializer(serializers.ModelSerializer):
    encrypted_data = serializers.CharField(write_only=True)
    merchant_unique_id = serializers.CharField(write_only=True)
    class Meta:
        model = Deposit
        fields = [
            'encrypted_data',
            'txn_id',
            'merchant_unique_id'
        ]

    def update(self, instance, validated_data):
        encrypted_data = validated_data.pop('encrypted_data')
        merchant_unique_id = validated_data.pop('merchant_unique_id')
        txn_id = validated_data.pop('txn_id')

        decrypted_data = decrypt_deposit_p2p_data(encrypted_data, merchant_unique_id)
        oxp_id = decrypted_data['oxp_id']
        merchant_id = decrypted_data['merchant_id']
        order_id = decrypted_data['order_id']
        deposit = Deposit.objects.filter(oxp_id=oxp_id, merchant_id=merchant_id, order_id=order_id)
        if not deposit.exists():
            raise ValueError("Deposit not found!")
        deposit = deposit.first()
        deposit.txn_id = txn_id
        deposit.save()

        return deposit



