from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_sms.models.sms import SMSManagement
from app_sms.serializers.sms import SMSManagementSerializer, SMSManagementUpdateSerializer
from services.pagination import CustomPagination
from services.token_generator import create_token
from utils.common_response import CommonResponse


class GenerateAccessToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return CommonResponse("success", create_token(request.user), status.HTTP_200_OK, "Successfully generate access token.")


class SMSListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            sms_id = request.query_params.get('sms_id', None)
            search_status = request.query_params.get('status', '')
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            # Build queryset
            smses = SMSManagement.objects.all()

            if sms_id:
                try:
                    sms = SMSManagement.objects.get(id=sms_id)
                    sms_serializers = SMSManagementSerializer(sms)
                    return CommonResponse(
                        "success", sms_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except SMSManagement.DoesNotExist:
                    return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Record not found")

            if search_query:
                smses = smses.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                smses = smses.filter(status=search_status)

            if start_date and end_date:
                smses = smses.filter(send_date__gte=start_date, send_date__lte=end_date)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(smses, request)

            if result_page is not None:
                smses_serializers = SMSManagementSerializer(result_page, many=True)
                return paginator.get_paginated_response(smses_serializers.data)
            else:
                return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")

        except SMSManagement.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")

        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")


class SMSCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = SMSManagementSerializer(data=request.data)
            if serializer.is_valid():
                # Set the creator of the prepayment
                serializer.save(created_by=request.user, updated_by=request.user, status='Confirmed', is_active=True)
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Successful Created")
            else:
                return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Unsuccessful!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class SMSUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            sms = get_object_or_404(SMSManagement, pk=pk)
            serializer = SMSManagementUpdateSerializer(sms, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Record updated")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except ValidationError as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


class SMSDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            sms = get_object_or_404(SMSManagement, pk=pk)
            sms.soft_delete()

            return CommonResponse("success", [], status.HTTP_200_OK, "Successfully deleted!")
        except SMSManagement.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found!")
        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")

