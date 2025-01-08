from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app_deposit.models.deposit import Deposit
from app_deposit.serializers.deposit import DepositSerializer, DepositListSerializer

from app_profile.models.profile import Profile
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class DepositListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

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
        search_keyword = request.query_params.get('search_keyword', None)

        if search_keyword:
            deposits = Deposit.objects.filter(
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
            # Get all deposits
            deposits = Deposit.objects.all()

        # Instantiate the custom paginator
        paginator = CustomPagination()

        # Apply pagination to the queryset
        page = paginator.paginate_queryset(deposits, request, view=self)

        if page is not None:
            # Serialize page instead of entire queryset
            serializer = DepositListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no page, meaning pagination failed or not needed, return all items
        serializer = DepositListSerializer(deposits, many=True)
        return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Found!")

    @swagger_auto_schema(
        operation_description="Create a new deposit",
        request_body=DepositSerializer,
        responses={
            201: openapi.Response('Deposit created successfully.', DepositSerializer),
            400: "Validation Error"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            # Save the deposit record
            deposit = serializer.save(created_by=request.user, updated_by=request.user)

            # Return a response
            return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Data Created!")

        # Return validation errors
        return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)


class DepositAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                deposit = Deposit.objects.get(pk=pk)
                serializer = DepositSerializer(deposit)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Found!")
            except Deposit.DoesNotExist:
                return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Deposit not found")
        else:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Data Not Found!")

    def put(self, request, pk=None):
        try:
            deposit = Deposit.objects.get(pk=pk)
            if not deposit:
                return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "deposit not found")
            serializer = DepositSerializer(deposit, data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Updated")
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Deposit.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Deposit not found")


    def delete(self, request, pk=None):
        try:
            deposit = Deposit.objects.get(pk=pk, is_active=True)
            deposit.soft_delete()
            return CommonResponse("success", {}, status.HTTP_204_NO_CONTENT, "Deposit deleted successfully")
        except Deposit.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Deposit not found")
