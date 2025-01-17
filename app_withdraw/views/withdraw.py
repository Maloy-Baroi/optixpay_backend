from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_deposit.models.deposit import Deposit
from app_withdraw.models.withdraw import Withdraw

from app_deposit.serializers.deposit import DepositSerializer
from app_withdraw.serializers.withdraw import WithdrawSerializer

from app_profile.models.profile import Profile
from django.db.models import Q

from services.is_admin import IsAdminUser, IsMerchantUser
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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
            return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Successfully Created!")
        return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Unable to create withdraw!")


class WithdrawUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            # Check permissions for the object based on user type and status
            if not self.check_object_permissions(request, withdraw):
                return CommonResponse("error", {}, status.HTTP_403_FORBIDDEN,
                                      "Update not allowed based on your user group and withdraw status.")

            serializer = WithdrawSerializer(withdraw, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Updated Data Successfully!")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Withdraw.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Withdraw not found")

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if hasattr(permission, 'has_object_permission'):
                if not permission.has_object_permission(request, self, obj):
                    return False
        return True

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
