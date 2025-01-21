from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_settlement.models.settlement import Settlement
from app_settlement.serializers.settlement import SettlementSerializer
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
                settlements = settlements.filter(settlement_id=settlement_id)

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
                settlements_serializer = SettlementSerializer(result_page, many=True)
                return paginator.get_paginated_response(settlements_serializer.data)
            else:
                return Response({"status": "error", "data": {}, "message": "No settlements available"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"status": "error", "data": {}, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)