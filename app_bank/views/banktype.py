# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from app_bank.models.bank import  BankTypeModel
# from app_bank.serializers.banktype import  BankTypeSerializer
# from custompermissions import IsSuperUser

# class BankTypeSuperUserAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsSuperUser]

#     def post(self, request):
#         """Create a new Bank Type"""
#         serializer = BankTypeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         """Update an existing Bank Type"""
#         try:
#             bank_type = BankTypeModel.objects.get(pk=pk)
#         except BankTypeModel.DoesNotExist:
#             return Response({"error": "BankType not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = BankTypeSerializer(bank_type, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         """Delete a Bank Type"""
#         try:
#             bank_type = BankTypeModel.objects.get(pk=pk)
#             bank_type.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except BankTypeModel.DoesNotExist:
#             return Response({"error": "BankType not found"}, status=status.HTTP_404_NOT_FOUND)


# class BankTypeAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk=None):
#         """Retrieve one or all Bank Types"""
#         if pk:
#             try:
#                 bank_type = BankTypeModel.objects.get(pk=pk)
#                 serializer = BankTypeSerializer(bank_type)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except BankTypeModel.DoesNotExist:
#                 return Response({"error": "BankType not found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             bank_types = BankTypeModel.objects.all()
#             serializer = BankTypeSerializer(bank_types, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app_bank.models.bank import BankTypeModel
from app_bank.serializers.banktype import BankTypeModelSerializer


class BankTypeModelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                bank_type = BankTypeModel.objects.get(pk=pk)
                serializer = BankTypeModelSerializer(bank_type)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BankTypeModel.DoesNotExist:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            bank_types = BankTypeModel.objects.filter()
            serializer = BankTypeModelSerializer(bank_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BankTypeModelSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk)
            serializer = BankTypeModelSerializer(bank_type, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BankTypeModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            bank_type = BankTypeModel.objects.get(pk=pk)
            bank_type.soft_delete()  # Perform a soft delete
            return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except BankTypeModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)