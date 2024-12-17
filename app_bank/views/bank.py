
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from app_bank.models.bank import BankModel
# from app_bank.serializers.bank import BankSerializer
# from custompermissions import IsAgent

# from app_profile.models.profile import Profile


# class BankListRetrieveAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk=None):
#         """
#         GET: List all banks or retrieve a single bank by ID.
#         """
#         if pk:
#             try:
#                 bank = BankModel.objects.get(pk=pk)
#                 serializer = BankSerializer(bank)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except BankModel.DoesNotExist:
#                 return Response(
#                     {"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND
#                 )
#         else:
#             banks = BankModel.objects.all()
#             serializer = BankSerializer(banks, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """
#         POST: Create a new bank.
#         """
#         # Automatically assign the agent to the authenticated user's profile
#         profile = Profile.objects.filter(user=request.user).first()
#         if profile and profile.profile_type == "AG":
#             # request.data['agent'] = profile.id  # Set the agent field from the authenticated user's profile

#             serializer = BankSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(agent=profile)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # def post(self, request):
#     #     """
#     #     POST: Create a new bank.
#     #     """
#     #     # Automatically assign the agent to the authenticated user's profile
#     #     profile = Profile.objects.filter(user=request.user).first()
#     #     if profile and profile.profile_type == 'AG':
#     #         # Create a mutable copy of request.data
#     #         data = request.data.copy()
#     #         data['agent'] = profile.id  # Set the agent field from the authenticated user's profile

#     #         # Use the mutable copy to validate and save
#     #         serializer = BankSerializer(data=data)
#     #         if serializer.is_valid():
#     #             serializer.save()
#     #             return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     #     else:
#     #         return Response({"error": "You are not authorized to create a bank."}, status=status.HTTP_403_FORBIDDEN)


# class BankPostPutDeleteAPIView(APIView):
#     permission_classes = [IsAuthenticated, IsAgent]

#     def put(self, request, pk):
#         """
#         PUT: Update an existing bank (full update).
#         """
#         try:
#             bank = BankModel.objects.get(pk=pk)
#         except BankModel.DoesNotExist:
#             return Response(
#                 {"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         if bank.agent.user != request.user:
#             return Response(
#                 {"error": "You can only update your own bank info."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         profile = Profile.objects.filter(user=request.user).first()
#         # if profile and profile.profile_type == 'AG':
#         # Automatically assign the agent to the authenticated user's profile
#         # request.data['agent'] = profile.id

#         serializer = BankSerializer(
#             bank, data=request.data, partial=False
#         )  # Full update
#         if serializer.is_valid():
#             serializer.save(agent=profile)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         """
#         DELETE: Delete a bank by ID (only for the bank's assigned agent).
#         """
#         try:
#             bank = BankModel.objects.get(pk=pk)
#         except BankModel.DoesNotExist:
#             return Response(
#                 {"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         # Check if the authenticated user is the agent of the bank
#         if bank.agent.user != request.user:
#             return Response(
#                 {"error": "You can only delete your own bank."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         bank.delete()
#         return Response(
#             {"message": "Bank deleted successfully"}, status=status.HTTP_204_NO_CONTENT
#         )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_bank.models.bank import BankModel
from app_bank.serializers.bank import BankModelSerializer
from rest_framework.exceptions import NotFound

from app_profile.models.profile import Profile





class BankModelAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                bank = BankModel.objects.get(pk=pk)
            except BankModel.DoesNotExist:
                raise NotFound(detail="Bank not found.")
            serializer = BankModelSerializer(bank)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            banks = BankModel.objects.all()
            serializer = BankModelSerializer(banks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BankModelSerializer(data=request.data, context={'request': request})
        profile = Profile.objects.filter(user=request.user).first()
        if serializer.is_valid():
            serializer.save(agent=profile)  # Will automatically set agent and bank_unique_id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            bank = BankModel.objects.get(pk=pk)
        except BankModel.DoesNotExist:
            raise NotFound(detail="Bank not found.")

        serializer = BankModelSerializer(bank, data=request.data, partial=True, context={'request': request})
        profile = Profile.objects.filter(user=request.user).first()
        if serializer.is_valid():
            serializer.save(agent=profile)  # Will automatically set agent if not provided
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            bank = BankModel.objects.get(pk=pk)
        except BankModel.DoesNotExist:
            raise NotFound(detail="Bank not found.")

        bank.delete()
        return Response({"detail": "Bank deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
