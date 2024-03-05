from django_filters import rest_framework as filters

from announcement.models import Category
from .models import CommentaryToAuthor


class CommentListFilter(filters.FilterSet):
    """ Фильтр своих комментариев на своей странице """

    category = filters.MultipleChoiceFilter(
        field_name="to_post__category__categories",
        choices=Category.Categories.choices,
        lookup_expr="exact",
        label='Категории',
    )
    author_post = filters.CharFilter(
        field_name="to_post__author__username",
        lookup_expr='exact',
        label='Автор',
    )
    date_after = filters.DateFilter(field_name='date_create', lookup_expr='date__gte')
    date_before = filters.DateFilter(field_name='date_create', lookup_expr='date__lte')

    class Meta:
        model = CommentaryToAuthor
        fields = ["author", ]
