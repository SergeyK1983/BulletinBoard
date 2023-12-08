from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to="cabinet/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __str__(self):
        return f"{self.pk} - {self.username}"
