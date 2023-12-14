from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import generics, permissions

from Adboard.settings import LOGIN_URL
from coment.models import CommentaryToAuthor
from .forms import LoginUserForm, RegisterUserForm, UpdateUserForm
from .models import User
from announcement.models import Post
from .serializer import ProfileSerializer
from .services import get_username


# if request.user.is_authenticated:
#     ...  # Do something for logged-in users.
# else:
#     ...  # Do something for anonymous users.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'cabinet/login.html'

    def get_success_url(self):
        return reverse_lazy('board_list')


class LogoutUser(LogoutView):
    def get_success_url(self):
        return reverse_lazy('board_list')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'cabinet/register.html'
    success_url = reverse_lazy('login')


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'cabinet/update.html'
    # pk_url_kwarg = 'id'

    def get_queryset(self):
        self.queryset = super().get_queryset()
        username = get_username(request=self.request)
        queryset = User.objects.filter(username=username)
        return queryset

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.pk])


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'cabinet/profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'id'

    login_url = LOGIN_URL

    def get_queryset(self):
        self.queryset = super().get_queryset()
        username = get_username(request=self.request)
        queryset = User.objects.filter(username=username)
        return queryset

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

