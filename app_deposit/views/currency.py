from locale import currency

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# from app_deposit.models.deposit import Deposit
from app_deposit.models.deposit import Currency
# from app_deposit.serializers.deposit import DepositSerializer
from app_deposit.serializers.currency import CurrencySerializer, CreateCurrencySerializer
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
                currency_serializers = CurrencySerializer(result_page, many=True)
                return paginator.get_paginated_response(currency_serializers.data)
            else:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "No currency available")

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving merchant data"
            )


class CreateCurrencyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def _check_if_already_exist(self, requested_data):
        name = requested_data.get('name')
        currency_code = requested_data.get('currency_code')

        print(f"Name: {name}, Currency code: {currency_code}")

        # Perform a case-insensitive search to check for existing records
        previously_existed_currency = Currency.objects.filter(
            Q(name__iexact=name) | Q(currency_code__iexact=currency_code))

        if previously_existed_currency.exists():
            previously_existed_currency = previously_existed_currency.first()
            if previously_existed_currency.is_active:
                print("is_active true")
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                      "Currency already exists!")
            else:
                print("is_active false")
                previously_existed_currency.is_active = True
                previously_existed_currency.name = name
                previously_existed_currency.currency_code = currency_code
                previously_existed_currency.save()
                serializer = CurrencySerializer(previously_existed_currency)
                print("Previously exist: ", previously_existed_currency)
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED,
                                      "Currency successfully created!")
        return None

    def post(self, request):
        response = self._check_if_already_exist(request.data)
        if response is not None:
            return response  # Return the response from check if it's not None
        serializer = CreateCurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
            return Response(
                {'status': 'success', 'data': serializer.data, 'message': 'Successfully created/updated currency'},
                status=status.HTTP_201_CREATED)
        else:
            # Print all serializer errors to debug
            print(serializer.errors)
            return Response({'status': 'error', 'data': {}, 'message': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


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
            serializer = CurrencySerializer(currency, data=request.data, context={'request': request}, partial=True)
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
