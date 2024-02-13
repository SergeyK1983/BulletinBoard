import secrets
import string
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status

from Adboard.settings import LOGIN_URL, SERVER_EMAIL, SERG_USER_CONFIRMATION_KEY, SERG_USER_CONFIRMATION_TIMEOUT

from .forms import LoginUserForm, RegisterUserForm, UpdateUserForm
from .models import User
from announcement.models import Post
from .serializer import UserSerializer, UserArticleSerializer, ProfileSerializer
from .services import get_username, return_response


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

        # if request.headers.get('Content-Type') == 'application/json':
        # return self.list(request, *args, **kwargs)
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
