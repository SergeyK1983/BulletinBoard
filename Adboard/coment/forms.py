

from django import forms
from django.http import request, HttpRequest

from .models import CommentaryToAuthor


class CommentCreateForm(forms.ModelForm):
    def get_context(self, request):
        pass

    user = 'Serg'
    title = 'Заголовок'
    author = forms.CharField(disabled=True, initial=user, label='Автор')
    to_post = forms.CharField(disabled=True, initial=title, label='На публикацию')

    class Meta:
        model = CommentaryToAuthor

        fields = ['author', 'to_post', 'comment', ]

        labels = {
            'comment': "Комментарий",
        }

