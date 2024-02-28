from django.utils.translation import gettext_lazy
from rest_framework.exceptions import ValidationError

from .models import Category


def post_media_directory_path(instance, filename) -> str:
    # Зря сделал тут эту функцию. По ходу разработки пришлось её тут оставить.
    # Все, что касается моделей, нужно делать в models
    pass


def correct_form_category_for_serializer(request):
    """
    Приложение announcement, views.py: PageCreateView, PageUpdateView.
    Подготавливает полученные данные от формы в поле "Категории" для передачи в serializer.
    Используется при TemplateHTMLRenderer.
    """
    data = request.data.copy()
    value = data.pop("category")
    try:
        label = Category.Categories(value[0]).label
    except ValueError:
        raise ValidationError(gettext_lazy(f"Не верно указана категория {value[0]}."), )
    data.update({"category.categories": label})
    return data
