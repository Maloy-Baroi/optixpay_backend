from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from app_deposit.models.deposit import Deposit
from app_withdraw.models.withdraw import Withdraw

from app_deposit.serializers.deposit import DepositSerializer
from app_withdraw.serializers.withdraw import WithdrawSerializer

from app_profile.models.profile import Profile



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
            withdraw = Withdraw.objects.all()
            serializer = WithdrawSerializer(withdraw, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        profile = Profile.objects.filter(user=request.user).first()
        if serializer.is_valid():
            serializer.save(merchant=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            serializer = WithdrawSerializer(withdraw, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Withdraw.DoesNotExist:
            return Response({"error": "withdraw not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        try:
            withdraw = Withdraw.objects.get(pk=pk)
            withdraw.delete()
            return Response({"message": "withdraw deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Withdraw.DoesNotExist:
            return Response({"error": "withdraw not found"}, status=status.HTTP_404_NOT_FOUND)
