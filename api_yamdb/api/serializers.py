from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, Serializer

User = get_user_model()


class SignUpSerializer(Serializer):
    class Meta:
        pass
