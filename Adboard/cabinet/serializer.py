from rest_framework import serializers

from announcement.models import Post
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
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
