from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import CommentaryToAuthor
from .tasks import send_mail_author_when_comment_accepted, send_mail_author_announcement_when_comment


@receiver(post_save, sender=CommentaryToAuthor)
def email_to_author_when_comment_accepted(sender, instance, created, **kwargs):
    """ Отправка письма автору отклика/комментария, когда автор объявления примет отклик/комментарий """

    comment = CommentaryToAuthor.objects.filter(accepted=True).last()
    if comment:
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
        if not created:
            send_mail_author_when_comment_accepted.delay(email_author_comment, html_content)


@receiver(post_save, sender=CommentaryToAuthor)
def email_to_author_when_comment(sender, instance, created, **kwargs):
    """ Отправка письма автору объявления, когда на объявление оставлен комментарий (отклик) """

    comment = CommentaryToAuthor.objects.all().last()
    author_comment = comment.author.username
    author_post = comment.to_post.author.username
    author_post_email = comment.to_post.author.email

    html_content = render_to_string(
        template_name='comment/email_announcement_comment.html',
        context={
            'comment': comment.comment,
            'title': comment.to_post.title,
            'author_comment': author_comment,
            'author_post': author_post,
        }
    )
    if created:
        send_mail_author_announcement_when_comment.delay(author_post_email, html_content)
