from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from unicodedata import category

from app_bank.models.bank import BankTypeModel
from app_bank.serializers.banktype import BankTypeModelSerializer, BankTypeGetSerializer
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
            bank_type_name = request.query_params.get('bank_type_name')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Filter bank_types based on query parameters
            bank_types = BankTypeModel.objects.all()

            if bank_type_name:
                try:
                    bank_type = BankTypeModel.objects.get(category=bank_type_name)
                    bank_types_serializers = BankTypeGetSerializer(bank_type)
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
                bank_types_serializers = BankTypeGetSerializer(result_page, many=True)
                return paginator.get_paginated_response(bank_types_serializers.data)
            else:
                return CommonResponse("error", "No bank_types available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving bank_type data"
            )

class BankTypeCreateAPIView(APIView):
    # Other methods remain unchanged...

    def post(self, request):
        try:
            # Check if the same name and category exist and are currently inactive
            existing_bank_type = BankTypeModel.objects.filter(
                Q(name=request.data.get('name')) &
                Q(category=request.data.get('category')) &
                Q(is_active=False)
            ).first()

            if existing_bank_type:
                # If found, just activate it
                existing_bank_type.is_active = True
                existing_bank_type.updated_by = request.user
                existing_bank_type.save(update_fields=['is_active', 'updated_by'])
                serializer = BankTypeModelSerializer(existing_bank_type)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK,
                                      "Bank Type reactivated successfully")
            else:
                # Otherwise, create a new bank type
                serializer = BankTypeModelSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
                    return CommonResponse("success", serializer.data, status.HTTP_201_CREATED,
                                          "Bank Type Successfully Created")
                else:
                    return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST,
                                          "Error in creating Bank Type")

        except Exception as e:
            return CommonResponse("error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "An error occurred while processing your request")


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
