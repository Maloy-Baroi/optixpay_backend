from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_bank.models.bank import BankTypeModel
from app_bank.serializers.banktype import BankTypeModelSerializer, BankTypeOnlyNameSerializer
from app_deposit.models.deposit import Deposit
from app_sms.models.sms import SMSManagement
from app_withdraw.models.withdraw import Withdraw

from app_deposit.serializers.deposit import DepositSerializer
from app_withdraw.serializers.withdraw import WithdrawSerializer, WithdrawCreateSerializer

from app_profile.models.profile import Profile
from django.db.models import Q

from core.models.InValidTransactionId import InvalidTransactionId
from services.is_admin import IsAdminUser
from services.is_agent import IsAgentUser
from services.is_merchant import IsMerchantUser
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class WithdrawListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            withdraw_id = request.query_params.get('withdraw_id')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Filter withdraws based on query parameters
            withdraws = Withdraw.objects.all()

            if withdraw_id:
                try:
                    withdraw = Withdraw.objects.get(id=withdraw_id)
                    withdraws_serializers = WithdrawSerializer(withdraw)
                    return CommonResponse(
                        "success", withdraws_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except Withdraw.DoesNotExist:
                    return CommonResponse("error", "withdraw not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                withdraws = withdraws.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                withdraws = withdraws.filter(status=search_status)
            if bank:
                withdraws = withdraws.filter(bank__icontains=bank)
            if is_active:
                withdraws = withdraws.filter(is_active=is_active)

            if not withdraws.exists():
                return CommonResponse("error", "No withdraws found", status.HTTP_204_NO_CONTENT)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(withdraws, request)

            if result_page is not None:
                withdraws_serializers = WithdrawSerializer(result_page, many=True)
                return paginator.get_paginated_response(withdraws_serializers.data)
            else:
                return CommonResponse("error", "No withdraws available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving withdraw data"
            )


class WithdrawCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMerchantUser]

    def post(self, request, *args, **kwargs):
        try:
            serializer = WithdrawCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Successfully Created!")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Unable to create withdraw request!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Failed to create withdraw request!")


class WithdrawUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAgentUser]

    def _check_transaction_id_validity(self, transaction_id):
        if transaction_id is None:
            return False

        if Withdraw.objects.filter(txn_id=transaction_id).exists():
            return False
        if InvalidTransactionId.objects.filter(txn_id=transaction_id).exists():
            return False
        # if SMSManagement.objects.filter(trx_id=transaction_id).exists() and not InvalidTransactionId.objects.filter(trx_id=transaction_id).exists():
        #     return True
        if Deposit.objects.filter(txn_id=transaction_id).exists():
            return False


    def put(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            transaction_id = request.data.get('txn_id', None)

            # if not self._check_transaction_id_validity(transaction_id):
            #     return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Transaction already exists!")

            serializer = WithdrawSerializer(withdraw, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Updated Data Successfully!")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Withdraw.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Withdraw not found")


class WithdrawDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk, is_active=True)
            if withdraw is None:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Record Not Found")
            withdraw.soft_delete()
            return CommonResponse("success", {}, status.HTTP_204_NO_CONTENT, "Withdraw deleted successfully")
        except Withdraw.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Withdraw not found")


class BankTypeForWithdrawCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            bank_type_names = BankTypeModel.objects.values_list('name', flat=True).distinct()
            bank_type_data = [{'name': name} for name in bank_type_names]  # Convert to list of dictionaries
            bank_type_serializers = BankTypeOnlyNameSerializer(bank_type_data, many=True)
            return CommonResponse("success", bank_type_serializers.data, status.HTTP_200_OK, "Data Found!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Data Not Found!")

