from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from announcement.models import Post, Category
from .models import User


class CategorySerializer(serializers.ModelSerializer):
    """ Категории публикаций """
    class Meta:
        model = Category
        fields = ('categories', )
        extra_kwargs = {
            'categories': {'choices': Category.Categories.labels, },
        }


class ProfileSerializer(serializers.ModelSerializer):
    """ Публикации авторов """
    category = CategorySerializer(label="Категории")

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'category',
            'title',
            'article',
            'images',
            'files',
            'date_create'
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'photo',
            'date_birth',
        ]


class UserSerializer(AuthorSerializer):
    """ Для просмотра страницы пользователя """
    posts = ProfileSerializer(many=True, read_only=True)

    class Meta(AuthorSerializer.Meta):
        model = User
        AuthorSerializer.Meta.fields.append('posts')


class UserArticleSerializer(ProfileSerializer):
    """ Для просмотра публикации со страницы пользователя """
    author = AuthorSerializer()


class UserRegisterSerializer(RegisterSerializer):
    """ Регистрация пользователя """
    username = serializers.CharField(min_length=4, max_length=100, write_only=True, label="Логин", required=True)
    email = serializers.CharField(max_length=100, style={'input_type': 'email'}, write_only=True, label="Почта",
                                  required=True)
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label="Пароль", required=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, label="Повтор пароля",
                                      required=True)


class UserLoginSerializer(LoginSerializer):
    username = serializers.CharField(max_length=100, write_only=True, label="Логин", required=True)
    email = serializers.CharField(max_length=100, style={'input_type': 'email'}, write_only=True, label="Почта",
                                  required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label="Пароль", required=True)


