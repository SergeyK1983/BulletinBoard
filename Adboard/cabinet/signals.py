from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from Adboard.settings import SERVER_EMAIL
from .models import User


@receiver(post_save, sender=User)
def email_registration(sender, created, **kwargs):
    """ Отправка письма при регистрации пользователя """

    user = User.objects.filter().last()
    email_user = user.email

    html_content = render_to_string(
        template_name='cabinet/email_registration.html',
        context={
            'user': user,
        }
    )
    if created:
        send_mail(
            subject='Доска объявлений',
            message='',
            from_email=SERVER_EMAIL,
            recipient_list=[email_user],
            html_message=html_content,
        )

