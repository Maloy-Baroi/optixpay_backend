from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_profile.models.merchant import MerchantProfile
from app_profile.models.wallet import MerchantWallet
from app_profile.serializers.wallet import MerchantWalletSerializer, MerchantWalletCreateSerializer, \
    MerchantWalletUpdateSerializer
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
                return Response({"status": False, "data": {}, "message": "Didn't provide merchant id!"},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                # Assuming that each merchant has only one profile, we use `get` instead of `filter`.
                merchant = MerchantProfile.objects.get(id=int(merchant_id))
            except MerchantProfile.DoesNotExist:
                return Response({"status": False, "data": {}, "message": "Merchant not found!"},
                                status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"status": False, "data": {}, "message": "Invalid merchant ID!"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Assuming `merchant_wallet` is a related name for a reverse ForeignKey or OneToOneField relationship
            wallets = merchant.merchant_wallet.all()  # Adjust according to your model relationship
            if wallets.exists():
                if wallet_id:
                    wallet = wallets.filter(id=wallet_id)
                    if wallet.exists():
                        serializer = MerchantWalletSerializer(wallet.first())
                        return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Wallet found")
                    else:
                        return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Wallet not found")
                serializer = MerchantWalletSerializer(wallets, many=True)
                return Response({"status": True, "data": serializer.data, "message": "Wallets retrieved successfully."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "data": {}, "message": "No wallets found!"},
                                status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))

class MerchantWalletCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            merchant_id = request.data.pop("merchant_id", None)

            serializer = MerchantWalletCreateSerializer(data=request.data, context={"merchant_id": merchant_id})
            if serializer.is_valid():
                serializer.save(created_by=request.user, updated_by=request.user, is_active=True)
                # Access the serializer.data as a property, not a method
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Merchant Wallet Created Successfully!")
            else:
                return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, "Unsuccessful Creation!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class MerchantWalletUpdateView(generics.UpdateAPIView):
    queryset = MerchantWallet.objects.all()
    serializer_class = MerchantWalletUpdateSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            # Determine if this is a partial update
            partial = kwargs.pop('partial', False)

            # Fetch the instance to be updated
            instance = self.get_object()

            # Pass the instance and data to the serializer
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Return the updated data
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully Updated Merchant Wallet!")
        except Exception as e:
            return CommonResponse('error', {}, status.HTTP_400_BAD_REQUEST, str(e))
