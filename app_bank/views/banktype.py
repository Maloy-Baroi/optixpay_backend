from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from unicodedata import category

from app_bank.models.bank import BankTypeModel
from app_bank.serializers.banktype import BankTypeModelSerializer
from app_deposit.models.deposit import Currency
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class BankTypeListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            bank_type_id = request.query_params.get('bank_type_id')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Filter bank_types based on query parameters
            bank_types = BankTypeModel.objects.all()

            if bank_type_id:
                try:
                    bank_type = BankTypeModel.objects.get(id=bank_type_id)
                    bank_types_serializers = BankTypeModelSerializer(bank_type)
                    return CommonResponse(
                        "success", bank_types_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except BankTypeModel.DoesNotExist:
                    return CommonResponse("error", "bank_type not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                bank_types = bank_types.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                bank_types = bank_types.filter(status=search_status)
            if bank:
                bank_types = bank_types.filter(bank__icontains=bank)
            if is_active:
                bank_types = bank_types.filter(is_active=is_active)

            if not bank_types.exists():
                return CommonResponse("error", "No bank_types found", status.HTTP_204_NO_CONTENT)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(bank_types, request)

            if result_page is not None:
                bank_types_serializers = BankTypeModelSerializer(result_page, many=True)
                return paginator.get_paginated_response(bank_types_serializers.data)
            else:
                return CommonResponse("error", "No bank_types available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving bank_type data"
            )

    def process_or_reactivate_bank_type(self, requested_data):
        name = requested_data.get('name')
        bank_category = requested_data.get('category')
        bank_currency = requested_data.get('currency')

        try:
            bank_type = BankTypeModel.objects.filter(name__iexact=name, category__iexact=bank_category).first()
            if bank_type:
                if bank_type.is_active:
                    return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Bank Type already exists!")

                bank_type.is_active = True
                bank_type.name = name
                bank_type.category = bank_category

                try:
                    currency = Currency.objects.get(id=bank_currency)
                except ObjectDoesNotExist:
                    return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Currency ID not found")

                bank_type.currency = currency
                bank_type.save()

                serializer = BankTypeModelSerializer(bank_type)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return CommonResponse("success", serializer.data, status.HTTP_201_CREATED,
                                          "Bank Type successfully reactivated and updated!")
                else:
                    return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST,
                                          "Invalid data for Bank Type")

            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                      "Bank Type doesn't exist and cannot be created in this method")

        except Exception as e:
            return CommonResponse("error", {"exception": str(e)}, status.HTTP_400_BAD_REQUEST,
                                  "An error occurred processing the request")

    def post(self, request):
        try:
            response = self._check_if_already_exist(request.data)
            if response is not None:
                return response  # Return the response from check if it's not None

            serializer = BankTypeModelSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED,
                                      "Bank Type Successfully Created")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST,
                                      "Bank Type with this name is already exists")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class BankTypeUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk)
            serializer = BankTypeModelSerializer(bank_type, data=request.data, context={'request': request},
                                                 partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Bank Type Successfully Updated")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except BankTypeModel.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Not found")


class BankTypeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk, is_active=True)
            bank_type.soft_delete()  # Perform a soft delete
            return CommonResponse("success", {}, status.HTTP_200_OK, "Bank Type Deleted!")
        except BankTypeModel.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "No Content Found")
