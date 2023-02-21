from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title

from reviews.models import Comment, Review
from django.db.models import Avg

from users.constants import CONF_CODE_MAX_LEN, EMAIL_MAX_LEN, USERNAME_MAX_LEN
from users.validators import not_me_username_validator, username_validator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserProfileSerializer(UserSerializer):
    """Сериализатор модели User для профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LEN,
        required=True,
        validators=[not_me_username_validator, username_validator],
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LEN,
        required=True,
    )


class GetAuthTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LEN,
        required=True,
        validators=[not_me_username_validator, username_validator],
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=CONF_CODE_MAX_LEN
    )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title
    
    def get_rating(self, obj):
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        return obj['rating']
 

class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "author", "title", "text", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "author", "review", "text", "pub_date")
        read_only_fields = ("review",)
        model = Comment