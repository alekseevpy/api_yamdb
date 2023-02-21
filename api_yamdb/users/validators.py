from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

username_validator = UnicodeUsernameValidator()


def not_me_username_validator(value):
    if value == "me":
        raise ValidationError(
            "Вы не можете использовать 'me' в качестве username"
        )
