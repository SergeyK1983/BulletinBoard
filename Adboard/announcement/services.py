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
    label = Category.Categories(value[0]).label
    data.update({"category.categories": label})
    return data
