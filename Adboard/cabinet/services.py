from rest_framework.response import Response

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


def return_response(request, data, status, template):
    """
    Используется в views.py: ProfileDetail, ProfileArticleDetail при проверке корректности запроса.
    Возвращает ответ в зависимости от формата запроса
    """

    if request.headers.get('Content-Type') == 'application/json':
        return Response(data=data, status=status)
    return Response({'error': data}, template_name=template)

