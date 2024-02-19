from rest_framework.response import Response


def return_response(request, data, status, template):
    """
    Используется в views.py: ProfileDetail, ProfileArticleDetail при проверке корректности запроса.
    Возвращает ответ в зависимости от формата запроса
    """

    if request.headers.get('Content-Type') == 'application/json':
        return Response(data=data, status=status)
    return Response({'error': data}, template_name=template)

