from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app_deposit.models.deposit import Deposit
from app_deposit.serializers.deposit import DepositListSerializer, DepositCreateSerializer, DepositSerializer, \
    DepositInternalCreateSerializer
from app_profile.models.merchant import MerchantProfile

from app_profile.models.profile import Profile
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class DepositListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Retrieve a list of deposits",
        manual_parameters=[
            openapi.Parameter(
                'search_keyword',
                openapi.IN_QUERY,
                description="Keyword to search deposits by customer ID, order ID, etc.",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: DepositListSerializer(many=True)}
    )

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            deposit_id = request.query_params.get('deposit_id', None)
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            bank_type = request.query_params.get('bank_type', '')
            is_active = request.query_params.get('is_active', True)

            # Build queryset
            deposits = Deposit.objects.all()

            if deposit_id:
                try:
                    agent = Deposit.objects.get(id=deposit_id)
                    deposit_serializers = DepositListSerializer(agent)
                    return CommonResponse(
                        "success", deposit_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except Deposit.DoesNotExist:
                    return CommonResponse("error", "Agent not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                deposits = deposits.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                deposits = deposits.filter(status=search_status)
            if bank:
                deposits = deposits.filter(bank__bank_name__icontains=bank)
            if bank_type:
                deposits = deposits.filter(bank__bank_type__category__iexact=bank_type)
            if is_active:
                deposits = deposits.filter(is_active=is_active)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(deposits, request)

            if result_page is not None:
                deposits_serializers = DepositListSerializer(result_page, many=True)
                return paginator.get_paginated_response(deposits_serializers.data)
            else:
                return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "No deposits available")

        except Deposit.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Agent not found")
        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Agent not found")

class DepositAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                deposit = Deposit.objects.get(pk=pk)
                serializer = DepositSerializer(deposit)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Found!")
            except Deposit.DoesNotExist:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Deposit not found")
        else:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Data Not Found!")

    def put(self, request, pk=None):
        try:
            deposit = Deposit.objects.get(pk=pk)
            if not deposit:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Deposit not found")
            serializer = DepositSerializer(deposit, data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Updated")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Deposit.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Deposit not found")


    def delete(self, request, pk=None):
        try:
            deposit = Deposit.objects.get(pk=pk, is_active=True)
            deposit.soft_delete()
            return CommonResponse("success", {}, status.HTTP_204_NO_CONTENT, "Deposit deleted successfully")
        except Deposit.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Deposit not found")


class DepositCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Deposit.objects.all()
    serializer_class = DepositInternalCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            login_user = request.user
            merchants = MerchantProfile.objects.filter(user=login_user)

            if merchants.exists():
                merchant = merchants.first()
            else:
                merchant_id = request.data.pop("merchant_id", None)
                if merchant_id is None:
                    return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Merchant not found")
                else:
                    merchant = MerchantProfile.objects.filter(id=merchant_id)
                    if merchant.exists():
                        merchant = merchant.first()
                    else:
                        return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Merchant not found")

            serializer = DepositInternalCreateSerializer(data=request.data, context={'merchant_id': merchant})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))
