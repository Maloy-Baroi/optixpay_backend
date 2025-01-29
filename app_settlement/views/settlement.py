from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_profile.models.merchant import MerchantProfile
from app_settlement.models.settlement import Settlement
from app_settlement.serializers.settlement import SettlementListSerializer, SettlementCreateSerializer, \
    SettlementUpdateSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class SettlementListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Use your custom pagination class

    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            settlement_id = request.query_params.get('settlement_id')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')

            settlements = Settlement.objects.all()

            if settlement_id:
                settlements = settlements.filter(id=settlement_id)

            if search_query:
                settlements = settlements.filter(
                    Q(merchant_id__name__icontains=search_query) |
                    Q(settlement_id__icontains=search_query)
                )
            if search_status:
                settlements = settlements.filter(status=search_status)

            if not settlements.exists():
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "No settlements found")

            paginator = self.pagination_class()
            paginator.page_size = int(page_size)
            result_page = paginator.paginate_queryset(settlements, request)

            if result_page is not None:
                settlements_serializer = SettlementListSerializer(result_page, many=True)
                return paginator.get_paginated_response(settlements_serializer.data)
            else:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "No settlements Record found")


        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "No settlements Record found")


class SettlementCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            merchant = MerchantProfile.objects.get(user=request.user)
            settlement_serializer = SettlementCreateSerializer(data=request.data,
                                                         context={'request': request, 'merchant_id': merchant})
            if settlement_serializer.is_valid():
                settlement_serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
                return CommonResponse('success', settlement_serializer.data, status.HTTP_201_CREATED,
                                      "Successfully created settlement")
            else:
                return CommonResponse('error', {}, status.HTTP_400_BAD_REQUEST, "Unsuccessful creation of settlement")
        except Exception as e:
            return CommonResponse('error', {}, status.HTTP_400_BAD_REQUEST, str(e))


class SettlementUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            settlement = Settlement.objects.get(id=pk)
            settlement_update_serializer = SettlementUpdateSerializer(settlement, data=request.data, partial=True)
            if settlement_update_serializer.is_valid():
                settlement_update_serializer.save(updated_by=request.user)
                return CommonResponse('success', settlement_update_serializer.data, status.HTTP_200_OK,
                                      "Successfully updated!")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Settlement Update issue raised!")

        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))

