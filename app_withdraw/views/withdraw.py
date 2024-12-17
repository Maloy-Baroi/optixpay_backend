from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from app_deposit.models.deposit import Deposit
from app_withdraw.models.withdraw import Withdraw

from app_deposit.serializers.deposit import DepositSerializer
from app_withdraw.serializers.withdraw import WithdrawSerializer

from app_profile.models.profile import Profile



# class WithdrawAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, pk=None):
#         if pk:
#             try:
#                 withdraw = Withdraw.objects.get(pk=pk)
#                 serializer = WithdrawSerializer(withdraw)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Withdraw.DoesNotExist:
#                 return Response({"error": "Withdraw not found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             withdraw = Withdraw.objects.all()
#             serializer = WithdrawSerializer(withdraw, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = WithdrawSerializer(data=request.data)
#         profile = Profile.objects.filter(user=request.user).first()
#         if serializer.is_valid():
#             serializer.save(merchant=profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk=None):
#         try:
#             withdraw = Withdraw.objects.get(pk=pk)
#             serializer = WithdrawSerializer(withdraw, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Withdraw.DoesNotExist:
#             return Response({"error": "withdraw not found"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk=None):
#         try:
#             withdraw = Withdraw.objects.get(pk=pk)
#             withdraw.delete()
#             return Response({"message": "withdraw deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         except Withdraw.DoesNotExist:
#             return Response({"error": "withdraw not found"}, status=status.HTTP_404_NOT_FOUND)



from django.db.models import Q
from services.pagination import CustomPagination



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
        return Response({"message": "Data Found!", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        pass


class WithdrawAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                withdraw = Withdraw.objects.get(pk=pk)
                serializer = WithdrawSerializer(withdraw)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Withdraw.DoesNotExist:
                return Response({"error": "Withdraw not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Data Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            if not withdraw:
                return Response({"error": "withdraw not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = WithdrawSerializer(withdraw, data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Withdraw.DoesNotExist:
            return Response({"error": "Withdraw not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            withdraw.soft_delete()
            return Response({"message": "Withdraw deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Withdraw.DoesNotExist:
            return Response({"error": "Withdraw not found"}, status=status.HTTP_404_NOT_FOUND)
