from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_profile.models.merchant import MerchantProfile
from app_profile.models.wallet import MerchantWallet
from app_profile.serializers.wallet import MerchantWalletSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class MerchantWalletListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            merchant_id = request.query_params.get('merchant_id', None)
            wallet_id = request.query_params.get('wallet_id', None)

            if merchant_id is None:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Didn't provide merchant id!")

            merchant = MerchantProfile.objects.filter(id=merchant_id)
            if merchant is None:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Merchant not found!")

            if wallet_id is None:
                wallets = merchant.merchant_wallet.filter(id=wallet_id).first()
                if wallets is None:
                    return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Wallet not found!")
            else:
                wallets = merchant.merchant_wallet.all()
                if wallets is None:
                    return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Wallet not found!")

            if wallets is not None:
                serializer = MerchantWalletSerializer(wallets, many=True)
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Wallet list Found!")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "No Record Found!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class MerchantWalletCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = MerchantWalletSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user, updated_by=request.user)
                return CommonResponse("success", {}, status.HTTP_201_CREATED, "Merchant Wallet Created Successfully!")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Unsuccessful Creation!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))



