from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import CommentaryToAuthor
from .tasks import send_mail_author_when_comment_accepted


@receiver(post_save, sender=CommentaryToAuthor)
def email_to_author_when_comment_accepted(sender, instance, **kwargs):
    """ Отправка письма автору отклика/комментария, когда автор объявления примет отклик/комментарий """

    comment = CommentaryToAuthor.objects.filter(accepted=True).last()
    author_comment = comment.author.username
    email_author_comment = comment.author.email
    author_post = comment.to_post.author.username

    html_content = render_to_string(
        template_name='comment/email_accepted_comment.html',
        context={
            'comment': comment.comment,
            'title': comment.to_post.title,
            'author_comment': author_comment,
            'author_post': author_post,
        }
    )
    send_mail_author_when_comment_accepted.delay(email_author_comment, html_content)
