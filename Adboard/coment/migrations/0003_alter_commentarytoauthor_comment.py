# Generated by Django 4.2.7 on 2023-12-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coment', '0002_alter_commentarytoauthor_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentarytoauthor',
            name='comment',
            field=models.TextField(max_length=500, verbose_name='Комментарий'),
        ),
    ]
