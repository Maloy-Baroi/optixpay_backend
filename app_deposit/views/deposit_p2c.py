import json
import random
from locale import currency

import requests
from django.conf import settings
from requests import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from app_bank.models.bank import BankTypeModel, AgentBankModel
from app_deposit.models.deposit import Deposit, Currency
from app_profile.models.agent import AgentProfile
from app_profile.models.merchant import MerchantProfile
from utils.common_response import CommonResponse
from utils.invoice_generate import generate_invoice_number
from utils.optixpay_id_generator import generate_opx_id
from utils.unique_default import get_unique_default
from utils.withdraw_commission_calculation import calculate_balances_for_deposit


class VerifyMerchantView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    queryset = MerchantProfile.objects.all()

    def post(self, request):
        try:
            unique_id = request.data.get('unique_id')
            # optixpay_component = request.data.get('optixpay_component')
            payment_method = request.data.get('payment_method')
            order_id = request.data.get('order_id', None)
            custom_id = request.data.get('custom_id', None)
            print("Bank category: ", payment_method)
            merchant = MerchantProfile.objects.filter(unique_id=unique_id).first()
            customer_id = request.data.get('customer_id', None)
            callbackurl = request.data.get('callbackurl', None)

            # special work starts
            # Special work ends

            if not merchant:
                print("Merchant not found", unique_id)
                return CommonResponse('error', {}, status.HTTP_400_BAD_REQUEST, "Merchant not found!")
            # okay

            if merchant:
                print(f"Merchant found: {merchant}\n")
                # Fetch a payment aggregator agent that supports the provided payment_method (provider)
                # selected_agent_ids = BankTypeModel.objects.filter(
                #     category__iexact=payment_method
                # ).values_list('id', flat=True)
                try:
                    bank_type = BankTypeModel.objects.filter(name__iexact=payment_method, category__iexact='p2c').first()
                    print(f"Bank type: {bank_type}\n")
                    if not bank_type:
                        return CommonResponse('error', {}, status.HTTP_400_BAD_REQUEST, "Bank type not found!")
                    select_agent_bank_ids = AgentBankModel.objects.filter(
                        usage_for__iexact='deposit',
                        bank_type__name__iexact=payment_method,
                        bank_type__category__iexact='p2c',
                    ).values_list('id', flat=True)

                    print("Selected agent bank: ", select_agent_bank_ids)

                    selected_bank_id = random.choice(select_agent_bank_ids)

                    print("Selected bank id: ", selected_bank_id)

                    selected_bank_obj = AgentBankModel.objects.get(id=selected_bank_id)
                    print("Select Bank obj", selected_bank_obj)
                    selected_agent = selected_bank_obj.agent
                    print("Selected agent: ", selected_agent)
                    agent_bank_app_key = selected_bank_obj.app_key
                    print("Selected app key: ", agent_bank_app_key)
                    agent_bank_secret_key = selected_bank_obj.secret_key
                    print("Selected secret key: ", agent_bank_secret_key)
                    agent_bank_unique_id = selected_bank_obj.id
                    print("Selected unique id: ", agent_bank_unique_id)
                    agent_bank_phone_number = selected_bank_obj.master_username
                    print("Selected bank phone number: ", agent_bank_phone_number)
                    agent_bank_password = selected_bank_obj.master_password
                    print("Bank Password: ", agent_bank_password)
                except Exception as e:
                    return CommonResponse('error', {}, status.HTTP_400_BAD_REQUEST, str(e))

                if selected_agent is not None:
                    print("Maloy Baroi")
                    # Return a response with the provider name and agent data, without exposing sensitive keys
                    # provider_key =
                    agent_data = {
                        'id': selected_agent.id,
                        'agent_name': selected_agent.name,
                        'bank_unique_id': agent_bank_unique_id,
                        # 'provider_key': agent_bank_app_key if agent_bank_app_key else "",
                        # 'provider_secret': agent_bank_secret_key if agent_bank_secret_key else "",
                        'provider_phone_number': agent_bank_phone_number,
                        'provider_password': agent_bank_password,
                    }

                    print("Agent Data: Maloy ", agent_data)
                    agent_profile = AgentProfile.objects.filter(id=selected_bank_obj.agent_id)
                    if agent_profile.exists():
                        agent_profile = agent_profile.first()

                    currency = Currency.objects.filter(currency_code="BDT")
                    if currency.exists():
                        currency = currency.first()

                    deposit = Deposit(
                        merchant_id=merchant,
                        customer_id=customer_id if customer_id else f"customer{random.randint(100000, 9999999999999)}",
                        bank=selected_bank_obj,
                        agent_id=agent_profile,
                        order_id= order_id if order_id else f"order{random.randint(100000, 9999999999999)}",
                        oxp_id=generate_opx_id(),
                        txn_id=get_unique_default(),
                        sending_amount=0,
                        sending_currency=currency,
                        actual_received_amount=0,
                        received_currency=currency,
                        sender_account=f"sender{random.randint(100000, 9999999999999)}",
                        receiver_account=selected_bank_obj.account_number,
                        agent_commission=0.0,
                        merchant_commission=0.0,
                        status="processing",
                        call_back_url= callbackurl if callbackurl else "http://google.com",
                    )

                    deposit.save()

                    if payment_method.lower() == 'bkash':
                        return CommonResponse("success", {
                            'message': 'Merchant is verified.',
                            'agent_data': agent_data,
                            'merchant_unique_id': merchant.unique_id,
                            'payment_obj': deposit.id,
                        }, status.HTTP_200_OK, "Merchant verified!")
                    elif payment_method.lower() == 'nagad':
                        return CommonResponse("success", {
                            'message': 'Merchant is verified.',
                            'agent_data': agent_data,
                            'merchant_unique_id': merchant.unique_id,
                            'orderId': f"order{random.randint(100000, 9999999999999)}",
                            'payment_obj': deposit.id,
                        }, status.HTTP_200_OK, "Merchant verified!")
                else:
                    return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                          f"No provider found for payment method: {payment_method}")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                      "Merchant is not found!")
        except MerchantProfile.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                  "Merchant is not found!")


