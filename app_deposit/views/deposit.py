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
    # def get(self, request):
    #     search_keyword = request.query_params.get('search_keyword', None)
    #
    #     if search_keyword:
    #         deposits = Deposit.objects.filter(
    #             Q(customer_id__icontains=search_keyword) |
    #             Q(order_id__icontains=search_keyword) |
    #             Q(oxp_id__icontains=search_keyword) |
    #             Q(txn_id__icontains=search_keyword) |
    #             Q(sender_account__icontains=search_keyword) |
    #             Q(receiver_account__icontains=search_keyword) |
    #             Q(merchant_id__full_name__icontains=search_keyword) |  # Assuming 'name' is a field in Profile model
    #             Q(bank__bank_name__icontains=search_keyword)  # Assuming 'name' is a field in BankModel
    #         )
    #     else:
    #         # Get all deposits
    #         deposits = Deposit.objects.all()
    #
    #     # Instantiate the custom paginator
    #     paginator = CustomPagination()
    #
    #     # Apply pagination to the queryset
    #     page = paginator.paginate_queryset(deposits, request, view=self)
    #
    #     if page is not None:
    #         # Serialize page instead of entire queryset
    #         serializer = DepositListSerializer(page, many=True)
    #         return paginator.get_paginated_response(serializer.data)
    #
    #     # If no page, meaning pagination failed or not needed, return all items
    #     serializer = DepositListSerializer(deposits, many=True)
    #     return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Found!")

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            deposit_id = request.query_params.get('deposit_id', None)
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Build queryset
            deposits = Deposit.objects.all()

            if deposit_id:
                try:
                    agent = Deposit.objects.get(id=deposit_id)
                    deposit_serializers = DepositSerializer(agent)
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
            if is_active:
                deposits = deposits.filter(is_active=is_active)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(deposits, request)

            if result_page is not None:
                deposits_serializers = DepositSerializer(result_page, many=True)
                return paginator.get_paginated_response(deposits_serializers.data)
            else:
                return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "No deposits available")

        except Deposit.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Agent not found")
        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Agent not found")


    @swagger_auto_schema(
        operation_description="Create a new deposit",
        request_body=DepositSerializer,
        responses={
            201: openapi.Response('Deposit created successfully.', DepositSerializer),
            400: "Validation Error"
        }
    )
    # def post(self, request):
    #     pass
    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            # Save the deposit record
            deposit = serializer.save(created_by=request.user, updated_by=request.user, is_active=True)

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
