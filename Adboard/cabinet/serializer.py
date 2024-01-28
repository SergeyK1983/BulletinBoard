from rest_framework import serializers, request
from rest_framework.request import Request

from announcement.models import Post, Category
from .models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('categories', )
        extra_kwargs = {
            'categories': {'choices': Category.Categories.labels, },
        }


class ProfileSerializer(serializers.ModelSerializer):
    # author = UserSerializer(label='Автор')
    category = CategorySerializer(label="Категории")

    class Meta:
        model = Post
        fields = (
            'author',
            'category',
            'title',
            'article',
            'images',
            'files',
            'date_create'
        )


class UserSerializer(serializers.ModelSerializer):
    # request = Request(request)
    posts = ProfileSerializer(many=True, read_only=True)
    # posts = serializers.RelatedField(queryset=User.objects.get(username=request.user.username).posts.all(), many=True, read_only=True)

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
            'posts',
        ]
