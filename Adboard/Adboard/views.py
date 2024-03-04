from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render


def index(request):
    return render(request, template_name='index.html')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1 align="center"> Ошибка 404 <br> Страница не найдена </h1>')


def server_error(exception):
    return HttpResponseServerError('<h1 align="center"> Ошибка 500 <br> Ошибка сервера. Мы всё исправим! </h1>')
