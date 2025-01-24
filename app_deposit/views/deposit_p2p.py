from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from app_deposit.models.deposit import Deposit
from app_deposit.serializers.deposit import DepositSerializer, DepositCreateSerializer, DepositExternalCreateSerializer
from utils.common_response import CommonResponse


class DepositPtoPCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new deposit",
        request_body=DepositCreateSerializer,
        responses={
            201: openapi.Response('Deposit created successfully.', DepositSerializer),
            400: "Validation Error"
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = DepositExternalCreateSerializer(data=request.data)

            if serializer.is_valid():
                # Save the deposit record

                serializer.save(is_active=True)
                # Return a response
                print("Merchant: ", serializer.data)
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Data Created!")

            # Return validation errors
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Exception as e:
            print(str(e))
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))

class DepositTransactionIdSubmitAPIView(APIView):

    def put(self, request, pk=None):
        try:
            serializer = DepositSerializer(request.data, context={'request': request}, partial=False)
            if serializer.is_valid():
                serializer.save()
                call_back_data = serializer.data
                return CommonResponse("success", call_back_data, status.HTTP_200_OK, "Transaction ID Submitted!")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Transaction id is not valid!")

        except Deposit.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Deposit not found")

