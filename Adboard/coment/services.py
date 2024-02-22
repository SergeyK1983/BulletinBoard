from rest_framework import generics, status
from rest_framework.response import Response

from announcement.models import Post
from cabinet.models import User


def return_response(request, data, status, template):
    """ Возвращает ответ в зависимости от формата запроса """

    if request.headers.get('Content-Type') == 'application/json':
        return Response(data=data, status=status)
    return Response({'error': data}, template_name=template)


def get_check_user(request, **kwargs):
    """
    Не используется.
    Проверка username в url
    Не возвращает 'announcement/page_error.html' не понятно почему
    """
    user = generics.get_object_or_404(User, username=kwargs['username'])
    if request.user != user:
        data = {"error": "Тут нет вашей страницы", 'status': 'HTTP_204_NO_CONTENT'}
        return return_response(request=request, data=data, status=status.HTTP_204_NO_CONTENT,
                               template='announcement/page_error.html')
    return True


def get_check_post_pk(request, **kwargs):
    """ Такая же фигня """

    if not Post.objects.filter(pk=kwargs['pk']).exists():
        data = {"error": "Такой публикации нет ...", 'status': 'HTTP_204_NO_CONTENT'}
        return return_response(request=request, data=data, status=status.HTTP_204_NO_CONTENT,
                               template='announcement/page_error.html')
    return True
