from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def post_media_directory_path(instance, filename) -> str:
    """
     Приложение cabinet, Модель User. Формирование пути для атрибута upload_to=
    """
    date = datetime.now()
    return f"cabinet/{instance.id}-{instance.username}/{date.year}/{date.month}/{date.day}/{filename}"


class User(AbstractUser):
    photo = models.ImageField(upload_to=post_media_directory_path, blank=True, null=True, verbose_name="Фотография")  # можно так: upload_to="cabinet/%Y/%m/%d/"
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __str__(self):
        return f"{self.pk} - {self.username}"

    def get_commentary_url(self):
        """ view in coment """
        return reverse(viewname='my-comment', kwargs={'username': self.username})

    def get_absolute_url(self):
        return reverse(viewname='profile', kwargs={'id': self.id})
