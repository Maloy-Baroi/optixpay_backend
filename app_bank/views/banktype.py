from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app_bank.models.bank import BankTypeModel
from app_bank.serializers.banktype import BankTypeModelSerializer
from utils.common_response import CommonResponse


class BankTypeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            bank_type = BankTypeModel.objects.all()
            serializer = BankTypeModelSerializer(bank_type, many=True)
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully get bank type")
        except BankTypeModel.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Data not found.")

    def post(self, request):
        serializer = BankTypeModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Bank Type Successfully Created")
        return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)


class BankTypeUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk)
            serializer = BankTypeModelSerializer(bank_type, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Bank Type Successfully Updated")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except BankTypeModel.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Not found")


class BankTypeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk, is_active=True)
            bank_type.soft_delete()  # Perform a soft delete
            return CommonResponse("success", "Deleted successfully", status.HTTP_204_NO_CONTENT, "Bank Type Deleted!")
        except BankTypeModel.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "No Content Found")