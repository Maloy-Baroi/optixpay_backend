from django.db import transaction
from django.db.models import Q
from pycparser.plyparser import Coord
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_auth.models import CustomUser
from app_profile.models.agent import AgentProfile
from app_profile.serializers.agent import AgentProfileSerializer
from services.pagination import CustomPagination
from utils.common_response import CommonResponse


class AgentDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self, request):
        try:
            # Extract query parameters
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', self.pagination_class.page_size)
            search_query = request.query_params.get('search', '')
            agent_id = request.query_params.get('agent_id', None)
            search_status = request.query_params.get('status', '')
            bank = request.query_params.get('bank', '')

            # Build queryset
            agents = AgentProfile.objects.all()

            if agent_id:
                try:
                    agent = AgentProfile.objects.get(id=agent_id)
                    agent_serializers = AgentProfileSerializer(agent)
                    return CommonResponse(
                        "success", agent_serializers.data, status.HTTP_200_OK, "Data Found!"
                    )
                except AgentProfile.DoesNotExist:
                    return CommonResponse("error", "Agent not found", status.HTTP_404_NOT_FOUND)

            if search_query:
                agents = agents.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
            if search_status:
                agents = agents.filter(status=search_status)
            if bank:
                agents = agents.filter(bank__icontains=bank)

            # Apply pagination
            paginator = self.pagination_class()
            paginator.page_size = int(page_size)  # Override page size if provided
            result_page = paginator.paginate_queryset(agents, request)

            if result_page is not None:
                agents_serializers = AgentProfileSerializer(result_page, many=True)
                return paginator.get_paginated_response(agents_serializers.data)
            else:
                return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "No agents available")

        except AgentProfile.DoesNotExist:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Agent not found")
        except Exception as e:
            return CommonResponse("error", [], status.HTTP_204_NO_CONTENT, "Agent not found")


class AgentProfileCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            with transaction.atomic():
                email = request.data.get('email')
                password = request.data.get('password', "123456")
                username = request.data.get('username')
                users = CustomUser.objects.filter(Q(email=email) | Q(username=username))

                if users.exists():
                    return CommonResponse("error", {},
                                          status.HTTP_400_BAD_REQUEST, "Username or email already exists")

                # Create the user object
                user = CustomUser(email=email, username=username)
                user.set_password(password)
                user.save()
                serializer = AgentProfileSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=user, created_by=user, updated_by=user)
                    return CommonResponse("success", serializer.data, status.HTTP_201_CREATED, "Successfully Created")
                else:
                    return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, "Unsuccessfully")
        except Exception as e:
            return CommonResponse("error", str(e), status=status.HTTP_400_BAD_REQUEST)


class AgentProfileUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            agent = AgentProfile.objects.get(pk=pk)
        except AgentProfile.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, "AgentProfile not found")

        serializer = AgentProfileSerializer(agent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CommonResponse("success", serializer.data, status.HTTP_200_OK, "Successfully Updated")
        return CommonResponse("error", serializer.errors, status.HTTP_400_BAD_REQUEST, serializer.errors)


class AgentProfileDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            agent = AgentProfile.objects.get(id=pk)
            agent.soft_delete()
            return CommonResponse("success", {}, status.HTTP_200_OK, "Content Not Found!")
        except AgentProfile.DoesNotExist:
            return CommonResponse("error", {}, status.HTTP_404_NOT_FOUND, 'AgentProfile not found!')
