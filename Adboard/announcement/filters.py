from django_filters import rest_framework as filters

from .models import Post, Category


class BoardListFilter(filters.FilterSet):  # filters.FilterSet
    """ Фильтр публикаций """

    category = filters.ChoiceFilter(field_name="category__categories", choices=Category.Categories.choices, lookup_expr="exact", label='Категории')  # , choices=Category.Categories.choices
    author = filters.CharFilter(field_name="author__username", label='Автор')
    # month = filters.NumberFilter(field_name='date_create', lookup_expr='month')
    # day = filters.NumberFilter(field_name='date_create', lookup_expr='day__gte')

    class Meta:
        model = Post
        fields = ["author", ]

