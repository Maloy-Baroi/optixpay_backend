from django.db import transaction
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from app_auth.models import CustomUser, CustomGroup
from app_profile.models.merchant import MerchantProfile
from app_profile.serializers.merchant import MerchantProfileSerializer, MerchantUpdateProfileSerializer, \
    MerchantDetailsSerializer
from app_profile.serializers.user import UserListSerializer
from services.is_merchant import IsMerchantUser
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class MerchantDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated, IsMerchantUser)

    def get(self, request):
        try:
            merchant = MerchantProfile.objects.get(user=request.user)
            print("Merchant: ", merchant)
            merchant_serializers = MerchantDetailsSerializer(merchant)
            return CommonResponse("success", merchant_serializers.data, status.HTTP_200_OK, "Merchant data found!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Merchant not found")


class MerchantListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            merchant_id = request.query_params.get('merchant_id')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Filter merchants based on query parameters
            merchants = MerchantProfile.objects.all()

            if merchant_id:
                try:
                    merchant = MerchantProfile.objects.get(id=merchant_id)
                    merchants_serializers = MerchantProfileSerializer(merchant)
                    return CommonResponse(
                        "success", merchants_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except MerchantProfile.DoesNotExist:
                    return CommonResponse("error", "Merchant not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                merchants = merchants.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                merchants = merchants.filter(status=search_status)
            if bank:
                merchants = merchants.filter(bank__icontains=bank)
            if is_active:
                merchants = merchants.filter(is_active=is_active)

            if not merchants.exists():
                return CommonResponse("error", "No merchants found", status.HTTP_204_NO_CONTENT)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(merchants, request)

            if result_page is not None:
                merchants_serializers = MerchantProfileSerializer(result_page, many=True)
                return paginator.get_paginated_response(merchants_serializers.data)
            else:
                return CommonResponse("error", "No merchants available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving merchant data"
            )


class MerchantProfileCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            with transaction.atomic():  # Ensures all operations inside are part of a single transaction
                email = request.data.get('email')
                password = request.data.get('password', "123456")
                username = request.data.get('username')
                users = CustomUser.objects.filter(Q(email=email) | Q(username=username))

                if users.exists():
                    return CommonResponse("error", {},
                                          status=status.HTTP_400_BAD_REQUEST,
                                          message="Username or email already exists")

                # Create the user object
                user = CustomUser(email=email, username=username)
                user.set_password(password)
                user.save()
                merchant_group, created = CustomGroup.objects.get_or_create(name='merchant')
                user.groups.add(merchant_group)
                user.save()

                # Set up the serializer with the created user and request data
                serializer = MerchantProfileSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    # Link the newly created user and the currently authenticated user for created_by and updated_by
                    merchant_profile = serializer.save(user=user, created_by=request.user, updated_by=request.user, is_active=True)
                    return CommonResponse("success", serializer.data,
                                          status=status.HTTP_201_CREATED, message="Successfully Created")
                else:
                    return CommonResponse("error", serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return CommonResponse("error", str(e), status=status.HTTP_400_BAD_REQUEST)


class MerchantProfileUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return MerchantProfile.objects.get(pk=pk)
        except MerchantProfile.DoesNotExist:
            return None

    def put(self, request, pk):
        merchant_profile = self.get_object(pk)
        if not merchant_profile:
            return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, 'MerchantProfile not found')
        serializer = MerchantUpdateProfileSerializer(merchant_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", serializer.data,
                                  status.HTTP_200_OK, "Successfully Updated")
        return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST)


class MerchantProfileDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return MerchantProfile.objects.get(pk=pk, is_active=True)
        except MerchantProfile.DoesNotExist:
            return None

    def delete(self, request, pk):
        merchant_profile = self.get_object(pk)
        if not merchant_profile:
            return CommonResponse("error", {}, status=status.HTTP_204_NO_CONTENT, message='MerchantProfile not found')
        merchant_profile.soft_delete()
        return CommonResponse("success", {}, status.HTTP_200_OK, "Deleted Successfully")

# class UserListAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         users = CustomUser.objects.only('id', 'email', 'username')
#         paginator = CustomPagination()
#         result_page = paginator.paginate_queryset(users, request)
#         serializer = UserListSerializer(result_page, many=True)
