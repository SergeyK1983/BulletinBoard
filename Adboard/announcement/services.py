from datetime import datetime


def post_media_directory_path(instance, filename) -> str:
    """
     Приложение announcement, Модель Post. Формирование пути для атрибута upload_to=
    """
    time = datetime.now()
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"announcement/{instance.author}/{time.year}/{time.month}/{time.day}/{filename}"

