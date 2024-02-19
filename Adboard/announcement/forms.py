from django import forms

from .models import Post, Category


class FormPost(forms.ModelForm):
    """ Форма для создания и изменения публикации """

    category = forms.ChoiceField(choices=Category.Categories.choices, label="Категории")

    class Meta:
        model = Post
        fields = ["category", "title", "article", "images", "files"]
        widgets = {
            "category": forms.Select(attrs={'class': 'form-select'}),  # от чего-то не влияет ...
            "title": forms.TextInput(attrs={'class': 'form-input'}),
            "article": forms.Textarea(attrs={'class': 'form-textarea', 'rows': 15})
        }
