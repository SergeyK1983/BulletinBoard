from rest_framework import serializers

from announcement.models import Post


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
