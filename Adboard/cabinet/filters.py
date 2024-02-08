from django_filters import rest_framework as filters
from django_filters import Filter

from announcement.models import Post
from .models import User


class CategoriesFilter(Filter):
    def filter(self, qs, value):
        if value is not None:
            user = User.objects.get(username='serg')
            qs = user.posts.filter(catecory=value)
        return qs


class UserListFilter(filters.FilterSet):
    """ Фильтр публикаций """

    # cat = CategoriesFilter(field_name='category__categories', lookup_expr='exact')

    cat = filters.CharFilter(field_name="posts", lookup_expr="icontains", label="Категории")  # , choices=Category.Categories.choices

    class Meta:
        model = User
        fields = []
