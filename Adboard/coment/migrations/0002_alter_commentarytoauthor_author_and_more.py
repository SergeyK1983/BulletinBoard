# Generated by Django 4.2.7 on 2023-12-17 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0002_alter_post_files_alter_post_images'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentarytoauthor',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usname', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='Автор комментария'),
        ),
        migrations.AlterField(
            model_name='commentarytoauthor',
            name='to_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='announcement.post', to_field='title', verbose_name='На публикацию'),
        ),
    ]
