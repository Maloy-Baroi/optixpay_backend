from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_profile.models.wallet import MerchantWallet
from app_profile.serializers.wallet import MerchantWalletSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class MerchantWalletAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')

            wallet = MerchantWallet.objects.filter(balance__gte=1)
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(wallet, request)

            if result_page is not None:
                serializer = MerchantWalletSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "No Record Found!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))



