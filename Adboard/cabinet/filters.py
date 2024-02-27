from django_filters import rest_framework as filters
from django_filters import Filter
from django_filters.filterset import BaseFilterSet
from rest_framework.filters import BaseFilterBackend

from announcement.models import Post, Category
from .models import User


class DateAfterFilter(Filter):
    def filter(self, qs, value):
        if value is not None:
            qs = Post.objects.filter(author=self.request.user.username)
        return qs


def posts(request):
    user = request.user.username
    return user.posts.all()


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

    date_after = filters.DateFilter(field_name='posts__date_create', lookup_expr='date__gte', label='Дата после:')

    class Meta:
        model = User
        fields = []
        # fields = {
        #     'posts__date_create': ('date__gte', ),
        # }

