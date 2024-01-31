from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from announcement.services import post_media_directory_path
from cabinet.models import User


class Post(models.Model):
    """
    Публикации. Публикация имеет одного автора и одну категорию. К публикациям возможны комментарии.
    """
    author = models.ForeignKey(
        to=User,
        to_field='username',
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        to='Category',
        to_field='categories',
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Категории'
    )
    title = models.CharField(max_length=100, unique=True, verbose_name='Заголовок')
    article = models.TextField(verbose_name='Содержание')
    images = models.ImageField(upload_to=post_media_directory_path, blank=True, null=True, verbose_name="Картинки")
    files = models.FileField(upload_to=post_media_directory_path, blank=True, null=True, verbose_name="Файлы медиа")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['id']

    def preview(self):
        article = self.article[:150]
        return article + ' ...'

    @property
    def images_url(self):
        if self.images and hasattr(self.images, 'url'):
            return self.images.url

    @property
    def files_url(self):
        if self.files and hasattr(self.files, 'url'):
            return self.files.url

    def __str__(self):
        return f"{self.author}: {self.category} - {self.title[:20]}"

    def get_absolute_url(self):
        return reverse(viewname='board_page', kwargs={'pk': self.id})  # 'name': self.author})


class Category(models.Model):
    """
    Категории публикаций
    """

    class Categories(models.TextChoices):
        # A .label property is added on values, to return the human-readable name.
        TANK = 'TK', _('Танки')
        HEALTH = 'HL', _('Хилы')
        DD = 'DD', _('ДД')
        MERCHANT = 'MCH', _('Торговцы')
        GUILDMASTER = 'GM', _('Гилдмастеры')
        QUESTGIVER = 'QG', _('Квестгиверы')
        FARRIER = 'FR', _('Кузнецы')
        TANNER = 'TN', _('Кожевники')
        POTIONMAKER = 'PM', _('Зельевары')
        SPELLMASTERS = 'SM', _('Мастера заклинаний')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    categories = models.CharField(max_length=18, choices=Categories.choices, default=Categories.TANK, unique=True,
                                  verbose_name='Категории')

    def __str__(self):
        return f"{self.categories}"
