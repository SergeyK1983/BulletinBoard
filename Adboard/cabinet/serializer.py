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

