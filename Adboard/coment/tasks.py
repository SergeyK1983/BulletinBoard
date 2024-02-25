from django.core.mail import send_mail

from Adboard.settings import SERVER_EMAIL

from Adboard.celery import app


@app.task
def send_mail_author_when_comment_accepted(email_author_comment, html_content):
    send_mail(
        subject='Доска объявлений',
        message='',
        from_email=SERVER_EMAIL,
        recipient_list=[email_author_comment],
        html_message=html_content,
    )
