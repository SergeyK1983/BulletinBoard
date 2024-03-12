from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import User
from .tasks import send_mail_user_registration


@receiver(post_save, sender=User)
def email_registration(sender, created, **kwargs):
    """ Отправка письма при регистрации пользователя """

    user = User.objects.filter().last()
    email_user = user.email

    html_content = render_to_string(
        template_name='cabinet/email_registration.html',
        context={
            'username': user.username,
        }
    )
    # if created:
    #     send_mail_user_registration.delay(email_user, html_content)
