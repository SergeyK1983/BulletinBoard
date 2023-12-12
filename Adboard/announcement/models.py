from django.db import models
from django.shortcuts import reverse

from announcement.services import post_media_directory_path
from cabinet.models import User


class Post(models.Model):
    """
    Публикации. Публикация имеет одного автора и одну категорию. К публикациям возможны комментарии.
    """
    author = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(to='Category', to_field='categories', on_delete=models.CASCADE, verbose_name='Категории')
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
        return reverse(viewname='board_page', kwargs={'pk': self.id, })  # 'name': self.author})


class Category(models.Model):
    """
    Категории публикаций
    """
    TANK = 'TK'
    HEALTH = 'HL'
    DD = 'DD'
    MERCHANT = 'MCH'
    GUILDMASTER = 'GM'
    QUESTGIVER = 'QG'
    FARRIER = 'FR'
    TANNER = 'TN'
    POTIONMAKER = 'PM'
    SPELLMASTERS = 'SM'

    CATEGORY = [
        (TANK, 'Танки'),
        (HEALTH, 'Хилы'),
        (DD, 'ДД'),
        (MERCHANT, 'Торговцы'),
        (GUILDMASTER, 'Гилдмастеры'),
        (QUESTGIVER, 'Квестгиверы'),
        (FARRIER, 'Кузнецы'),
        (TANNER, 'Кожевники'),
        (POTIONMAKER, 'Зельевары'),
        (SPELLMASTERS, 'Мастера заклинаний')
    ]

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    categories = models.CharField(max_length=3, choices=CATEGORY, default=TANK, unique=True, verbose_name='Категории')

    def __str__(self):
        return f"{self.categories}"
