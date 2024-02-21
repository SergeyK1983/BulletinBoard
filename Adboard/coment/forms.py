from django import forms

from .models import CommentaryToAuthor


class CommentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CommentCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CommentaryToAuthor
        fields = ['author', 'to_post', 'comment']
        labels = {
            'comment': "Комментарий",
        }
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-input', 'disabled': True}),
            'to_post': forms.TextInput(attrs={'class': 'form-input', 'disabled': True}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 15, "autofocus": True})
        }

