from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer

User = get_user_model()


class SignUpView(APIView):
    permission_classes = []


class GetTokenView(APIView):
    def post(self, request):
        pass
