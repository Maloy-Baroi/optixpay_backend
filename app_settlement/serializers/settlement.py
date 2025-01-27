from locale import currency

from rest_framework import serializers
from app_profile.models.merchant import MerchantProfile  # Import the model if it's in a separate file
from app_deposit.models.deposit import Currency  # Make sure the import is correct
from app_profile.models.wallet import MerchantWallet
from app_settlement.models.settlement import Settlement
from utils.optixpay_id_generator import generate_settlement_id
from utils.unique_default import get_unique_default


class SettlementListSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant_id.name', read_only=True)
    merchant_unique_id = serializers.CharField(source='merchant_id.unique_id', read_only=True)
    currency_code = serializers.CharField(source='currency.currency_code', read_only=True)

    class Meta:
        model = Settlement
        fields = ['id', 'settlement_id', 'merchant_unique_id', 'merchant_name', 'currency', 'currency_code', 'amount', 'commission_percentage',
                  'amount_after_commission', 'txn_id', 'usdt_address', 'status', 'created_at', 'updated_at']


class SettlementCreateSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(queryset=MerchantWallet.objects.all())

    class Meta:
        model = Settlement
        fields = [
            'id',
            'wallet',
            'amount',
            'usdt_address',
        ]

    def validate_wallet(self, value):
        if not isinstance(value, MerchantWallet):
            raise serializers.ValidationError("Wallet must be a valid MerchantWallet ID.")
        return value

    def validate(self, data):
        """
        Check that the necessary fields are not only present but also valid.
        """
        if 'wallet' not in data or 'amount' not in data or 'usdt_address' not in data:
            raise serializers.ValidationError("All fields must be provided: wallet, amount, usdt_address.")
        return data

    def create(self, validated_data):
        amount = validated_data.get('amount', None)
        usdt_address = validated_data.get('usdt_address', None)
        wallet = validated_data.get('wallet', None)

        merchant_id = self.context.get('merchant_id', None)
        settlement_id = generate_settlement_id()
        # wallet_obj = MerchantWallet.objects.get(id=wallet)

        if wallet is None or amount is None or usdt_address is None:
            raise serializers.ValidationError("Value Missing!")

        amount_after_commission = float(amount) + (float(amount) * float(wallet.settlement_commission)/100)
        if wallet.balance < amount_after_commission:
            raise ValueError(f"Invalid Amount! Your requesting amount is {amount}. Couldn't adjust with the commission.")

        wallet.balance = wallet.balance - amount_after_commission
        wallet.save()

        settlement = Settlement(
            settlement_id = settlement_id,
            merchant_id = merchant_id,
            wallet = wallet,
            currency = wallet.wallet_base_currency,
            amount = amount,
            commission_percentage = wallet.settlement_commission,
            amount_after_commission = amount_after_commission,
            txn_id = get_unique_default(),
            usdt_address = usdt_address,
            status = "pending"
        )

        settlement.save()
        return settlement


class SettlementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = [
            'exchange_rate',
            'txn_id',
            'status',
        #     Read only fields

        ]

    def update(self, instance, validated_data):
        exchange_rate = validated_data.get('exchange_rate', None)
        txn_id = validated_data.get('txn_id', None)
        status = validated_data.get('status', None)

        if exchange_rate is None:
            raise ValueError("Exchange Rate is missing!")
        if txn_id is None:
            raise ValueError("Transaction ID is missing!")
        if status is None:
            raise ValueError("Status is missing!")

        if status == "failed":
            instance.wallet.balance = instance.wallet.balance + instance.amount_after_commission
            instance.wallet.save()
        elif status == "pending":
            return ValueError("Transaction is still pending.")
        else:
            amount = instance.amount
            amount_in_usd = float(amount) / float(exchange_rate)
            instance.usdt_address = amount_in_usd
            instance.exchange_rate = exchange_rate
            instance.txn_id = txn_id
            instance.status = status
            instance.save()
            return instance
