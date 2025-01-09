from locale import currency

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
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
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            currency_id = request.query_params.get('currency_id')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Filter currencys based on query parameters
            currencys = Currency.objects.all()

            if currency_id:
                try:
                    currency = Currency.objects.get(id=currency_id)
                    currencys_serializers = CurrencySerializer(currency)
                    return CommonResponse(
                        "success", currencys_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except Currency.DoesNotExist:
                    return CommonResponse("error", "Currency not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                currencys = currencys.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                currencys = currencys.filter(status=search_status)
            if bank:
                currencys = currencys.filter(bank__icontains=bank)
            if is_active:
                currencys = currencys.filter(is_active=is_active)

            if not currencys.exists():
                return CommonResponse("error", "No Currency found", status.HTTP_204_NO_CONTENT)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(currencys, request)

            if result_page is not None:
                currencys_serializers = CurrencySerializer(result_page, many=True)
                return paginator.get_paginated_response(currencys_serializers.data)
            else:
                return CommonResponse("error", "No currency available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving merchant data"
            )

        #     queryset = Currency.objects.all()
        #     paginator = self.pagination_class()
        #     result_page = paginator.paginate_queryset(queryset, request)
        #     serializer = CurrencySerializer(result_page, many=True)
        #     return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully fetched all currencies")
        # except Currency.DoesNotExist:
        #     return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Deposit not found")

    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
            return CommonResponse("success", serializer.data, status.HTTP_201_CREATED,
                                  "Successfully created new currency")
        else:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Unsuccessful")


class CurrencyUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                currency = Currency.objects.get(id=pk)
                serializer = CurrencySerializer(currency)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully fetched currency")
            except Currency.DoesNotExist:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Currency not found")
        else:
            currencies = Currency.objects.all()
            serializer = CurrencySerializer(currencies, many=True)
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully fetched all currencies")

    def put(self, request, pk=None):
        if not pk:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Missing currency identifier")
        try:
            currency = Currency.objects.get(pk=pk)
            serializer = CurrencySerializer(currency, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully updated currency")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Invalid data")
        except Currency.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Currency not found")


class CurrencyDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk=None):
        if not pk:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Missing currency identifier")
        try:
            currency = Currency.objects.get(pk=pk, is_active=True)
            currency.soft_delete()
            return CommonResponse("success", {}, status.HTTP_200_OK, "Currency deleted successfully")
        except Currency.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Currency not found")
