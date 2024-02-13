from django_filters import rest_framework as filters
from django_filters import Filter
from django_filters.filterset import BaseFilterSet
from rest_framework.filters import BaseFilterBackend

from announcement.models import Post, Category
from .models import User


class CategoriesFilter(Filter):
    def filter(self, qs, value):
        if value is not None:
            user = User.objects.get(username='serg')
            qs = user.posts.filter(category__categories=value)
        return qs


class PostsListFilter(filters.FilterSet):
    """ Фильтр публикаций """

    category = filters.MultipleChoiceFilter(
        field_name="category__categories",
        choices=Category.Categories.choices,
        lookup_expr="exact",
        label='Категории',
    )
    date_after = filters.DateFilter(field_name='date_create', lookup_expr='date__gte', label='Дата после:')
    date_before = filters.DateFilter(field_name='date_create', lookup_expr='date__lte', label='Дата до:')

    class Meta:
        model = Post
        fields = []


class UserListFilter(filters.FilterSet):
    """ Фильтр публикаций """
    pass
