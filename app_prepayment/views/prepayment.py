from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app_prepayment.models.prepayment import Prepayment
from app_prepayment.serializers.prepayment import PrepaymentSerializer, PrepaymentUpdateSerializer
from app_profile.models.agent import AgentProfile
from services.pagination import CustomPagination
from utils.common_response import CommonResponse



class PrepaymentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            prepayment_id = request.query_params.get('prepayment_id', None)
            search_status = request.query_params.get('status', '')

            # Build queryset
            prepayments = Prepayment.objects.all()

            if prepayment_id:
                try:
                    prepayment = Prepayment.objects.get(id=prepayment_id)
                    prepayment_serializers = PrepaymentSerializer(prepayment)
                    return CommonResponse(
                        "success", prepayment_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except Prepayment.DoesNotExist:
                    return CommonResponse("error", "Record not found", status.HTTP_404_NOT_FOUND)

            if search_query:
                prepayments = prepayments.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                prepayments = prepayments.filter(status=search_status)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(prepayments, request)

            if result_page is not None:
                prepayments_serializers = PrepaymentSerializer(result_page, many=True)
                return paginator.get_paginated_response(prepayments_serializers.data)
            else:
                return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")

        except Prepayment.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")

        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")

    def post(self, request):
        try:
            serializer = PrepaymentSerializer(data=request.data)
            if serializer.is_valid():
                # Set the creator of the prepayment
                agent = AgentProfile.objects.get(user=request.user)
                serializer.save(agent_id=agent,created_by=request.user, updated_by=request.user, is_active=True, status='Pending')
                return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Successful Created")
            else:
                return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Unsuccessful!")
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))


class PrepaymentUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            prepayment = get_object_or_404(Prepayment, pk=pk, is_active=True)
            serializer = PrepaymentUpdateSerializer(prepayment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Record updated")
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, serializer.errors)
        except ValidationError as e:
            return CommonResponse("error", {}, status.HTTP_400_BAD_REQUEST, str(e))
        except Exception as e:
            return CommonResponse("error", {}, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


class PrepaymentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            prepayment = get_object_or_404(Prepayment, pk=pk)
            prepayment.soft_delete()

            return CommonResponse("success", [], status.HTTP_200_OK, "Successfully deleted!")
        except Prepayment.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found!")
        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Record not found")
