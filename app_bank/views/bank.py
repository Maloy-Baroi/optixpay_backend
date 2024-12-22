from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from app_bank.models.bank import BankModel
from app_bank.serializers.bank import BankModelSerializer
from rest_framework.exceptions import NotFound

from app_profile.models.profile import Profile, upload_to


class BankListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            banks = BankModel.objects.all()
            serializer = BankModelSerializer(banks, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            agent_id = request.data.get('agent')
            serializer = BankModelSerializer(data=request.data, context={'request': request})
            print("Profile: ", Profile.objects.filter(id=agent_id))
            profile = Profile.objects.filter(id=agent_id).first() if Profile.objects.filter(id=agent_id).exists() else None
            if serializer.is_valid() and profile:
                serializer.save(agent=profile, created_by=request.user,
                                updated_by=request.user)  # Will automatically set agent and bank_unique_id
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


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
