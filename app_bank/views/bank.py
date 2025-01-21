from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from app_bank.models.bank import AgentBankModel
from app_bank.serializers.bank import BankModelSerializer
from rest_framework.exceptions import NotFound

from app_profile.models.agent import AgentProfile
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class BankListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            banks = AgentBankModel.objects.all()

            serializer = BankModelSerializer(banks, many=True)
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Fetched Success!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))

class BankCreateAPIView(APIView):

    def post(self, request):
        try:
            agent_id = request.data.get('agent')
            serializer = BankModelSerializer(data=request.data, context={'request': request})
            profile = AgentProfile.objects.filter(id=agent_id).first() if AgentProfile.objects.filter(id=agent_id).exists() else None
            if serializer.is_valid() and profile:
                serializer.save(agent=profile, created_by=request.user,
                                updated_by=request.user, is_active=True)  # Will automatically set agent and bank_unique_id
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Created Successfully")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Created Unsuccessful!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class BankUpdateAPIView(APIView):
    # def get(self, request, pk=None):
    #     if pk:
    #         try:
    #             bank = AgentBankModel.objects.get(pk=pk)
    #         except AgentBankModel.DoesNotExist:
    #             raise NotFound(detail="Bank not found.")
    #         serializer = BankModelSerializer(bank)
    #         return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Fetched Success!")
    #     else:
    #         banks = AgentBankModel.objects.all()
    #         serializer = BankModelSerializer(banks, many=True)
    #         return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Data Fetched Success!")

    def put(self, request, pk):
        try:
            bank = AgentBankModel.objects.get(id=pk)
        except AgentBankModel.DoesNotExist:
            raise NotFound(detail="Bank not found.")

        serializer = BankModelSerializer(bank, data=request.data, partial=True, context={'request': request})
        # profile = AgentProfile.objects.filter(user=request.user).first()
        if serializer.is_valid():
            serializer.save()  # Will automatically set agent if not provided
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Updated Success!")
        return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)


class BankDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk=None):
        try:
            bank = AgentBankModel.objects.get(pk=pk, is_active=True)
            bank.soft_delete()
            return CommonResponse("success", {}, status.HTTP_200_OK, "Bank deleted successfully.")
        except AgentBankModel.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Record not found.")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, str(e))
