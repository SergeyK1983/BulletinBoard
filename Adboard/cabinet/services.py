from datetime import datetime

from django.utils.translation import gettext_lazy
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from announcement.models import Post


class DateFilterException(APIException):
    @staticmethod
    def get_check_input_date(date):
        """ Проверка даты на входе get_queryset_filter() """

        format_date = "%Y-%m-%d"
        try:
            datetime.strptime(date, format_date)
        except ValueError:
            raise ValidationError(gettext_lazy(f"Значение {date} имеет неверный формат даты"))


def return_response(request, data, status, template):
    """
    Используется в views.py: ProfileDetail, ProfileArticleDetail при проверке корректности запроса.
    Возвращает ответ в зависимости от формата запроса
    """

    if request.headers.get('Content-Type') == 'application/json':
        return Response(data=data, status=status)
    return Response({'error': data}, template_name=template)


def get_queryset_filter(author, date_after=None, date_before=None, category=None):
    """
    Фильтрация объявлений на странице пользователя (по другому не вышло фильтровать)
    Используется в serializer.py: UserSerializer
    Возвращает фильтрованный queryset
    """
    args_list = [category, date_before, date_after]

    if date_after:
        DateFilterException.get_check_input_date(date_after)
    if date_before:
        DateFilterException.get_check_input_date(date_before)

    choice = [
        {1: Post.objects.filter(
            author=author,
            date_create__date__gte=date_after) if date_after else None},
        {2: Post.objects.filter(
            author=author,
            date_create__date__lte=date_before) if date_before else None},
        {3: Post.objects.filter(
            author=author,
            date_create__date__gte=date_after,
            date_create__date__lte=date_before) if date_after and date_before else None},
        {4: Post.objects.filter(
            author=author,
            category=category) if category else None},
        {5: Post.objects.filter(
            author=author,
            category=category,
            date_create__date__gte=date_after) if category and date_after else None},
        {6: Post.objects.filter(
            author=author,
            category=category,
            date_create__date__lte=date_before) if category and date_before else None},
        {7: Post.objects.filter(
            author=author,
            category=category,
            date_create__date__gte=date_after,
            date_create__date__lte=date_before) if all(args_list) else None},
    ]

    binary_number = ''
    for i in args_list:
        binary_number += '1' if i else '0'

    binary_number = binary_number[::-1]  # чтобы число писалось слева направо
    decimal_number = int(binary_number[2]) * 2 ** 2 + int(binary_number[1]) * 2 ** 1 + int(binary_number[0]) * 2 ** 0

    try:
        queryset = [i.get(decimal_number) for i in choice if i.get(decimal_number, None)][0]
    except IndexError:
        return Post.objects.none()
    return queryset


def get_filter_posts_for_template(author, date_after=None, date_before=None, category=None):
    if not any([date_after, date_before, category]):
        queryset = Post.objects.filter(author=author)
    else:
        queryset = get_queryset_filter(author, date_after, date_before, category)
    return queryset.order_by('-date_create')
