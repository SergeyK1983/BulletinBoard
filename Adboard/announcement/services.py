from datetime import datetime

from .models import Category


def post_media_directory_path(instance, filename) -> str:
    """
     Приложение announcement, Модель Post. Формирование пути для атрибута upload_to=
    """
    date = datetime.now()
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"announcement/{instance.author}/{date.year}/{date.month}/{date.day}/{filename}"


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
