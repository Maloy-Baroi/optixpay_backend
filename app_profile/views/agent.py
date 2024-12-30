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
from utils.common_response import CommonResponse


class AgentDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            agent_id = request.query_params.get('agent_id')
            search_query = request.query_params.get('search_query')
            if agent_id:
                agent = AgentProfile.objects.get(id=agent_id)
                agent_serializer = AgentProfileSerializer(agent)
                return CommonResponse("success", agent_serializer.data, status.HTTP_200_OK)
            elif search_query:
                agents = AgentProfile.objects.filter(
                    Q(name__icontains=search_query) | Q(unique_id__icontains=search_query)
                )
                agents_serializer = AgentProfileSerializer(agents, many=True)
                return CommonResponse("success", agents_serializer.data, status.HTTP_200_OK)
            else:
                agents = AgentProfile.objects.all()
                agents_serializer = AgentProfileSerializer(agents, many=True)
                return CommonResponse("success", agents_serializer.data, status.HTTP_200_OK)
        except AgentProfile.DoesNotExist:
            return CommonResponse("error", "Agent not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return CommonResponse("error", str(e), status.HTTP_400_BAD_REQUEST, "Agent data couldn't be retrieved")

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
            return Response({'message': 'AgentProfile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentProfileSerializer(agent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentProfileDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            agent = AgentProfile.objects.get(pk=pk)
        except AgentProfile.DoesNotExist:
            return Response({'message': 'AgentProfile not found'}, status=status.HTTP_404_NOT_FOUND)

        agent.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
