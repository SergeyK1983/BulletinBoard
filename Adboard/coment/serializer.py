from rest_framework import serializers

from announcement.models import Post
from cabinet.models import User
from .models import CommentaryToAuthor


def validate_queryset_to_post(self):
    """
    Проверка, что запись действительно существует перед выдачей экземпляра. Использовано в CommentSerializer.
    """
    if not Post.objects.filter(id=self._context['kwargs']['id']).exists():
        raise serializers.ValidationError({"Detail": "Такой публикации нет ..."})
    instance = Post.objects.get(id=self._context['kwargs']['id'])
    return instance


class CommentListSerializer(serializers.ModelSerializer):
    """ Список комментариев """

    class Meta:
        model = CommentaryToAuthor
        fields = ('author', 'to_post', 'comment', 'accepted', 'date_create')


class CommentSerializer(serializers.ModelSerializer):
    """ Создание комментариев """

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


class CommentAcceptedSerializer(serializers.ModelSerializer):
    """ Изменение статуса комментария на принято (accepted) """

    class Meta:
        model = CommentaryToAuthor
        fields = ('accepted', )

    def validate_accepted(self, value):
        if not value:
            raise serializers.ValidationError("Должен быть True")
        return value

    def update(self, instance, validated_data):
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.save()
        return instance


