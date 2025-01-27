from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from app_deposit.models.deposit import Deposit
from app_deposit.serializers.deposit import DepositSerializer, DepositCreateSerializer, DepositExternalCreateSerializer, \
    DepositPutRequestSerializer
from core.models.InValidTransactionId import InvalidTransactionId
from utils.common_response import CommonResponse
from utils.decrypt_deposit_p2p_data import decrypt_deposit_p2p_data


class DepositPtoPCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = DepositExternalCreateSerializer(data=request.data)

            if serializer.is_valid():
                # Save the deposit record

                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Data Created!")

            # Return validation errors
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))

class DepositTransactionIdSubmitAPIView(APIView):

    def _update_deposit_data(self, data):
        try:
            encrypted_data = data.pop('encrypted_data')
            merchant_unique_id = data.pop('unique_id')
            txn_id = data.pop('txn_id')

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

            deposit_serializer = DepositPutRequestSerializer(deposit)
            invalid_txn = InvalidTransactionId(txn_id=txn_id)
            invalid_txn.save()

            return CommonResponse("success", deposit_serializer.data, status.HTTP_200_OK, "Data Updated!!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))

    def put(self, request, pk=None):
        try:
            return self._update_deposit_data(request.data)
        except Deposit.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Deposit not found")