class DepositBKashPayView(APIView):
    def post(self, request):
        try:
            print("_____________start__________")
            bank_unique_id = request.data.get('bank_unique_id', None)
            print("Bank unique id: ", bank_unique_id)
            merchant_unique_id = request.data.get('merchant_unique_id', None)
            print("Merchant unique id: ", merchant_unique_id)

            bank_obj = AgentBankModel.objects.filter(id=int(bank_unique_id)).first()
            print("Bank obj: ", bank_obj)
            merchant = MerchantProfile.objects.filter(unique_id=merchant_unique_id).first()
            print("Merchant obj: ", merchant)
            # if not merchant:
            #     return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
            #                           "Merchant is not found!")

            agent_bank_username = request.data.get('username', None)
            print("Agent Bank username: ", agent_bank_username)
            agent_bank_password = request.data.get('password', None)
            print("Agent Bank password: ", agent_bank_password)
            payment_amount = request.data.get('payment_amount', None)
            print("Payment amount: ", payment_amount)
            payment_method = request.data.get('payment_method', None)
            print("Payment method: ", payment_method)
            payment_currency = request.data.get('payment_currency', None)
            print("Payment currency: ", payment_currency)
            deposit_id = request.data.get('deposit_id', None)
            print("Deposit ID: ", deposit_id)

            # merchant_wallets = merchant.merchant_wallet.all()
            # print("Merchant wallets: ", merchant_wallets)
            # merchant_wallet = merchant_wallets.filter(bank=bank_obj.bank_type).first()
            # print("Merchant wallet: ", merchant_wallet)
            # merchant_commission = 5
            #
            # deposit = Deposit.objects.filter(id=int(deposit_id)).first()
            # print("deposit: ", deposit)
            # deposit.sending_amount = payment_amount
            # agent_bank = deposit.bank
            # agent_commission = 10.0
            # a,b,c,d = calculate_balances_for_deposit(
            #     requested_amount=payment_amount,
            #     merchant_balance=merchant_wallet.balance,
            #     agent_balance=agent_bank.balance,
            #     merchant_commission=merchant_commission,
            #     agent_commission=agent_commission
            # )
            # agent_amount_after_commission = a
            # merchant_amount_after_commission = b
            # agent_balance_should_be = c
            # merchant_balance_should_be = d
            # deposit.agent_amount_after_commission = agent_amount_after_commission
            # deposit.merchant_amount_after_commission = merchant_amount_after_commission
            # deposit.agent_balance_should_be = agent_balance_should_be
            # deposit.merchant_balance_should_be = merchant_balance_should_be
            # deposit.save()

            # Define the headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "username": agent_bank_username,
                "password": agent_bank_password
            }
            print("Headers: ", headers)

            # Define the body
            data = {
                "app_key": bank_obj.app_key,
                "app_secret": bank_obj.secret_key
            }
            print(f"Appkey: {bank_obj.app_key}, secret: {bank_obj.secret_key}")
            # Make the request to the external API using requests
            # response = requests.post(
            #     "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant",
            #     json=data,
            #     headers=headers
            # )
            # Make the request to the external API using requests
            response = requests.post(
                "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant",
                json=data,
                headers=headers
            )

            print("Response: ", response)
            print("Response status: ", response.status_code)
            print("Response json: ", response.json())

            # Check if the response is successful
            if str(response.status_code) == "200":
                response_json = response.json()
                response_json_dictionary = dict(response_json)
                id_token = response_json_dictionary.get('id_token')
                if id_token:
                    # sandbox = bkash_create_sandbox(
                    #     call_back_path="http://localhost:3000/",
                    #     amount=payment_amount,
                    #     currency=payment_currency,
                    #     invoice_number=invoice_number,
                    #     merchant_id=username,
                    #     id_token=id_token,
                    #     x_app_key=app_key,
                    #     username=username
                    # )

                    # create_payment = Payment(merchant=merchant,
                    #                          amount=int(payment_amount),
                    #                          currency=payment_currency,
                    #                          paymentMethod=payment_method,
                    #                          created_by=merchant.user,
                    #                          updated_by=merchant.user)
                    # create_payment.commission = (int(create_payment.amount) * settings.COMMISSION) / 100
                    # create_payment.after_commission = create_payment.amount - create_payment.commission
                    # create_payment.save()
                    # deposit = Deposit(
                    #     merchant_id=merchant,
                    #     customer_id="",
                    #     bank=bank_obj,
                    #     agent_id=bank_obj.agent_id,
                    #     order_id="",
                    #     oxp_id="",
                    #     txn_id="",
                    #     sending_amount=payment_amount,
                    #     sending_currency="",
                    #     actual_received_amount=payment_amount,
                    #     received_currency=payment_currency,
                    #     sender_account="",
                    #     receiver_account=bank_obj.account_number,
                    #     agent_commission=0.0,
                    #     merchant_commission=0.0,
                    #     status="processing",
                    #     call_back_url="",
                    # )

                    return CommonResponse("success", {"id_token": id_token, "payment_id": deposit_id}, status.HTTP_200_OK, "Success")

                    # return Response({"message": "Auth Token Found!", "data": {"id_token": id_token, "payment_id": deposit_id}}, status=status.HTTP_200_OK)
            elif response.status_code == 401:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                      "Failed to authenticate with BKA API")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                      "Failed to authenticate with BKA API")

        except Exception as e:
            print("Exception Error: ", str(e))
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Required Data is not given")


