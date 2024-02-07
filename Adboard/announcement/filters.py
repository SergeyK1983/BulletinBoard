from django_filters import rest_framework as filters

from .models import Post, Category


class BoardListFilter(filters.FilterSet):  # filters.FilterSet
    """ Фильтр публикаций """

    category = filters.CharFilter(field_name="category__categories", lookup_expr="exact")  # , choices=Category.Categories.choices
    author = filters.CharFilter(field_name="author__username", lookup_expr="exact")
    month = filters.NumberFilter(field_name='date_create', lookup_expr='month')
    day = filters.NumberFilter(field_name='date_create', lookup_expr='day__gte')

    class Meta:
        model = Post
        fields = ["category", "author", "date_create"]

