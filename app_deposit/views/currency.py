from locale import currency

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# from app_deposit.models.deposit import Deposit
from app_deposit.models.deposit import Currency
# from app_deposit.serializers.deposit import DepositSerializer
from app_deposit.serializers.currency import CurrencySerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class CurrencyListPostAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            queryset = Currency.objects.all()
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = CurrencySerializer(result_page, many=True)
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully fetched all currencies")
        except Currency.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Deposit not found")

    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Successfully created new currency")
        else:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)



class CurrencyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                currency = Currency.objects.get(pk=pk)
                serializer = CurrencySerializer(currency)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully fetched currency")
            except Currency.DoesNotExist:
                return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Deposit not found")
        else:
            currency = Currency.objects.all()
            serializer = CurrencySerializer(currency, many=True)
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully fetched currency")

    def put(self, request, pk=None):
        try:
            currency = Currency.objects.get(pk=pk)
            if not currency:
                return CommonResponse("error", status.HTTP_404_NOT_FOUND, "Currency not found")
            serializer = CurrencySerializer(currency, data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully updated currency")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Currency.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Currency not found")


    def delete(self, request, pk=None):
        try:
            currency = Currency.objects.get(pk=pk, is_active=True)
            if currency is None:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Currency Not Found!")
            currency.soft_delete()
            return CommonResponse("success", {}, status.HTTP_204_NO_CONTENT, "Currency deleted successfully")
        except Currency.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Currency not found")
