from django.shortcuts import render
from django.views.generic import DetailView, ListView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions

from coment.models import CommentaryToAuthor
from .models import User
from announcement.models import Post
from .serializer import ProfileSerializer


# if request.user.is_authenticated:
#     ...  # Do something for logged-in users.
# else:
#     ...  # Do something for anonymous users.

class ProfileDetail(DetailView):
    model = User
    template_name = 'cabinet/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(id=self.object.pk)
        context['posts'] = Post.objects.filter(author=user[0].username)
        context['comments'] = CommentaryToAuthor.objects.filter(to_post__author=user[0].username)
        return context


class ProfileList(ListView):
    model = Post
    template_name = 'cabinet/profile_list.html'
    context_object_name = 'profilelist'

