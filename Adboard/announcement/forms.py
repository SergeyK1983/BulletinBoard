from django import forms

from .models import Post, Category


class FormPost(forms.ModelForm):
    category = forms.ChoiceField(choices=Category.Categories.choices, label="Категории")

    class Meta:
        model = Post
        fields = ["category", "title", "article", "images", "files"]
        widgets = {
            'article': forms.Textarea(attrs={'class': 'form-text', 'cols': 80, 'rows': 15})
        }
