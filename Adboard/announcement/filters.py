from django_filters import rest_framework as filters

from .models import Post, Category


class BoardListFilter(filters.FilterSet):
    """ Фильтр публикаций """

    category = filters.MultipleChoiceFilter(
        field_name="category__categories",
        choices=Category.Categories.choices,
        lookup_expr="exact",
        label='Категории',
    )
    author = filters.CharFilter(
        field_name="author__username",
        lookup_expr='exact',  # с icontains не работает
        label='Автор',
    )
    date_after = filters.DateFilter(field_name='date_create', lookup_expr='date__gte')
    date_before = filters.DateFilter(field_name='date_create', lookup_expr='date__lte')

    class Meta:
        model = Post
        fields = ["author", ]
