import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import request, HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from Adboard.settings import SERVER_EMAIL
from .models import CommentaryToAuthor
from announcement.models import Post
from .forms import CommentCreateForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = CommentaryToAuthor
    form_class = CommentCreateForm
    template_name = 'comment/comment.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.request.POST)
        print(self.object.author)
        print(self.kwargs)
        # title = Post.objects.get(id=self.kwargs['id'])
        current_user = self.request.user
        self.object.author = current_user
        # print(title)
        print(current_user)
        print(self.object.author)

        comment = self.request.POST.get['comment']
        post_title = self.request.POST.get['to_post']

        # html_content = render_to_string(
        #     template_name='comment/email_comment.html',
        #     context={
        #         'from_user': current_user.username,
        #         'post_author': '',
        #         'post_title': post_title,
        #         'comment': comment,
        #     }
        # )
        # send_mail(
        #     subject='Доска объявлений',
        #     message='',
        #     from_email=SERVER_EMAIL,
        #     recipient_list=[user.email, ],
        #     html_message=html_content,
        # )

        return super().form_valid(form)

    def get_success_url(self):
        # url = self.request.
        return reverse_lazy('board_list')