class BkashPaymentInitiateAPIView(APIView):

    def post(self, request):
        # Extract individual fields from the request data
        try:
            token = request.data.get('id_token')  # Extract id_token from request
            x_app_key = request.data.get("x_app_key", "0vWQuCRGiUX7EPVjQDr0EUAYtc")  # Default value if not present
            payer_reference = request.data.get('payer_reference', "")  # Default payer reference
            callback_url = request.data.get("callback_url", "http://optixpay.com/call-back/")  # Default callback URL
            merchant_association_info = request.data.get('merchant_association_info',
                                                         "MI05MID54RF091234560ne")  # Default info
            amount = str(request.data.get('amount', "1"))  # Convert amount to string and default to "1"
            currency = request.data.get('currency', "BDT")  # Default currency is BDT
            intent = request.data.get('intent', "authorization")  # Default intent
            invoice_number = generate_invoice_number()  # Generate the unique invoice number

            if token:
                url = f"{settings.BKASH_BASE_URL}/tokenized/checkout/create"
                headers = {
                    'Authorization': f'{token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'x-app-key': x_app_key
                }
                data = {
                    "mode": "0011",
                    "payerReference": payer_reference,
                    "callbackURL": callback_url,
                    "merchantAssociationInfo": merchant_association_info,
                    "amount": amount,
                    "currency": currency,
                    "intent": intent,
                    "merchantInvoiceNumber": invoice_number
                }

                # Make the POST request
                response = requests.post(url, json=data, headers=headers)

                # Handle the response based on status code
                if response.status_code == 200:
                    return CommonResponse(
                        "success", {
                            "data": response.json(),
                            "id_token": token,
                            "x_app_key": x_app_key
                        },
                        HTTP_200_OK, "Start Depositing"
                    )
                return CommonResponse("error", response.json(), response.status_code, "Failed")

            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Could not authenticate")

        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Required Data is not given")

