from locale import currency

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# from app_deposit.models.deposit import Deposit
from app_deposit.models.deposit import Currency
# from app_deposit.serializers.deposit import DepositSerializer
from app_deposit.serializers.currency import CurrencySerializer


class CurrencyListPostAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            currencies = Currency.objects.all()
            serializer = CurrencySerializer(currencies, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Currency.DoesNotExist:
            return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class CurrencyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                currency = Currency.objects.get(pk=pk)
                serializer = CurrencySerializer(currency)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Currency.DoesNotExist:
                return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            currency = Currency.objects.all()
            serializer = CurrencySerializer(currency, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        try:
            currency = Currency.objects.get(pk=pk)
            if not currency:
                return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CurrencySerializer(currency, data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Currency.DoesNotExist:
            return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk=None):
        try:
            currency = Currency.objects.get(pk=pk)
            currency.delete()
            return Response({"message": "Currency deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Currency.DoesNotExist:
            return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)
