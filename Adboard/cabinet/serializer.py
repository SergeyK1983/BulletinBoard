from dj_rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import gettext_lazy
from rest_framework import serializers

from announcement.models import Post, Category
from .models import User
from .services import get_queryset_filter


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

    # author = AuthorSerializer()
    category = CategorySerializer()

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
    """ Данные авторов """

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


class UserProfileSerializer(AuthorSerializer):
    """ Для просмотра страницы пользователя """

    posts = serializers.SerializerMethodField("get_posts")

    class Meta(AuthorSerializer.Meta):
        model = User
        fields = AuthorSerializer.Meta.fields.copy()
        fields.append('posts')

    def get_posts(self, instance):
        author = self.context['request'].user.username
        date_after = self.context['request'].query_params.get('date_after', None)
        date_before = self.context['request'].query_params.get('date_before', None)
        category = self.context['request'].query_params.get('category', None)
        if not any([date_after, date_before, category]):
            queryset = Post.objects.filter(author=author)
        else:
            queryset = get_queryset_filter(author, date_after, date_before, category)
        return ProfileSerializer(queryset.order_by('-date_create'), many=True).data


class UserArticleSerializer(AuthorSerializer):
    """ Для просмотра публикации со страницы пользователя """

    post = serializers.SerializerMethodField("get_post")

    class Meta:
        model = User
        fields = AuthorSerializer.Meta.fields.copy()
        fields.append('post')

    def get_post(self, instance):
        id_post = self.context['view'].kwargs['id']
        queryset = instance.posts.filter(id=id_post)
        return ProfileSerializer(queryset, many=True).data


class UserUpdateSerializer(AuthorSerializer):
    """ Изменение данных пользователя """

    class Meta(AuthorSerializer.Meta):
        fields = AuthorSerializer.Meta.fields.copy()
        fields.remove('id')

    def validate_email(self, email):
        if self.context['request'].user.email != email:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(gettext_lazy("Такой email уже существует"), )
        return email

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.date_birth = validated_data.get('date_birth', instance.date_birth)

        instance.save()
        return instance


class UserRegisterSerializer(RegisterSerializer):
    """ Регистрация пользователя """

    username = serializers.CharField(
        min_length=4,
        max_length=100,
        write_only=True,
        label="Логин",
        required=True
    )
    email = serializers.CharField(
        max_length=100,
        style={'input_type': 'email'},
        write_only=True,
        label="Почта",
        required=True
    )
    password1 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Пароль",
        required=True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Повтор пароля",
        required=True
    )

    def validate_email(self, email):
        super().validate_email(email)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(gettext_lazy("Такой email уже существует"), )
        return email

