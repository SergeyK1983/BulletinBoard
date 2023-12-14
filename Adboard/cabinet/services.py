from .models import User


class UsernameNotExistsException(Exception):

    def __str__(self):
        return f"Нет пользователя с таким username"


def get_username(request):
    """
    Используется в ProfileDetail для получения username пользователя выполнившего вход, чтобы ограничить доступ
    к приватным страницам других пользователей.
    Возвращает имя пользователя.
    """
    try:
        username = User.get_username(self=request.user)
        return username
    except UsernameNotExistsException:
        return None