class BkashPaymentExecuteAPIView(APIView):

    def post(self, request):
        try:
            id_token = request.data.get('id_token')
            x_app_key = request.data.get('x_app_key')
            if id_token:
                deposit_id = request.data.get('deposit_id')
                payload = json.dumps({
                    "paymentID": deposit_id
                })
                url = f"{settings.BKASH_BASE_URL}/tokenized/checkout/execute"
                headers = {
                    'Authorization': f'{id_token}',
                    'Accept': 'application/json',
                    'x-app-key': x_app_key,
                }

                deposit_obj = Deposit.objects.get(id=int(deposit_id))

                response = requests.request("POST", url, headers=headers, data=payload)

                if response.status_code == 200 and response.json().get('transactionStatus') and response.json().get(
                        'transactionStatus') == 'Authorized':

                    deposit_obj.order_id = response.json().get('paymentID')
                    # payment_obj.paymentID = response.json().get('paymentID')
                    deposit_obj.txn_id = response.json().get('trxID')
                    # payment_obj.intent = response.json().get('intent')
                    # payment_obj.merchantInvoiceNumber = response.json().get('merchantInvoiceNumber')
                    # payment_obj.payerType = response.json().get('payerType')
                    # payment_obj.payerReference = response.json().get('payerReference')
                    deposit_obj.customer_id = response.json().get('customerMsisdn')
                    deposit_obj.sender_account = response.json().get('payerAccount')
                    deposit_obj.status = "success" if response.json().get('statusMessage').lower() else "cancelled"
                    # payment_obj.transaction_type = 'deposit'
                    deposit_obj.save()

                    return CommonResponse("success", response.json(), status.HTTP_200_OK, "Successful")
                else:
                    deposit_obj.status = "failed"
                    deposit_obj.save()
                    return CommonResponse("error", {}, status.HTTP_406_NOT_ACCEPTABLE, "Payment is unsuccessful")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Could not authenticate")
        except Exception as e:
            print("Exception Error: ", str(e))
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Required Data is not given")
