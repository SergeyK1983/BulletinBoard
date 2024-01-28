from django.db import models
from django.shortcuts import reverse

from cabinet.models import User
from announcement.models import Post


class CommentaryToAuthor(models.Model):
    """
    Отклики на публикации других авторов
    """
    author = models.ForeignKey(User, to_field='username', related_name="comment", on_delete=models.CASCADE, verbose_name='Автор комментария')
    to_post = models.ForeignKey(Post, to_field='title', related_name="comment", on_delete=models.CASCADE, verbose_name='На публикацию')
    comment = models.TextField(max_length=500, verbose_name="Комментарий")
    accepted = models.BooleanField(default=False, verbose_name="Принято")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отклик автору'
        verbose_name_plural = 'Отклики автору'
        ordering = ['id']

    def __str__(self):
        return f"{self.author}: - {self.comment[:20]}"

    def get_absolute_url(self):
        return reverse(viewname='commentary', kwargs={'pk': self.id, 'name': self.author})
