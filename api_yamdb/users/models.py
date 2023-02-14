from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models

from .validators import not_me_username_validator


class User(AbstractUser):

    ROLE_CHOICES = (
        ("USER", "user"),
        ("MODERATOR", "moderator"),
        ("ADMIN", "admin"),
    )
    username_validator = UnicodeUsernameValidator()

    bio = models.TextField(
        "Биография", blank=True, help_text="Здесь напишите о себе"
    )
    confirmation_code = models.PositiveIntegerField(
        "Код подтверждения", blank=True, null=True
    )
    email = models.EmailField(
        "Адрес эл. почты",
        blank=False,
        unique=True,
        help_text="Введите адрес электронной почты",
    )
    role = models.CharField(
        "Роль пользователя",
        choices=ROLE_CHOICES,
        max_length=30,
        default="USER",
        help_text="Выберите роль пользователя",
    )
    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
        help_text="Введите имя пользователя",
        validators=[username_validator, not_me_username_validator],
    )

    def email_user(
        self,
        message,
        subject="Регистрация",
        from_email="yamdb@gmail.com",
        **kwargs
    ):
        send_mail(subject, message, from_email, [self.email], **kwargs)

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
