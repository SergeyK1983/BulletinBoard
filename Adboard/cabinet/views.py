import json
import secrets
import string
import uuid
import re
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate

from rest_framework.exceptions import APIException

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView, LogoutView

from Adboard.settings import LOGIN_URL, SERVER_EMAIL, SERG_USER_CONFIRMATION_KEY, SERG_USER_CONFIRMATION_TIMEOUT

from .forms import LoginUserForm, RegisterUserForm, UpdateUserForm
from .models import User
from announcement.models import Post
from .serializer import UserSerializer, UserArticleSerializer, ProfileSerializer, UserRegisterSerializer

from .services import get_username, return_response


class RegisterUser(APIView):
    """ Регистрация """

    serializer_class = UserRegisterSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/register.html"

    def get(self, request):
        form = RegisterUserForm()
        serializer = self.serializer_class()
        data = serializer.data
        data.update({'content-type': 'multipart/form-data'})
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data=data, status=status.HTTP_200_OK)
        return Response({"form": form})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST, context={'request': request})
        form = RegisterUserForm(request.POST)
        header = re.compile(r"^multipart/form-data")  # проверяю сначала строки

        if serializer.is_valid():
            user = serializer.save(request)
            data = {'id': user.id, 'username': user.username, 'email': user.email}
            if header.search(request.headers.get('Content-Type')):
                return Response(data=data, status=status.HTTP_201_CREATED)
            return redirect('login')

        if header.search(request.headers.get('Content-Type')):
            return Response(data={'error': 'не верно введены данные', 'invalid': serializer.errors},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"form": form})
        # TODO обработать другие форматы на предмет не верного обращения, чтобы не было ошибки сервера


class LoginUser(LoginView):
    """ Аутентификация """

    serializer_class = LoginSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/login.html"

    def get(self, request):
        serializer = self.serializer_class()
        form = LoginUserForm()
        data = serializer.data
        data.update({'content-type': 'multipart/form-data'})
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data=data, status=status.HTTP_200_OK)
        return Response({"form": form})

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        header = re.compile(r"^multipart/form-data")

        if header.search(request.headers.get('Content-Type')):
            return self.get_response()
        return redirect('board_list')
    # TODO доработать дружелюбие формы на предмет неверного ввода


class LogoutUser(LogoutView):
    """  Выход """

    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/logout.html"

    def get(self, request, *args, **kwargs):
        return Response(template_name="cabinet/logout.html")

    def post(self, request, *args, **kwargs):
        if request.headers.get('Content-Type') == 'application/json':
            return self.logout(request)
        else:
            django_logout(request)
            return redirect('board_list')


class DestroyUserView(generics.DestroyAPIView):
    """ Удаление пользователя """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/destroy_user.html"

    def get(self, request, *args, **kwargs):
        user = self.get_queryset().filter(username=request.user.username)
        data = {'profile': user}
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'msg': 'Удаление аккаунта', 'method': 'POST'}, status=status.HTTP_200_OK)
        return Response(data=data)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(User, username=request.user.username)
        self.perform_destroy(instance)
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'status': 'Аккаунт пользователя удален'}, status=status.HTTP_204_NO_CONTENT)
        return redirect('board_list')

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = UserListFilter
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/profile_list.html"

    def get_queryset(self):
        # Нужно для нормального вывода в json формате
        queryset = User.objects.filter(username=self.request.user.username)  # User.objects.raw("SQL запрос")
        return queryset

    def get(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            data = {'error': 'Пользователя не существует', 'status': 'HTTP_200_OK'}
            if request.headers.get('Content-Type') == 'application/json':
                return Response(data=data, status=status.HTTP_200_OK)
            return Response({'error': data}, template_name='announcement/page_error.html')

        if request.user != user:
            data = {"error": "Тут нет вашей страницы", 'status': 'HTTP_200_OK'}
            if request.headers.get('Content-Type') == 'application/json':
                return Response(data=data, status=status.HTTP_200_OK)
            return Response({'error': data}, template_name='announcement/page_error.html')

        # нужно для TemplateHTMLRenderer:
        user_qs = User.objects.filter(username=self.request.user.username)
        posts = Post.objects.filter(author=self.request.user.username).order_by("-date_create")
        # posts_filter = self.filterset_class(self.request.GET, posts)
        # print('фильтр', posts_filter.qs)
        data = {'profile': user_qs, 'posts': posts}

        # можно и так, но фичи работать не будут:
        # serializer = UserSerializer(user)
        # j_data = json.dumps(serializer.data)
        # d_data = json.loads(j_data)

        if request.headers.get('Content-Type') == 'application/json':
            return self.list(request, *args, **kwargs)
        return Response(data=data, status=status.HTTP_200_OK)


class ProfileArticleDetail(generics.ListAPIView):
    """ Страница просмотра конкретной публикации пользователя """

    serializer_class = UserArticleSerializer
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
            data = {'error': 'Пользователя не существует', 'status': 'HTTP_200_OK'}
            return return_response(request=request, data=data, status=status.HTTP_200_OK,
                                   template='announcement/page_error.html')

        if request.user != user:
            data = {"error": "Тут нет вашей страницы", 'status': 'HTTP_200_OK'}
            return return_response(request=request, data=data, status=status.HTTP_200_OK,
                                   template='announcement/page_error.html')
        elif not list(self.get_queryset()):
            data = {"error": "Такой записи нет", 'status': 'HTTP_200_OK'}
            return return_response(request=request, data=data, status=status.HTTP_200_OK,
                                   template='announcement/page_error.html')

        user_qs = User.objects.filter(username=self.request.user.username)
        posts = Post.objects.filter(id=self.kwargs['id'])
        data = {'profile': user_qs, 'posts': posts}

        if request.headers.get('Content-Type') == 'application/json':
            return self.list(request, *args, **kwargs)
        return Response(data=data, status=status.HTTP_200_OK)
