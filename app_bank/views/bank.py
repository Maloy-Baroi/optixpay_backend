from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from app_bank.models.bank import AgentBankModel, BankTypeModel
from app_bank.serializers.bank import BankModelSerializer
from rest_framework.exceptions import NotFound

from app_profile.models.agent import AgentProfile
from services.is_admin import IsAdminUser
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class BankListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank_id = request.query_params.get('bank_id', '')
            is_active = request.query_params.get('is_active', True)

            # Filter banks based on query parameters
            banks = AgentBankModel.objects.all()

            if bank_id:
                try:
                    bank = AgentBankModel.objects.get(id=bank_id)
                    banks_serializers = BankModelSerializer(bank)
                    return CommonResponse(
                        "success", banks_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except AgentBankModel.DoesNotExist:
                    return CommonResponse("error", "bank not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                banks = banks.filter(
                    Q(bank_name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                banks = banks.filter(status=search_status)
            if is_active:
                banks = banks.filter(is_active=is_active)

            if not banks.exists():
                return CommonResponse("error", "No banks found", status.HTTP_204_NO_CONTENT)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(banks, request)

            if result_page is not None:
                banks_serializers = BankModelSerializer(result_page, many=True)
                return paginator.get_paginated_response(banks_serializers.data)
            else:
                return CommonResponse("error", "No banks available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving bank data"
            )


class BankCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            profile = None
            bank_type = str(request.data.pop('bank_type')).lower()
            bank_method = str(request.data.pop('bank_method')).lower()
            bank_type = BankTypeModel.objects.filter(name__iexact=bank_method, category__iexact=bank_type).first()

            if request.user.groups.filter(name='admin').exists():
                agent_unique_id = request.data.get('agent_unique_id', None)
                profile = AgentProfile.objects.filter(unique_id=agent_unique_id).first() if AgentProfile.objects.filter(
                    unique_id=agent_unique_id).exists() else None

            elif request.user.groups.filter(name='agent').exists():
                profile = AgentProfile.objects.filter(user=request.user).first()
            else:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "User Role does not exist")

            serializer = BankModelSerializer(data=request.data, context={'request': request})
            print("Profile: ", profile)
            if serializer.is_valid() and profile:
                serializer.save(bank_type=bank_type, agent=profile, created_by=request.user,
                                updated_by=request.user,
                                is_active=True)  # Will automatically set agent and bank_unique_id
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
