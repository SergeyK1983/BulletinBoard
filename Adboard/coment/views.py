import json

from django.http import request, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .models import CommentaryToAuthor
from .forms import CommentCreateForm


def comment_create(request):
    form = CommentCreateForm()
    data = json.loads(request.body)
    print(data)
    print(request.GET)
    print(request.POST)
    if form.is_valid:
        form.save()

# class CommentCreateView(LoginRequiredMixin, CreateView):
#     form_class = CommentCreateForm
#     template_name = 'comment/comment.html'
#

    # def get_success_url(self):
    #     # url = self.request.
    #     return reverse_lazy('board_page')

