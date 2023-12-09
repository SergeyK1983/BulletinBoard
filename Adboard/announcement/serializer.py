from rest_framework import serializers

from announcement.models import Post


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'author',
            'category',
            'title',
            'article',
            'images',
            'files'
        )
