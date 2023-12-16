from rest_framework import serializers

from announcement.models import Post, Category


class BoardSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

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


class BoardPageSerializer(serializers.ModelSerializer):
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


class BoardPageCreateSerializer(serializers.ModelSerializer):
    # в поле автора подставляет текущего зарегистрированного пользователя
    # поле автора в запросе не отображает
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Глючит, не соображает какую категорию взять
    # CATEGORY = Category.CATEGORY
    # category = serializers.ChoiceField(choices=CATEGORY, label="Категория")

    class Meta:
        model = Post
        fields = (
            'author',
            'category',
            'title',
            'article',
            'images',
            'files',
        )
