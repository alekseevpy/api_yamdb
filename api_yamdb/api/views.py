from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOnly
from .registration.confirmation import send_confirmation_code
from .registration.token_generator import get_token_for_user
from .serializers import (
    GetAuthTokenSerializer,
    SignUpSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Вьюсет модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


class SignUpView(APIView):
    """CBV для регистрации пользователя и получения кода на почту."""

    permission_classes = []

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            user, _ = User.objects.get_or_create(
                username=username, email=email
            )
            user.confirmation_code = send_confirmation_code(user)
            user.save()
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthTokenView(APIView):
    """CBV для получения и обновления токена."""

    permission_classes = []

    def post(self, request):
        serializer = GetAuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {"confirmation_code": ["Неверный код подтверждения"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(get_token_for_user(user), status=status.HTTP_200_OK)
