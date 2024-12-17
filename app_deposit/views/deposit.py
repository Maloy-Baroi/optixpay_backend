# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from ..models.deposit import Deposit
# # from ..serializers.deposit import DepositSerializer

# # class CreateDepositAPIView(APIView):
# #     def post(self, request, *args, **kwargs):
# #         serializer = DepositSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # class RetrieveDepositAPIView(APIView):
# #     def get(self, request, pk, *args, **kwargs):
# #         try:
# #             deposit = Deposit.objects.get(pk=pk)
# #         except Deposit.DoesNotExist:
# #             return Response({"error": "Deposit not found."}, status=status.HTTP_404_NOT_FOUND)

# #         serializer = DepositSerializer(deposit)
# #         return Response(serializer.data, status=status.HTTP_200_OK)


# # class UpdateDepositAPIView(APIView):

# #     def put(self, request, pk, *args, **kwargs):
# #         try:
# #             deposit = Deposit.objects.get(pk=pk)
# #         except Deposit.DoesNotExist:
# #             return Response({"error": "Deposit not found."}, status=status.HTTP_404_NOT_FOUND)

# #         serializer = DepositSerializer(deposit, data=request.data, partial=True)  # Use partial=True for partial updates
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # class DeleteDepositAPIView(APIView):
# #     def delete(self, request, pk, *args, **kwargs):
# #         try:
# #             deposit = Deposit.objects.get(pk=pk)
# #         except Deposit.DoesNotExist:
# #             return Response({"error": "Deposit not found."}, status=status.HTTP_404_NOT_FOUND)

# #         deposit.delete()
# #         return Response({"message": "Deposit deleted successfully."}, status=status.HTTP_204_NO_CONTENT)










# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions

# # from optixpay_backend.app_auth import serializers
# from app_deposit.models.deposit import Deposit
# from app_deposit.serializers.deposit import DepositSerializer
# from rest_framework import serializers

# from app_profile.models.profile import Profile

# from custompermissions import IsMerchant


# class DepositListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         """
#         List all deposits for the current merchant.
#         """
#         deposits = Deposit.objects.filter(merchant__user=request.user)
#         serializer = DepositSerializer(deposits, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         """
#         Create a new deposit.
#         """
#         profile = Profile.objects.filter(user=request.user).first()
#         if profile and profile.profile_type == "MC":

#             serializer = DepositSerializer(data=request.data, context={'request': request})
#             if serializer.is_valid():
#                 serializer.save(merchant=profile)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DepositDetailView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsMerchant]

#     def get_object(self, pk, user):
#         """
#         Retrieve the deposit object, ensuring it belongs to the current merchant.
#         """
#         try:
#             return Deposit.objects.get(pk=pk, merchant__user=user)
#         except Deposit.DoesNotExist:
#             raise serializers.ValidationError('Deposit not found.')

#     def get(self, request, pk, *args, **kwargs):
#         """
#         Retrieve a specific deposit.
#         """
#         deposit = self.get_object(pk, request.user)
#         serializer = DepositSerializer(deposit)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk, *args, **kwargs):
#         """
#         Update a specific deposit.
#         """
#         deposit = self.get_object(pk, request.user)
#         profile = Profile.objects.filter(user=request.user).first()
#         if profile and profile.profile_type == "MC":
#             serializer = DepositSerializer(deposit, data=request.data, partial=True, context={'request': request})
#             if serializer.is_valid():
#                 serializer.save(merchant=profile)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, *args, **kwargs):
#         """
#         Delete a specific deposit.
#         """
#         profile = Profile.objects.filter(user=request.user).first()
#         if profile and profile.profile_type == "MC":
#             deposit = self.get_object(pk, request.user)
#             deposit.delete()
#             return Response({'detail': 'Deposit deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)












from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app_deposit.models.deposit import Deposit
from app_deposit.serializers.deposit import DepositSerializer

from app_profile.models.profile import Profile



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
            deposits = Deposit.objects.all()
            serializer = DepositSerializer(deposits, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        profile = Profile.objects.filter(user=request.user).first()
        if serializer.is_valid():
            serializer.save(merchant=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            deposit.delete()
            return Response({"message": "Deposit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Deposit.DoesNotExist:
            return Response({"error": "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
