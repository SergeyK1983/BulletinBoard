from django_filters import rest_framework as filters
from django_filters import Filter

from announcement.models import Post, Category
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


class BoardListFilter(filters.FilterSet):
    """ Фильтр публикаций """

    category = filters.MultipleChoiceFilter(
        field_name="category__categories",
        choices=Category.Categories.choices,
        lookup_expr="exact",
        label='Категории',
    )
    date_after = filters.DateFilter(field_name='date_create', lookup_expr='date__gte')
    date_before = filters.DateFilter(field_name='date_create', lookup_expr='date__lte')

    class Meta:
        model = Post
        fields = []
