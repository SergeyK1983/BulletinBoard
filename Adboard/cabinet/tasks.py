from django.core.mail import send_mail

from Adboard.settings import SERVER_EMAIL

from Adboard.celery import app


@app.task
def send_mail_user_registration(email_user, html_content):
    send_mail(
        subject='Доска объявлений',
        message='',
        from_email=SERVER_EMAIL,
        recipient_list=[email_user],
        html_message=html_content,
    )
