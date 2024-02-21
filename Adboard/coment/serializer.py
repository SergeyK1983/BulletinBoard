from rest_framework import serializers

from announcement.models import Post
from cabinet.models import User
from .models import CommentaryToAuthor


def validate_queryset_to_post(self):
    """
    Проверка, что запись действительно существует перед выдачей экземпляра
    """
    if not Post.objects.filter(pk=self._context['kwargs']['pk']).exists():
        raise serializers.ValidationError({"Detail": "Такой публикации нет ..."})
    instance = Post.objects.get(pk=self._context['kwargs']['pk'])
    return instance


class CommentSerializer(serializers.ModelSerializer):
    """
    Создание комментариев
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CommentaryToAuthor
        fields = (
            'author',
            'to_post',
            'comment',
        )

    def create(self, validated_data):
        validated_data.update({'author': User.objects.get(username=self._context['request'].user.username)})
        validated_data.update({'to_post': validate_queryset_to_post(self)})
        instance = CommentaryToAuthor.objects.create(**validated_data)
        return instance

