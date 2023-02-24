from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.viewsets import ModelViewSet

from core.permissions import (
    IsAdminOrReadOnly,
    IsAuthorModeratorAdminOrReadOnly,
)
from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import GetListCreateDeleteMixin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleRetrieveSerializer,
    TitleWriteSerializer,
)


class ReviewViewSet(ModelViewSet):
    """
    Получить список всех отзывов.
    Добавление нового отзыва.
    Получение отзыва по id.
    Обновление отзыва по id.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    http_method_names = ("get", "post", "delete", "patch")

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    """
    Получить список всех комментариев.
    Добавление нового комментария к отзыву.
    Получить комментарий по id.
    Обновление комментария по id.
    Удаление комментария.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    http_method_names = ("get", "post", "delete", "patch")

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведения."""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ("get", "post", "delete", "patch")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleRetrieveSerializer
        return TitleWriteSerializer


class CategoryViewSet(GetListCreateDeleteMixin):
    """Вьюсет для категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(GetListCreateDeleteMixin):
    """Вьюсет для жанра."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
