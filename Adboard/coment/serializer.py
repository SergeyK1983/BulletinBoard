from rest_framework import serializers

from announcement.models import Post
from cabinet.models import User
from .models import CommentaryToAuthor


class CommentToPost:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_post(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post


def queryset_to_post(self, value):
    print("value= ", value)
    if value == Post.objects.all():
        value = Post.objects.get(pk=self._context['kwargs']['pk'])
    else:
        raise serializers.ValidationError("Blog post is not about Django")
    return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Создание комментариев
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print("fields=> ", self.fields)
        # print("queryset=> ", Post.objects.get(pk=self._context['kwargs']['pk']))
        # print('serializer_context=> ', self._context)
        print("поле = ", self.fields['to_post'])

        # self.fields['to_post'].queryset = Post.objects.get(pk=self._context['kwargs']['pk'])

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # to_post = serializers.HiddenField(default=CommentToPost().get_post())
    # to_post = serializers.SlugRelatedField(slug_field='title', read_only=True)  # default=Post.objects.get(pk=2)

    class Meta:
        model = CommentaryToAuthor
        fields = (
            'author',
            'to_post',
            'comment',
        )
        # read_only_fields = ['author', 'to_post']
        extra_kwargs = {
            'to_post': {'validators': [queryset_to_post]},
        }

    def create(self, validated_data):
        validated_data.update({'author': User.objects.get(username=self._context['request'].user.username)})
        validated_data.update({'to_post': Post.objects.get(pk=self._context['kwargs']['pk'])})
        instance = CommentaryToAuthor(
            author=validated_data['author'],
            to_post=validated_data['to_post'],
            comment=validated_data['comment'],
        )
        instance.save()
        return instance

