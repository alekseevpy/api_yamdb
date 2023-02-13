from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("USER", "user"),
        ("MODERATOR", "moderator"),
        ("ADMIN", "admin"),
        ("SUPERUSER", "superuser"),
    )

    bio = models.TextField(
        "Биография", blank=True, help_text="Здесь напишите о себе"
    )
    confirmation_code = models.PositiveIntegerField(
        "Код подтверждения", blank=True, null=True
    )
    email = models.EmailField("Адрес эл. почты", blank=False, unique=True)
    role = models.CharField(
        "Роль пользователя",
        choices=ROLE_CHOICES,
        max_length=30,
        default="USER",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        if self.role == "MODERATOR":
            self.is_staff = True
        if self.role == "ADMIN":
            self.is_superuser = True
        super().save(*args, **kwargs)
