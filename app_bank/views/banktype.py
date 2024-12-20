from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app_bank.models.bank import BankTypeModel
from app_bank.serializers.banktype import BankTypeModelSerializer


class BankTypeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            bank_type = BankTypeModel.objects.all()
            serializer = BankTypeModelSerializer(bank_type, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except BankTypeModel.DoesNotExist:
            return Response({"error": "Data not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = BankTypeModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Bank Type Successfully Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BankTypeRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk)
            serializer = BankTypeModelSerializer(bank_type, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BankTypeModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk)
            bank_type.soft_delete()  # Perform a soft delete
            return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except BankTypeModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)