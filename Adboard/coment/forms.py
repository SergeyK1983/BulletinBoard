from urllib import request

from django import forms

from cabinet.models import User
# from django.http import request, HttpRequest

from .models import CommentaryToAuthor


class CommentCreateForm(forms.ModelForm):
    user = User.objects.filter(pk=2)
    title = 'Заголовок'
    # author = forms.CharField(disabled=True, initial=user[0].username, label='Автор')
    # to_post = forms.CharField(initial=title, label='На публикацию')

    class Meta:
        model = CommentaryToAuthor
        fields = ['author', 'to_post', 'comment', ]
        labels = {
            'comment': "Комментарий",
        }

