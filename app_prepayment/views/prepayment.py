from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app_prepayment.models.prepayment import Prepayment
from app_prepayment.serializers.prepayment import PrepaymentSerializer, PrepaymentUpdateSerializer
from app_profile.models.agent import AgentProfile
from services.pagination import CustomPagination
from utils.common_response import CommonResponse

import hashlib
import hmac
import json

# Shared secret key (ensure this is securely managed, not hard-coded in production)
SECRET_KEY = 'ebb620-d11037-56c184-d69d9e-f04a7'

# Assuming SECRET_KEY and other constants are defined and imported correctly
class WebhookAPIView(APIView):
    """
    Handle webhook calls with signature verification.
    """
    permission_classes = [AllowAny]  # This allows the endpoint to be accessed without authentication

    def post(self, request):
        try:
            received_signature = request.headers.get('x-signature', '')
            print("Received Signature: ", received_signature)
            request_body = request.body.decode('utf-8')
            print("Request Body: ", request_body)
            platform_id = '1333'
            signature_contract = f'{platform_id};{request_body};{SECRET_KEY}'
            signature = hmac.new(SECRET_KEY.encode(), signature_contract.encode(), hashlib.sha256).hexdigest()
            print("Generated Signature: ", signature)

            data = request.data

            try:
                agent = AgentProfile.objects.get(id=int(data.get('orderId')))
            except AgentProfile.DoesNotExist:
                return Response({"error": "AgentProfile not found"}, status=status.HTTP_404_NOT_FOUND)

            prepayment = Prepayment(
                agent_id=agent,
                transaction_hash=data.get('txhash'),
                amount_usdt=data.get('amount'),
                sender_address=data.get('addressFrom'),
                receiver_address=data.get('addressTo'),
                platform_id=data.get('platformId'),
                payment_id=data.get('paymentId'),
                exchange_rate=120.87,
                converted_amount=120.87 * float(data.get('amount')),
                status='Pending',
                created_by=agent.user,
                updated_by=agent.user
            )
            prepayment.save()

            return Response({"status": "success", "message": "Data received and verified"}, status=status.HTTP_200_OK)

            # if hmac.compare_digest(received_signature, signature):
            #
            # else:
            #     return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "Unknown error", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
                    return CommonResponse("error", {}, status.HTTP_204_NO_CONTENT, "Record not found")

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
