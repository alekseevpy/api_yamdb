from datetime import datetime as dt
from random import randint

from django.contrib.auth import get_user_model

from .constants import CONF_CODE_DIGITS_QUANTITY, CONF_CODE_MAX, CONF_CODE_MIN


User = get_user_model()


def generate_confirmation_code(
    min_val: int, max_val: int, digits_quantity: int
) -> str:
    """Генерирует строку со случайным кодом.
    От min_val до max_val и длиной digits_quantity.
    """
    return "".join(
        map(str, (randint(min_val, max_val) for _ in range(digits_quantity)))
    )


def send_confirmation_code(user: User) -> str:
    """Посылает письмо с кодом подтверждения на эл. почту Пользователя.
    Возвращает строку с кодом подтверждения.
    """
    confirmation_code = generate_confirmation_code(
        CONF_CODE_MIN, CONF_CODE_MAX, CONF_CODE_DIGITS_QUANTITY
    )
    email_message = (
        "Вы получили это письмо, потому что пытались зарегистрироваться \n"
        "или обновить токен на ресурсе YamDB.\n"
        "Подтвердите свой аккаунт и получите максимум от YamDB везде, \n"
        "где бы вы не вошли:\n"
        f"Ваше имя пользователя: {user.username}\n"
        "Используйте этот код подтверждения:\n"
        f"{confirmation_code}"
    )
    user.email_user(email_message)
    return confirmation_code
