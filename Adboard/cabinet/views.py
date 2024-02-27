import re

from django.contrib.auth import logout as django_logout
from django.db.models import Q
from django.utils.translation import gettext_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from dj_rest_auth.serializers import LoginSerializer

from .filters import PostsListFilter, UserListFilter
from .forms import LoginUserForm, RegisterUserForm, UpdateUserForm
from .models import User
from announcement.models import Post
from .serializer import UserArticleSerializer, UserRegisterSerializer, UserUpdateSerializer, \
    UserProfileSerializer
from .services import return_response


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
        instance = generics.get_object_or_404(User, username=request.user.username)
        self.perform_destroy(instance)
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'status': 'Аккаунт пользователя удален'}, status=status.HTTP_204_NO_CONTENT)
        return redirect('board_list')

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """ Изменение данных пользователя """

    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/update.html"

    def get_queryset(self):
        queryset = User.objects.filter(username=self.request.user.username)
        return queryset

    def get(self, request, *args, **kwargs):
        user = self.get_queryset()
        serializer = self.serializer_class(user[0])
        initial = {
            "username": user[0].username,
            "first_name": user[0].first_name,
            "last_name": user[0].last_name,
            "email": user[0].email,
            "photo": user[0].photo,
            "date_birth": user[0].date_birth,
        }
        form = UpdateUserForm(initial=initial)
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'data': serializer.data, 'content-type': 'multipart/form-data'},
                            status=status.HTTP_200_OK)
        return Response({"profile": user, "form": form})

    def post(self, request, *args, **kwargs):
        data = request.data
        instance = generics.get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class(instance=instance, data=data, context={'request': request})
        header = re.compile(r"^multipart/form-data")

        if not serializer.is_valid():
            data = {'error': 'Не корректные данные ...', 'detail': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': data}, template_name='announcement/page_error.html')
        if serializer.is_valid():
            try:
                serializer.save()
                if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                    data = {'state': 1, 'message': 'Изменение прошло успешно'}
                    return Response(data, status=status.HTTP_200_OK)
                return redirect('profile', request.user.id)
            except APIException:
                data = {'error': 'Сервер не отвечает.', 'status': 'HTTP_500_INTERNAL_SERVER_ERROR'}
                if header.search(request.headers.get('Content-Type')) and data.get('mark') is None:
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'error': data}, template_name='announcement/page_error.html')

            # TODO обработать другие форматы на предмет не верного обращения, чтобы не было ошибки сервера


class UserPasswordChange(PasswordChangeView):
    """ Изменение пароля """

    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/password_change.html"

    def get(self, request, *args, **kwargs):
        user = generics.get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class()
        form = serializer.set_password_form_class(user)
        if request.headers.get('Content-Type') == 'application/json':
            return Response(data={'data': serializer.data, 'content-type': 'application/json'},
                            status=status.HTTP_200_OK)
        return Response({"form": form})

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if request.headers.get('Content-Type') == 'application/json':
            return Response({'detail': gettext_lazy('New password has been saved.')})
        return redirect('user-update')


class ProfileDetail(generics.ListAPIView):
    """ Страница пользователя """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = UserListFilter
    # renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = "cabinet/profile_list.html"

    def get_queryset(self):
        queryset = User.objects.filter(username=self.request.user.username)
        return queryset

    # def get(self, request, *args, **kwargs):
    #
    #     try:
    #         user = User.objects.get(id=kwargs['id'])
    #     except ObjectDoesNotExist:
    #         data = {'error': 'Пользователя не существует', 'status': 'HTTP_200_OK'}
    #         if request.headers.get('Content-Type') == 'application/json':
    #             return Response(data=data, status=status.HTTP_200_OK)
    #         return Response({'error': data}, template_name='announcement/page_error.html')
    #
    #     if request.user != user:
    #         data = {"error": "Тут нет вашей страницы", 'status': 'HTTP_200_OK'}
    #         if request.headers.get('Content-Type') == 'application/json':
    #             return Response(data=data, status=status.HTTP_200_OK)
    #         return Response({'error': data}, template_name='announcement/page_error.html')
    #
    #     # нужно для TemplateHTMLRenderer:
    #     user_qs = User.objects.filter(username=self.request.user.username)
    #     posts = Post.objects.filter(author=self.request.user.username).order_by("-date_create")
    #     # posts_filter = self.filterset_class(self.request.GET, posts)
    #     # print('фильтр', posts_filter.qs)
    #     data = {'profile': user_qs, 'posts': posts}
    #
    #     if request.headers.get('Content-Type') == 'application/json':
    #         return self.list(request, *args, **kwargs)
    #     return Response(data=data, status=status.HTTP_200_OK)


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
