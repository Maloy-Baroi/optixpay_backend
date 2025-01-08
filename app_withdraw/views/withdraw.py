from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from app_deposit.models.deposit import Deposit
from app_withdraw.models.withdraw import Withdraw

from app_deposit.serializers.deposit import DepositSerializer
from app_withdraw.serializers.withdraw import WithdrawSerializer

from app_profile.models.profile import Profile
from django.db.models import Q
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class WithdrawListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        search_keyword = request.query_params.get('search_keyword', None)

        if search_keyword:
            withdraws = Withdraw.objects.filter(
                Q(customer_id__icontains=search_keyword) |
                Q(order_id__icontains=search_keyword) |
                Q(oxp_id__icontains=search_keyword) |
                Q(txn_id__icontains=search_keyword) |
                Q(sender_account__icontains=search_keyword) |
                Q(receiver_account__icontains=search_keyword) |
                Q(merchant_id__full_name__icontains=search_keyword) |  # Assuming 'name' is a field in Profile model
                Q(bank__bank_name__icontains=search_keyword)  # Assuming 'name' is a field in BankModel
            )
        else:
            # Get all withdraws
            withdraws = Withdraw.objects.all()

        # Instantiate the custom paginator
        paginator = CustomPagination()

        # Apply pagination to the queryset
        page = paginator.paginate_queryset(withdraws, request, view=self)

        if page is not None:
            # Serialize page instead of entire queryset
            serializer = WithdrawSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no page, meaning pagination failed or not needed, return all items
        serializer = WithdrawSerializer(withdraws, many=True)
        return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Found!")

    def post(self, request):
        pass


class WithdrawAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                withdraw = Withdraw.objects.get(pk=pk)
                serializer = WithdrawSerializer(withdraw)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Found!")
            except Withdraw.DoesNotExist:
                return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Withdraw not found")
        else:
            return CommonResponse("error",{}, status.HTTP_404_NOT_FOUND, "Data Not Found!")

    def put(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            if not withdraw:
                return CommonResponse("error",{}, status.HTTP_404_NOT_FOUND, "withdraw not found")
            serializer = WithdrawSerializer(withdraw, data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Updated Data Successfully!")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Withdraw.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Withdraw not found")


    def delete(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk, is_active=True)
            if withdraw is None:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Record Not Found")
            withdraw.soft_delete()
            return CommonResponse("success", {}, status.HTTP_204_NO_CONTENT, "Withdraw deleted successfully")
        except Withdraw.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Withdraw not found")
