from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_auth.models import CustomUser
from app_profile.models.staff import StaffProfile
from app_profile.serializers.profile import ProfileSerializer
from app_profile.serializers.staff import StaffSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class StaffListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            staff_id = request.query_params.get('staff_id')
            search_query = request.query_params.get('search', '')
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')
            is_active = request.query_params.get('is_active', True)

            # Filter staffs based on query parameters
            staffs = StaffProfile.objects.all()

            if staff_id:
                try:
                    staff = StaffProfile.objects.get(id=staff_id)
                    staffs_serializers = StaffSerializer(staff)
                    return CommonResponse(
                        "success", staffs_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except StaffProfile.DoesNotExist:
                    return CommonResponse("error", "staff not found", status.HTTP_204_NO_CONTENT)

            if search_query:
                staffs = staffs.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                staffs = staffs.filter(status=search_status)
            if bank:
                staffs = staffs.filter(bank__icontains=bank)
            if is_active:
                staffs = staffs.filter(is_active=is_active)

            if not staffs.exists():
                return CommonResponse("error", "No staffs found", status.HTTP_204_NO_CONTENT)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(staffs, request)

            if result_page is not None:
                staffs_serializers = StaffSerializer(result_page, many=True)
                return paginator.get_paginated_response(staffs_serializers.data)
            else:
                return CommonResponse("error", "No staffs available", status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return CommonResponse(
                "error", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR,
                "An error occurred while retrieving staff data"
            )


class StaffCreateAPIView(APIView):
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
                staff_group, created = Group.objects.get_or_create(name='staff')
                user.groups.add(staff_group)
                user.save()

                # Set up the serializer with the created user and request data
                serializer = StaffSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    # Link the newly created user and the currently authenticated user for created_by and updated_by
                    staff_profile = serializer.save(user=user, created_by=request.user, updated_by=request.user,
                                                       is_active=True, status='Active')
                    return CommonResponse("success", serializer.data,
                                          status=status.HTTP_201_CREATED, message="Successfully Created")
                else:
                    return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Unsuccessful")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class StaffProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return StaffProfile.objects.get(pk=pk)
        except StaffProfile.DoesNotExist:
            return None

    def put(self, request, pk):
        staff_profile = self.get_object(pk)
        if not staff_profile:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "Record not found")

        serializer = StaffSerializer(staff_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully updated")
        else:
            return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Validation errors")


class StaffProfileDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return StaffProfile.objects.get(id=pk)
        except StaffProfile.DoesNotExist:
            return None

    def delete(self, request, pk):
        try:
            staff_profile = self.get_object(pk)
            if not staff_profile:
                return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, 'Record not found')
            else:
                staff_profile.soft_delete()
                return CommonResponse("success", {}, status.HTTP_200_OK, "Successfully Deleted")
        except Exception as e:
            common = CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Record not found")

