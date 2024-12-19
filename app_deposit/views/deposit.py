from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app_deposit.models.deposit import Deposit
from app_deposit.serializers.deposit import DepositSerializer

from app_profile.models.profile import Profile
from services.pagination import CustomPagination


class DepositListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

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
            serializer = DepositSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no page, meaning pagination failed or not needed, return all items
        serializer = DepositSerializer(deposits, many=True)
        return Response({"message": "Data Found!", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            # Save the deposit record
            deposit = serializer.save()

            # Return a response
            return Response({
                "message": "Deposit created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                deposit = Deposit.objects.get(pk=pk)
                serializer = DepositSerializer(deposit)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Deposit.DoesNotExist:
                return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Data Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        try:
            deposit = Deposit.objects.get(pk=pk)
            if not deposit:
                return Response({"error": "deposit not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DepositSerializer(deposit, data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Deposit.DoesNotExist:
            return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk=None):
        try:
            deposit = Deposit.objects.get(pk=pk)
            deposit.soft_delete()
            return Response({"message": "Deposit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Deposit.DoesNotExist:
            return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
