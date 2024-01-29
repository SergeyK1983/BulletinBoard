import secrets
import string
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.fields import CurrentUserDefault
# from django_redis import cache
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.utils import json

from Adboard.settings import LOGIN_URL, SERVER_EMAIL, SERG_USER_CONFIRMATION_KEY, SERG_USER_CONFIRMATION_TIMEOUT
from coment.models import CommentaryToAuthor
from .forms import LoginUserForm, RegisterUserForm, UpdateUserForm
from .models import User
from announcement.models import Post
from .serializer import UserSerializer, UserArticleSerializer, ProfileSerializer
from .services import get_username


# if request.user.is_authenticated:
#     ...  # Do something for logged-in users.
# else:
#     ...  # Do something for anonymous users.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'cabinet/login.html'

    def get_success_url(self):
        return reverse_lazy('board_list')


class LogoutUser(LogoutView):
    def get_success_url(self):
        return reverse_lazy('board_list')


class RegisterUser(CreateView):
    """ Регистрация, создание пользователя """
    form_class = RegisterUserForm
    template_name = 'cabinet/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user, created = User.objects.get_or_create(email=form.cleaned_data['email'])
        new_pass = None
        # if created or user.is_active is False:
        if created:
            # на будущую доработку генерирую пароль
            alphabet = string.ascii_letters + string.digits
            new_pass = ''.join(secrets.choice(alphabet) for i in range(8))
            # user.set_password(new_pass)
            # user.save(update_fields=["password", ])

        # if new_pass or user.is_active is False:
        if new_pass:
            token = uuid.uuid4().hex
            redis_key = SERG_USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, {'user_id': user.id}, timeout=SERG_USER_CONFIRMATION_TIMEOUT)

            confirm_link = self.request.build_absolute_uri(
                reverse_lazy("login_confirm", kwargs={'token': token})
            )

        html_content = render_to_string(
            template_name='cabinet/email.html',
            context={
                'username': user.username,  # username не пришел, еще не существует
                'confirm_link': confirm_link,
                'password': new_pass,
            }
        )
        send_mail(
            subject='Доска объявлений',
            message='',
            from_email=SERVER_EMAIL,
            recipient_list=[user.email, ],
            html_message=html_content,
        )
        return super().form_valid(form)


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'cabinet/update.html'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        self.queryset = super().get_queryset()
        username = get_username(request=self.request)  # функция из cabinet.services.py
        queryset = User.objects.filter(username=username)
        return queryset

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.pk])


class ProfileDetail(generics.ListAPIView):
    """ Страница пользователя """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cabinet/profile_list.html"

    def get_queryset(self):
        # Нужно для нормального вывода в json формате
        queryset = User.objects.filter(username=self.request.user.username)  # User.objects.raw("SQL запрос")
        return queryset

    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            data = {'state': 0, 'message': 'Пользователя не существует'}
            # return Response(data=data, status=status.HTTP_200_OK)
            return HttpResponse(content=data['message'], status=status.HTTP_200_OK)

        if request.user != user:
            data = {"message": "Тут нет вашей страницы", }
            # return Response(data=data, status=status.HTTP_200_OK)
            return HttpResponse(content=data['message'], status=status.HTTP_200_OK)

        # нужно для TemplateHTMLRenderer:
        qs1 = User.objects.filter(username=self.request.user.username)
        qs2 = Post.objects.filter(author=self.request.user.username).order_by("-date_create")
        data = {'profile': qs1, 'posts': qs2}

        # можно и так, но фичи работать не будут:
        # serializer = UserSerializer(user)
        # j_data = json.dumps(serializer.data)
        # d_data = json.loads(j_data)

        # return self.list(request, *args, **kwargs)
        return Response(data=data, status=status.HTTP_200_OK)


# def get_mail(request):
#     # тут что-то
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # возвращает на ту же страницу


class ProfileArticleDetail(generics.ListAPIView):
    """ Страница просмотра конкретной публикации пользователя """

    serializer_class = UserArticleSerializer  # ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cabinet/profile_article.html"

    def get_queryset(self, **kwargs):
        queryset = Post.objects.filter(id=self.kwargs['id'])
        return queryset

    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.get(username=kwargs['username'])
        except ObjectDoesNotExist:
            data = {'state': 0, 'message': 'Пользователя не существует'}
            # return Response(data=data, status=status.HTTP_200_OK)
            return HttpResponse(content=data['message'], status=status.HTTP_200_OK)

        if request.user != user:
            data = {"message": "Тут нет вашей страницы", }
            # return Response(data=data, status=status.HTTP_200_OK)
            return HttpResponse(content=data['message'], status=status.HTTP_200_OK)

        # нужно для TemplateHTMLRenderer:
        qs1 = User.objects.filter(username=self.request.user.username)
        qs2 = Post.objects.filter(id=self.kwargs['id'])
        data = {'profile': qs1, 'posts': qs2}

        # return self.list(request, *args, **kwargs)
        return Response(data=data, status=status.HTTP_200_OK)
