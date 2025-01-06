from django.contrib.admin.templatetags.admin_list import pagination
from django.db import transaction
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_auth.models import CustomUser
from app_profile.models.merchant import MerchantProfile
from app_profile.serializers.merchant import MerchantProfileSerializer, MerchantUpdateProfileSerializer
from app_profile.serializers.user import UserListSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class MerchantListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            merchant_id = request.query_params.get('merchant_id')
            search_query = request.query_params.get('search_query')
            if merchant_id:
                merchants = MerchantProfile.objects.get(id=merchant_id)
                if not merchants:
                    return CommonResponse("error", "Merchant not found", status.HTTP_404_NOT_FOUND)
                merchants_serializers = MerchantProfileSerializer(merchants)
                return CommonResponse("success", merchants_serializers.data, status.HTTP_200_OK, "Data Found!")

            elif search_query:
                merchants = MerchantProfile.objects.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
                if not merchants.exists():
                    return CommonResponse("error", "Merchant not found", status.HTTP_404_NOT_FOUND)
            else:
                merchants = MerchantProfile.objects.all()

            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(merchants, request)
            if result_page is not None:
                merchants_serializers = MerchantProfileSerializer(result_page, many=True)
                return paginator.get_paginated_response(merchants_serializers.data)
            else:
                return CommonResponse("error", "No merchants available", status.HTTP_404_NOT_FOUND)

        except MerchantProfile.DoesNotExist:
            return CommonResponse("error", "Merchant profile not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CommonResponse("error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  "An error occurred while retrieving merchant data")


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

                # Set up the serializer with the created user and request data
                serializer = MerchantProfileSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    # Link the newly created user and the currently authenticated user for created_by and updated_by
                    merchant_profile = serializer.save(user=user, created_by=request.user, updated_by=request.user)
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
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, 'MerchantProfile not found')
        serializer = MerchantUpdateProfileSerializer(merchant_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", serializer.data,
                                  status.HTTP_200_OK, "Successfully Updated")
        return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST)


class MerchantProfileDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return MerchantProfile.objects.get(pk=pk)
        except MerchantProfile.DoesNotExist:
            return None

    def delete(self, request, pk):
        merchant_profile = self.get_object(pk)
        if not merchant_profile:
            return CommonResponse("error", {}, status=status.HTTP_404_NOT_FOUND, message='MerchantProfile not found')
        merchant_profile.soft_delete()
        return CommonResponse("success", {}, status.HTTP_204_NO_CONTENT, "Deleted Successfully")

# class UserListAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         users = CustomUser.objects.only('id', 'email', 'username')
#         paginator = CustomPagination()
#         result_page = paginator.paginate_queryset(users, request)
#         serializer = UserListSerializer(result_page, many=True)
