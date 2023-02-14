from django.core.exceptions import ValidationError


def not_me_username_validator(value):
    if value == "me":
        raise ValidationError(
            "Вы не можете использовать 'me' в качестве username"
        )
